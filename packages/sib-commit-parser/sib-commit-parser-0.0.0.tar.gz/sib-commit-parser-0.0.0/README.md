# Conventional changelog for Startin'blox

## Commit types

| Commit Type | Title      | Description       | Release    | In changelog |
|:-----------:|------------|-------------------|------------|:------------:|
| `minor`     | Minor      | Minor release     | `minor`    | `yes`        |
| `major`     | Major      | Major release     | `major`    | `yes`        |
| `feature`   | Features   | New behavior      | `patch`    | `yes`        |
| `update`    | Updates    | Change behavior   | `patch`    | `yes`        |
| `bugfix`    | Bug Fixes  | Fix bugs          | `patch`    | `yes`        |
| `ui`        | Interface  | Change appearance | `patch`    | `yes`        |
| `syntax`    | Syntax     | Refactoring code  | `patch`    | `yes`        |
|             | Other      | All others        | `patch`    | `no`         |

[See reference](https://git.happy-dev.fr/startinblox/management#commit-messages)

## Setup

Add the relevant `semantic_release` section to your `setup.cfg`:
```
[semantic_release]
version_variable = myapp/__init__.py:__version__
commit_parser = sib_semantic_release.parser
```

Install the package in your build environment (not working yet!):
```
$ pip install sib-semantic-release
```

FIXME: force installation from specific indexes:
```
$ pip install git+https://github.com/plup/python-semantic-release
$ pip install git+https://git.happy-dev.fr/startinblox/semantic-release-py
```
