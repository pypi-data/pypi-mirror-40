# Directrix Package

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

This requires setuptools, wheel, and twine.

To create source and binary distributions in the dist/ folder execute:

```
python setup.py sdist bdist_wheel
```

To upload to PyPI test server execute:

```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

To install from PyPI test server execute:

```
pip install --index-url https://test.pypi.org/simple/ directrix_pkg
```

To upload to PyPI production server execute:

```
twine upload dist/*
```

To install from PyPI production server execute:

```
pip install directrix_pkg
```
