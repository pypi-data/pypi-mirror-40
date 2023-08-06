'''
Programmer: Miles Boswell

Setup script for PYPI
'''
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='Toucan-Tools',
     version='0.4',
     scripts=['toucan'] ,
     author="Miles Boswell, Egan Johnson",
     author_email="nunyabusiness@gmail.com",
     description="A simple image processing library written in python.",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/bm20894/Image-Tools",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
