# dumcpm

Possibly very dumb package manager for C/++, written in Python.

## Installation

```bash
$ pip install dumbcpm
```

## Usage

### Getting root repository

Root repository will be cloned into `~/dumbcpm-repos/handicraftsman-dumbcpm-packages` on first start.

To update root repository, run `git pool` in its root directory.

### Writing a package manifest

This is the package manifest i used for testing:

```
name: hello
version: 0.1.0
description: "Hello, World!"

git-repo: "/home/handicraftsman/dumbcpm/hello/"
git-tag: master

depends:
  world: ">=0.1.0,<0.2.0"

# In this way you can tell dumbcpm to also build given targets. (if they're not built by default)
# This field is honored only in the root package (aka working)
#also-build:
#  - world/world

targets:
  hello:
    type: executable # 'library' is another possible type.
                     # It will produce a shared library.
    sources:
      - "src/main.cpp"
      - "src/whatever.c"
    include-dirs: # include dirs are also passed into the targets which depend on this one
      - "."
    cpp: "c++17"
    c: "c11"
    pkg-config:
      - "jsoncpp >= 1.8.4"
    link:
      - world/world # In this way you can link to a library dependency provided by
                    # another package.
    # flags: -DWHATEVER # In this way you can define extra compile flags to be used
                        # at compile time.
    # after-flags: -DWHATEVER # These flags will be added at the end of the command.
                              # This can be used for linking with static libraries.
```

### Fetching packages for build

```bash
python -m dumbcpm fetch
```

This will check installed repositories for needed packages and download them.

### Building packages

```bash
python -m dumbcpm build
```

This will build all targets specified in the current package and their dependencies into
`./dumbcpm-build/` directory.

More targets to build can be specified as shown above.

### Copying libraries

pkg-config libraries required by the project can be copied into the build directory using the next command:

```bash
python -m dumbcpm libs
```

### Creating a repository

dumbcpm repository is a folder (possibly a git repository) with structure like below:

```
repository.yaml
<package>/
  <package>-<version>.yaml
```

repository.yaml example:

```yaml
packages:
  - hello
  - world
```

### Installing a repository

After creating or cloning a repository, it must be registered in `~/.dumbcpm.yaml` as shown below:

```yaml
repositories:
  - /home/%USERNAME%/dumbcpm-repos/handicraftsman-dumbcpm-packages
```

handicraftsman-dumbcpm-packages is a clone of https://github.com/handicraftsman/dumbcpm-packages/

### Adding a package to a repository

As shown above, your new package can be added to the repository by adding a new entry to its `repository.yaml`

New package version can be added by copying your `package.yaml` to `/path/to/repo/<pkg>/<pkg>-<version>.yaml`

