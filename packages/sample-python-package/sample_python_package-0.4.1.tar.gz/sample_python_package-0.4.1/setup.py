from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
      # Basic distribution info
      name='sample_python_package', #name of tar.gz file
      version='0.4.1', #version, must be updated to upload edits to PyPI
      packages=find_packages('src'),
            #the actual code to be distributed as a python package, include all packages under src
            #can specify packages or directories/files to exclude
      package_dir={'':'src'}, #tell disutils packages are under src #why are this and the above necessary?

      # Dependencies for project
      install_requires=[              #specifies what other distributions must be installed with your package
                        'pandas >= 0.23.0',     #all dependencies not already installed will be downloaded and installed
                        'numpy',
                        ],
      #python_requires='3.7', #specifies the version of Python to use
      setup_requires=['pytest-runner'], #specifies other distributions necessary for setup to run
      tests_require=['pytest'], #specifies another test method than what setuptools uses
      #dependency_links=['https://github.com/mashiyatz/test.git'],
            #strings to be searched when project depends on packages not on PyPI

      # PyPI metadata
      author='Mashiyat Zaman',
      author_email='Mashiyat_Zaman@r.recruit.co.jp',
      description='Testing',
      long_description='Testing Python package creation.',
      license='RCO',
      url='https://ghe.kst3.jp/contents-create-dev/sample_python_package',


      include_package_data=True, #allows files listed in MANIFEST.in to be included with distribution
      exclude_package_data={'': ['tests/*']}, #exlude from all packages
      scripts=['bin/script-sample'], #allows module to be accessed via command line
      zip_safe=False #specifies whether the project can be run from the zip file

)