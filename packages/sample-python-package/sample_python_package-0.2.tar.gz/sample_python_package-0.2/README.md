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
    like `name`, `version`, and `packages`. If you want to publish it, you'll
    add more parameters. 
    * The `zip_safe` flag lets you decide whether your project can be installed
    as a zipfile or directory.
4. You can now install the package locally using `pip install .`

#### Twine
Use Twine to publish Python packages on PyPI. 
1. `pip install twine`
2. Create an account on PyPI: https://pypi.org/
3. Create a tar.gz file using `python setup.py sdist`. This command creates a directory `dist/` that contains the source distribution.
4. Upload to PyPI using `twine upload dist/*`. You will be prompted for your PyPI username and password.
5. Your package can now be installed by anyone using `pip install your-package-name`.

#### Example
1. `pip install sample_python_package`
2. In Python, try:
   * `>>> import sample_python_package`
   * `>>> sample_python_package.hello()`