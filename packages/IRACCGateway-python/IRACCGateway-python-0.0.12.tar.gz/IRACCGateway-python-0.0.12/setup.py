import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="IRACCGateway-python",
    version="0.0.12",
    author="yangziy",
    author_email="yangziy@outlook.com",
    description="Driver for IRACCGateway(Daikin Specified Version)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yangziy/IRACCGateway-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)