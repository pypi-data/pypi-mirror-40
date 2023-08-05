from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='svalbard',
      version='0.1',
      description='Easy time handling in the context of weather forecasting',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/paulskeie/svalbard',
      author='Paul Skeie',
      author_email='paul.skeie@gmail.com',
      license='Apache-2.0',
      packages=['svalbard'],
      zip_safe=False)