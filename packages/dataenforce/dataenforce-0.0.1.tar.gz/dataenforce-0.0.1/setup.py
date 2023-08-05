import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dataenforce",
    version="0.0.1",
    author="Cedric Canovas",
    author_email="dev@canovas.me",
    description="Enforce columns & data types of pandas DataFramese",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CedricFR/dataenforce",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
