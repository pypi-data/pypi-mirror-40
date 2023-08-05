import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BasicTree",
    version="0.0.1",
    author="Andrew Farley",
    author_email="amf7crazy@gmail.com",
    description="A basic tree library, useful for testing different searching methods",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/And1210/BasicTree",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)