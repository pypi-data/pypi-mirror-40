from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()
with open("requirements.txt") as f:
	required = f.read().splitlines()

setup(
name = "zoo_animal_classification",
version="1.0.0",
description = "classification of zoo animals using machine learning models",
long_description= readme,
author = "Xinyu Zhang, Yijia Chen, Xiaochi Ge",
author_email = "mandy_zhang512@gwu.edu",
url = "https://github.com/yijiaceline/CSF-project.git",
license = "MIT",
classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
],
keywords = "decision tree, classification, multiclass, zoo, animals",
install_requires = required
)
