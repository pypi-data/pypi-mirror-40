import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pceuropa-test",
    version="0.0.1",
    author="Rafal Marguzewicz",
    author_email="rafal@pceuropa.net",
    description="Test utility package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pceuropa/test",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
