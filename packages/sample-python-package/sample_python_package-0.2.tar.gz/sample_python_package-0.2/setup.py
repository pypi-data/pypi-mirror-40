from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='sample_python_package',
      version='0.2',
      description='Testing',
      long_description='Testing Python package creation.',
      # classifiers=[
      #     'Development Status :: 1 - Alpha',
      #     'License :: D Approved :: E License',
      #     'Programming Language :: Python :: 3.7',
      #     'Topic :: Date & Time'
      # ],
      url='https://ghe.kst3.jp/contents-create-dev/sample_python_package',
      author='Mashiyat Zaman',
      author_email='Mashiyat_Zaman@r.recruit.co.jp',
      license='RCO',
      packages=find_packages(), #['sample_python_package'] #the package itself
      install_requires=['datetime'],
      dependency_links=['https://github.com/mashiyatz/test.git'],
      zip_safe=False)