import setuptools
import re

#with open("README.md", "r") as fh:
#    long_description = fh.read()


setuptools.setup(
    name='clinphen',
    version='1.24',
    scripts=['clinphen'],
    author="Cole A. Deisseroth",
    author_email="cdeisser@stanford.edu",
    description="An automatic phenotype extractor",
    long_description='ClinPhen is a free-to-use tool that automatically extracts phenotypes from clinical notes.',
    long_description_content_type="text/markdown",
    url="http://bejerano.stanford.edu/clinphen/",
    packages=setuptools.find_packages() + ['clinphen_src'],
    include_package_data=True,
    install_requires=['nltk', 'six'],
     classifiers=[
         "Programming Language :: Python :: 2.7",
         "Operating System :: OS Independent",
     ],
 )

