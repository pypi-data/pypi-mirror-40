# sample_python_package
Testing python package creation.

## Procedure

#### Creating a simple package
     your-git-repo/
           your-package/
               __init__.py
           setup.py
1. Create the directory structure above. 
    * Give your package a unique name so that it can be uploaded to PyPI. 
2. Write a function in `__init__.py`. 
    * From Python docs: The `__init__.py` file is required for Python to 
    treat the directory as containing a package. In the simplest case, it 
    can actually just be an empty file. 
3. Write a single call to `setuptools.setup()` in `setup.py`. 
    * From setuptools docs: The simplest setup needs only a few parameters
    like `name` (name of the distribution's tar.gz file), `version`, and `packages`. 
    * The `zip_safe` flag lets you decide whether your project can be installed
    as a zipfile or directory.
    * *TODO:* Add link to or create list of setuptools parameters.
4. You can now install the package locally using `pip install .`

#### Twine
Use Twine to publish Python packages on PyPI. 
1. `pip install twine`
2. Create an account on PyPI: https://pypi.org/
3. Create a tar.gz file using `python setup.py sdist`. This command creates a directory `dist/` that contains the source distribution.
4. Upload to PyPI using `twine upload dist/*`. You will be prompted for your PyPI username and password.
5. Your package can now be installed by anyone using `pip install your-package-name`.
6. If you want to publish an updated version of your package:
    1. In `setup.py`, change the `version`.
    2. Repeat step 3 above. There will now be the new version of your package in `dist/`.
    3. Upload using `twine upload dist/your-updated-package`. 
    4. To update on your machine, use `pip install your-package-name --upgrade`.

#### Using pytest
Using pytest is possible with setuptools, but will require a few extra steps.
1. In `setup.py`, add two more parameters to the `setup` call: 
`setup-requires=['pytest-runner']` and `tests-require=['pytest']`. These two
will allow us to run pytest. 
2. Create a new file `setup.cfg` and add `[aliases]`. In the next line, add
`test=pytest`.
    * In `setup.cfg`, users can write values for parameters in `setup.py` using a 
    basic syntax. Values in `setup.py` will override values in `setup.cfg`. 
3. Create a new `tests/` directory in your module with your test files.  
4. Use `python setup.py test` to run your tests. 

#### On using data
If your package uses data (i.e., as a .csv file), it's best to have it in
the same directory as as the .py file that uses it. In order to include it 
as part of your distribution, you need to do the following steps:
1. Create `MANIFEST.in` in the root directory of the git repository.
2. Write `include filepath/to/your/data.csv`.
    * You must also `include` README files and other non-Python files in
     `MANIFEST.in`. 

#### Using Docker in your package
TBD

#### Example
1. `pip install sample_python_package`
2. In Python, try:
   * `>>> import sample_python_package`
   * `>>> sample_python_package.hello()`