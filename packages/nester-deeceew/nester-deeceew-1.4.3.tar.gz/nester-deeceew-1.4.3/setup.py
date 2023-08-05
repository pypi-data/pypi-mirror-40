import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nester-deeceew",
    version="1.4.3",
    author="Danial Williams",
    author_email="deeceew@gmail.com",
    description="A simple printer of nested lists.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://test.pypi.org/project/nester-deeceew/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
