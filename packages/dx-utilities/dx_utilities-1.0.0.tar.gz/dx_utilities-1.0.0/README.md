# `dx-utilities` package

A collection of base utilities for engineering software packages.

# Installation

## Development

* Create virtual environment:

        $ make install

* Activate virtual environment and run tests:

        $ source venv/bin/activate
        $ nose2

## As a dependency

### From source code

```
$ pip install git://git@gitlab.com/d-e/dx-utilities.git#egg=dx_utilities
```

### From Python Package Index (PyPI)

```
$ pip install dx-utilities
```

## Features

* Geometry module on top of `shapely`_.
* Representations of physical fields.
* Linear algebra and numerical integration

  * Utilities on top of `numpy` and `mathutils.Vector`.

* Decorators.
* Exception classes with error-code.
* Data-structures.
* Book-keeping of physical constants and manipulation of units.
* Testing and printing utilities

### Sample usage

```
>>> from dx_utilities.geometry import PlanarShape
>>> rectangle = PlanarShape.new(shape='rectangle', bx=1.0, by=2.0)
>>> rectangle.area
2.0
```

## Contribute

Source code lives in https://gitlab.com/d-e/dx-utilities.

### Code of conduct

We abide by the provisions of [Contributor Coventant Code of Conduct][COC].

### Workflow

Follow this [simplified gitflow model][gitflow].

### Coding standards

* Follow [PEP8 rules](https://www.python.org/dev/peps/pep-0008/).
* Populate docstrings with concise descriptions and the signature
  of the object according to [sphinx guidelines][sphinx-sig]. For a
  complete overview of documentation options see
  [Sphinx docs](http://www.sphinx-doc.org)
* Write unit-tests.

### Versioning

We follow [semantic versioning][semver].

### Review the docs locally

Documentation is generated through continuous-integration (CI). For
review purposes it can be generated locally with:

```
$ make MODPATH=../dx_utilities -C docs apidoc html
```

For more details on the process run

```
$ make docs-help
```

## Public API

See the [documentation pages](https://d-e.gitlab.io/dx-utilities/).


## License

This program is free software: you can redistribute it and/or modify
it under the terms of the [GNU Affero General Public License](LICENSE) as
published by the Free Software Foundation, either version 3 of the
License, or any later version.

[gitflow]: https://gitlab.com/d-e/dx-utilities/wikis/git-workflow
[semver]: https://semver.org/
[COC]: https://www.contributor-covenant.org/version/1/4/code-of-conduct
[sphinx-sig]: http://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#info-field-lists
