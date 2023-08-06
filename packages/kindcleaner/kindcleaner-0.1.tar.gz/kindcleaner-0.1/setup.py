import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='kindcleaner',
    version='0.1',
    author="innlouvate",
    author_email="franklin@thoughtworks.com",
    description="Data cleaning package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/innlouvate/kindcleaner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
