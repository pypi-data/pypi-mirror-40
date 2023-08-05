# Tensorflow Extras

Various helpful extra utilities for deep learning with Tensorflow.

## Overview

TODO

## Docs

TODO

## Development

**Running tests**

```
ptw -p --runner "pytest --cov=tfextras --cov-report=term-missing --cov-branch test/unit -s"
```

**Develop**

```
pip install -e .
rm -r $(find . -name '*.egg-info')
```

**Push**

```
python setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
twine upload dist/*
```
