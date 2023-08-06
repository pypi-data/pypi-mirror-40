import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SimpleVN",
    version="0.0.5",
    author="Menthol - Derek Zhang",
    author_email="derek.zhang0210@gmail.com",
    description="A simple module to create really quick visual novels",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/D3REKZHANG/SimpleVN",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)