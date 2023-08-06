import argparse
import os
import os.path
import glob
import re
import sys
import subprocess
import shlex
from pathlib import Path
from functools import cmp_to_key

from structlog import get_logger, wrap_logger
from structlog.dev import ConsoleRenderer
import yaml
import semver
import pkgconfig

glog = wrap_logger(get_logger(), processors=[ConsoleRenderer(pad_event=42, colors=True)])

cc = os.getenv('CC', 'gcc')
cxx = os.getenv('CXX', 'g++')

def system(cmd):
  glog.info('execute', cmd=cmd)
  os.system(cmd)

def has_updated_headers(std, flags, ifile):
  glog.info('has_updated_headers()', file=ifile)

  c = ''
  if ifile.endswith('.c'):
    c = cc
  elif ifile.endswith('.cpp'):
    c = cxx
  else:
    glob.failure('invalid file extension', file=ifile)
    sys.exit(1)
  
  out = subprocess.check_output(shlex.split(c + ' ' + flags + ' -std=' + std + ' -M ' + ifile)).decode('utf-8')
  sp = re.compile(r'[\\\r\n\s]+').split(out)
  sp.pop(0)
  sp.pop(0)

  for f in sp:
    if not f:
      continue
    if os.path.getmtime(f) > os.path.getmtime(ifile):
      return True
  
  return False

def has_updated_sources(ofile, ifiles):
  glog.info('has_updated_sources()', ofile=ofile)

  if not os.path.isfile(ofile):
    return True
  
  for f in ifiles:
    if not f:
      continue
    if os.path.getmtime(f) > os.path.getmtime(ofile):
      return True
    
  
  return False
  
class Target:
  def __init__(self, ctx, pm, name, data):
    self.log = glog.bind(pkg=pm.name, name=name, type=data['type'])
    self.log.info('Target()')
    self.ctx = ctx
    self.pm = pm
    self.name = name
    self.data = data
    self.built = False
    self.linked = False
    self.link_info = data.get('link', [])
    self.link = {}
    self.type = data.get('type', 'executable')
    def upd(d):
      if ctx.this_package.name == pm.name:
        return d
      else:
        return './dumbcpm-packages/' + pm.name + '/' + d + '/'
    self.include_dirs = set([upd(d) for d in data.get('include-dirs', [])])
    self.sources = data.get('sources', [])
    self.cpp = data.get('cpp', 'c++11')
    self.c = data.get('c', 'c11')
    self.pkg_config = data.get('pkg-config', [])
    self.flags = ' -Wl,-rpath=\'$ORIGIN\' -fPIC -L./dumbcpm-build/ ' + data.get('flags', '') + ' '
    self.has_cpp_sources = False
    for s in self.sources:
      if s.endswith('.cpp'):
        self.has_cpp_sources = True
        break
    
class PackageManifest:
  def __init__(self, ctx, data):
    self.log = glog.bind(name=data['name'], version=data['version'])
    self.log.info('PackageManifest()')
    self.ctx = ctx
    self.data = data
    self.name = data['name']
    self.version = data['version']
    self.git_repo = data['git-repo']
    self.git_tag = data['git-tag']
    self.depends = data.get('depends', {})
    self.targets_base = data.get('targets', {})
    self.targets = {}
    self.also_build = data.get('also-build', [])
    self.loaded = False
    self.built = False
    self.loaded_targets = False
    
  def load_targets(self):
    if self.loaded_targets:
      return
    self.loaded_targets = True
    for k, v in self.targets_base.items():
      self.targets[k] = Target(self.ctx, self, k, v)

  def fetch(self):
    cwd = os.getcwd()
    os.chdir('./dumbcpm-packages')
    if not os.path.isdir('./' + self.name):
      system('git clone ' + self.git_repo + ' -b ' + self.git_tag + ' ' + self.name)
    else:
      os.chdir('./' + self.name)
      system('git pull')
      system('git checkout ' + self.git_tag)
    os.chdir(cwd)

class Repository:
  def __init__(self, ctx, path):
    self.log = glog.bind(path=path)
    self.log.info('Repository()')
    self.ctx = ctx
    self.path = path
    with open(self.path + '/repository.yaml', 'r') as f:
      self.data = yaml.load(f)
    self.package_names = self.data['packages']
    self.versions = {}
    
  def list_versions(self, name):
    self.log.info('Repository.list_versions()', name=name)
    
    if name in self.versions:
      return self.versions[name]
    
    vv = glob.glob(self.path + '/' + name + '/' + name + '-*.*.*.yaml')
    vr = []
    for v in vv:
      s = re.search(r'^.*?-(\d+\.\d+\.\d+)\.yaml$', v, re.IGNORECASE)
      if s:
        vr.append(s.group(1))
    self.versions[name] = vr
    return self.versions[name]

  def has_package(self, name, version):
    if os.path.isfile(self.path + '/' + name + '/' + name + '-' + version + '.yaml'):
      return True
    return False

class PMContext:
  def __init__(self):
    self.log = glog
    self.log.info('Hello, World!')
    with open(str(Path.home()) + '/.dumbcpm.yaml') as f:
      self.data = yaml.load(f)
    self.repository_paths = self.data['repositories']
    self.repositories = []
    for path in self.repository_paths:
      self.repositories.append(Repository(self, path))
    self.versions = {}
    self.packages = {}
    self.packages_v = {}
    self.this_package = None
    
  def list_versions(self, name):
    self.log.info('PMContext.list_versions()', name=name)
    if name in self.versions:
      return self.versions[name]
    s = set()
    for r in self.repositories:
      vv = r.list_versions(name)
      for v in vv:
        s.add(v)
    self.versions[name] = sorted(list(s), key=cmp_to_key(semver.compare))
    return self.versions[name]

  def load(self, name, version='latest', build=False):
    self.log.info('PMContext.load()', name=name, version=version, build=build)
    if version == 'latest':
      vv = self.list_versions(name)
      version = vv[-1]
    if (name + '-' + version) in self.packages:
      return self.packages[name + '-' + version]
    for r in self.repositories:
      if build or r.has_package(name, version):
        pt = None
        if build:
          pt = './dumbcpm-packages/' + name + '/package.yaml'
        else:
          pt = r.path + '/' + name + '/' + name + '-' + version + '.yaml'
        with open(pt, 'r') as f:
          p = PackageManifest(self, yaml.load(f))
          self.packages[name + '-' + version] = p
          if not name in self.packages_v:
            self.packages_v[name] = {}
          self.packages_v[name][version] = p
          return self.packages[name + '-' + version]
    self.log.failure('unable to find a package', name=name, version=version)
    sys.exit(1)

  def load_this(self, build=False):
    self.log.info('PMContext.load_this()', build=build)
    with open('./package.yaml', 'r') as f:
      data = yaml.load(f)
      self.this_package = PackageManifest(self, data)
      self.packages[self.this_package.name + '-' + self.this_package.version] = self.this_package
      if not self.this_package.name in self.packages_v:
        self.packages_v[self.this_package.name] = {}
      self.packages_v[self.this_package.name][self.this_package.version] = self.this_package
      self.versions[self.this_package.name] = [self.this_package.version]
    self.load_dependencies(self.this_package, build)
    
  def limit_package_versions(self, name, spec):
    self.log.info('PMContext.limit_package_versions()', pkg=name, spec=spec)
    specs = spec.split(',')
    def matches(v):
      for s in specs:
        if not semver.match(v, s):
          return False
      return True
    vv = self.versions[name]
    vv = [v for v in vv if matches(v)]
    vv = sorted(vv, key=cmp_to_key(semver.compare))
    if not vv:
      self.log.failure('unable to find at least one matching version', pkg=name, spec=spec)
    self.versions[name] = vv
    
  def load_dependencies(self, pkg, build=False):
    self.log.info('PMContext.load_dependencies()', pkg=pkg.name, build=build)
    if pkg.loaded:
      return
    pkg.loaded = True
    for k, v in pkg.depends.items():
      self.list_versions(k)
      self.limit_package_versions(k, v)
      self.load_dependencies(self.load(k, 'latest', build), build)
      
  def fetch(self):
    self.log.info('PMContext.fetch()')
    if not os.path.isdir('./dumbcpm-packages/'):
      os.mkdir('./dumbcpm-packages/')
    for name, vers in self.packages_v.items():
      if name == self.this_package.name:
        continue
      p = vers[self.versions[name][-1]]
      p.fetch()

  def build_file(self, pkg, target, ifile, ofile):
    self.log.info('PMContext.build_file()', pkg=pkg.name, target=target.name, ifile=ifile, ofile=ofile)
    c = ''
    std = ''
    if ifile.endswith('.c'):
      c = cc
      std = target.c
    elif ifile.endswith('.cpp'):
      c = cxx
      std = target.cpp
    else:
      self.log.failure('invalid file extension', file=ifile)
      sys.exit(1)
    if os.path.isfile(ofile) and ((os.path.getmtime(ofile) < os.path.getmtime(ifile)) or (not has_updated_headers(std, target.flags, ifile))):
      return
    system(c + ' -c ' + target.flags + ' -std=' + std + ' -o ' + ofile + ' ' + ifile)
    
  def build_target(self, pkg, target):
    self.log.info('PMContext.build_target()', pkg=pkg.name, target=target.name)
    if target.built:
      return
    target.built = True
    if not target.sources:
      return
    ofiles = []
    for ifile in target.sources:
      if pkg.name != self.this_package.name:
        ifile = './dumbcpm-packages/' + pkg.name + '/' + ifile
      ofile = ifile + '.o'
      ofiles.append(ofile)
      self.build_file(pkg, target, ifile, ofile)
    c = ''
    if target.has_cpp_sources:
      c = cxx
    else:
      c = cc
    if target.type == 'executable':
      if has_updated_sources('./dumbcpm-build/' + target.name, ofiles):
        system(c + ' ' + target.flags + ' -o ./dumbcpm-build/' + target.name + ' ' + ' '.join(ofiles))
    elif target.type == 'library':
      if has_updated_sources('./dumbcpm-build/lib' + target.name + '.so', ofiles):
        system(c + ' -shared ' + target.flags + ' -o ./dumbcpm-build/lib' + target.name + '.so ' + ' '.join(ofiles))
    else:
      self.log.failure('invalid target type', target=target.name, type=target.type)
      sys.exit(1)
        
  def build_pkg(self, pkg):
    self.log.info('PMContext.build_pkg()', pkg=pkg.name)
    if pkg.built:
      return
    pkg.built = True
    for pn in pkg.depends.keys():
      self.build_pkg(self.packages_v[pn][self.versions[pn][-1]])
    self.log.info('actually building', pkg=pkg.name)
    for tn, to in pkg.targets.items():
      self.build_target(pkg, to)

  def link_target_pkgconfig(self, pkg, target, pc):
    self.log.info('PMContext.link_target_pkgconfig()', pkg=pkg.name, target=target.name, pc=pc)
    if not pkgconfig.exists(pc):
      self.log.failure('unable to find a pkg-config', pc=pc)
    target.flags += (' ' + pkgconfig.libs(pc) + ' ' + pkgconfig.cflags(pc))
      
  def link_target(self, pkg, target):
    self.log.info('PMContext.link_target()', pkg=pkg.name, target=target.name)
    if target.linked:
      return
    target.linked = True
    for pc in target.pkg_config:
      self.link_target_pkgconfig(pkg, target, pc)
    for dn in target.link_info:
      sp = dn.split('/')
      p = sp[0]
      t = sp[1]
      if (not p in self.packages_v) or (not self.packages_v[p]):
        self.log.failure('unable to find package for target', pkg=p, target=t)
        sys.exit(1)
      po = self.packages_v[p][self.versions[p][-1]]
      po.load_targets()
      if not t in po.targets:
        self.log.failure('unable to find target in package', pkg=p, target=t)
        sys.exit(1)
      to = po.targets[t]
      if to.type != 'library':
        self.log.failure('unable to link to a non-library target', pkg=p, target=t)
        sys.exit(1)
      target.link[dn] = to
      target.include_dirs = target.include_dirs.union(to.include_dirs)
    for d in target.include_dirs:
      target.flags += (' -I' + d)
    for dn, to in target.link.items():
      target.flags += (' -l' + to.name)
      
  def build(self):
    self.log.info('PMContext.build()')
    for name, vv in self.packages_v.items():
      pkg = vv[self.versions[name][-1]]
      pkg.load_targets()
      for tn, t in pkg.targets.items():
        self.link_target(pkg, t)
    self.build_pkg(self.this_package)
    for dn in self.this_package.also_build:
      print('Also building ' + dn)
      sp = dn.split('/')
      pn = sp[0]
      tn = sp[1]
      pkg = self.packages_v[pn][self.versions[pn][-1]]
      t = pkg.targets[tn]
      self.build_target(pkg, t)
      
if __name__ == "__main__":
  home = str(Path.home())

  if not os.path.isfile(home + '/.dumbcpm.yaml'):
    with open(home + '/.dumbcpm.yaml', 'w+') as f:
      f.write('repositories:\n  - ' + home + '/dumbcpm-repos/handicraftsman-dumbcpm-packages')
  
  if not os.path.isdir(home + '/dumbcpm-repos/'):
    os.mkdir(home + '/dumbcpm-repos/')

  if not os.path.isdir(home + '/dumbcpm-repos/handicraftsman-dumbcpm-packages'):
    system('bash -c "cd ' + home + '/dumbcpm-repos/; git clone https://github.com/handicraftsman/dumbcpm-packages handicraftsman-dumbcpm-packages"')

  parser = argparse.ArgumentParser(prog='dumbcpm')
  
  subparsers = parser.add_subparsers(help='available subcommands', dest='which')

  parser_fetch = subparsers.add_parser('fetch', help='fetches package dependencies')
  parser_fetch.set_defaults(which='fetch')

  parser_build = subparsers.add_parser('build', help='builds current package and its dependencies')
  parser_build.set_defaults(which = 'build')

  res = parser.parse_args()

  if res.which == 'fetch':
    ctx = PMContext()
    ctx.load_this()
    ctx.fetch()
  elif res.which == 'build':
    if not os.path.isdir('./dumbcpm-build'):
      os.mkdir('./dumbcpm-build')
    ctx = PMContext()
    ctx.load_this(True)
    ctx.build()
  else:
    print('Invalid command')
    sys.exit(2)
