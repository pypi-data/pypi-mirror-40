import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
   name='bigmpi4py',
   version='1.2.1',
   description='BigMPI4py: Python module for parallelization of Big Data objects',
   long_description=long_description,
   license="LICENSE",
   author='Alex M. Ascension',
   author_email='alexmascension@gmail.com',
   url="https://gitlab.com/alexmascension/bigmpi4py",
   install_requires=[], #external packages as dependencies
   packages=setuptools.find_packages(),
   classifiers=[

      "Programming Language :: Python :: 3",

      "License :: OSI Approved :: MIT License",

      "Operating System :: OS Independent",

   ],
) 
