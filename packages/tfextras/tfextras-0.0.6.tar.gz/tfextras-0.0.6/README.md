# Tensorflow Extras

> pip3 install tfextras

[![HitCount](http://hits.dwyl.io/nardeas/tensorflow-extras.svg)](http://hits.dwyl.io/nardeas/tensorflow-extras)

Various helpful extra utilities for deep learning with Tensorflow.

## Install

If you install via pip it will automatically install all the dependencies for you. If you insist on not using pip then check [here](https://github.com/nardeas/tensorflow-extras/blob/master/setup.py).

```
pip install tfextras
pip3 install tfextras
```

## Docs

[Full documentation here](https://github.com/nardeas/tensorflow-extras/blob/master/DOCS.md)

## Development

**Running tests**

```
ptw -p --runner "pytest --cov=tfextras --cov-report=term-missing --cov-branch test/unit -s"
ptw -p --runner "pytest --cov=tfextras --cov-report=term-missing --cov-branch test/integration -s"
```

**Develop**

```
pip install -e .
rm ~/.virtualenvs/<envname>/lib/python3.6/site-packages/tfextras.egg-link
rm -r $(find . -name '*.egg-info')
```

**Update**

```
python setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
twine upload dist/* && rm build && rm dist
```
