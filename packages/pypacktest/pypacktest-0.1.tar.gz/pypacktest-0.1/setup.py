import setuptools 

with open("README.md", "r") as fh:
    long_description = fh.read()
	
setuptools.setup(name='pypacktest',
	version='0.1',
    description='Python Package test',
    url='https://github.com/achabrier/pypacktest',
    author='Alain Chabrier',
    author_email='alain.chabrier@ibm.com',
    long_description=long_description,
	long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
	  
	  