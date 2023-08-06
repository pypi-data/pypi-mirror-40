from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='sample_python_package',
      version='0.3.1',
      description='Testing',
      include_package_data=True, #allows files listed in MANIFEST.in to be included with distribution
      long_description='Testing Python package creation.',
      # classifiers=[
      #     'Development Status :: 1 - Alpha',
      #     'License :: D Approved :: E License',
      #     'Programming Language :: Python :: 3.7',
      #     'Topic :: Date & Time'
      # ],
      url='https://ghe.kst3.jp/contents-create-dev/sample_python_package',
      scripts=['bin/script-sample'],
      author='Mashiyat Zaman',
      author_email='Mashiyat_Zaman@r.recruit.co.jp',
      license='RCO',
      packages=find_packages(), #['sample_python_package'] #the package itself
      install_requires=['datetime'],
      dependency_links=['https://github.com/mashiyatz/test.git'],
      setup_requires=['pytest-runner'],
      #test_suite='pytest',  #not sure how to use
      tests_require=['pytest'],  #not sure how to use
      zip_safe=False)