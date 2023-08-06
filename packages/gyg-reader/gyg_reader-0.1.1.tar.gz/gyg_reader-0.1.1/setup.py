from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='gyg_reader',
      version='0.1.1',
      description='Retrieve booking details from GetYourGuide orders',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/sknzl/gyg_reader/',
      author='Swen Kunzel',
      author_email='swenkuenzel@gmail.com',
      license='MIT',
      packages=['gyg_reader'],
      install_requires=[
          'requests',
          'lxml',
      ],
      zip_safe=False)
