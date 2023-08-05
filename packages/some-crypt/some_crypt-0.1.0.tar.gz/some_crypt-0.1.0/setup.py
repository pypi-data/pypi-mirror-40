import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="some_crypt",
    version="0.1.0",
    author="Wes Rickey",
    author_email="d.wrickey@gmail.com",
    description="A simple (and simplistic) basic cryptography package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Grimmslaw/some_crypt.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
