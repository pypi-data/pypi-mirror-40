import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wosPyFile",
    version="2.0.0",
    author="Wellington Silva",
    author_email="wellington@wosilva.com",
    description="Simple package for file reading",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WellingtonOSilva/pyFile",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)