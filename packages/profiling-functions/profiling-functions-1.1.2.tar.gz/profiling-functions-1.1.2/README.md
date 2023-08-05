# Build library
```commandline
python3 -m pip install --user --upgrade setuptools wheel
rm -rf dist/
python3 setup.py sdist bdist_wheel
```


# Upload to pypi:
```commandline
python3 -m pip install --user --upgrade twine
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
twine upload dist/*
```

