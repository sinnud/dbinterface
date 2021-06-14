## Database Connection
This module will connect database like

- PostgreSQL
- mySQL

## compile
The command to compile the package is
```python -m build --wheel```
Assume you have `pip install build`

## Unittest for this development
- The unittest can also be treated as sample of using this module.
- run test from the folder this file belong to with command `python -m unittest tests.[test_file].[test_func]`

## install compiled package
```pip --disable-pip-version-check install --find-links ./dist jsonutils```

## Auto doc generation
Create PDF version documentation, store as extra source file in repository.

- The python module sphinx to `make latex`
- The MikTeX software to `pdflatex jsonutils.tex`
- copy the PDF file to repository