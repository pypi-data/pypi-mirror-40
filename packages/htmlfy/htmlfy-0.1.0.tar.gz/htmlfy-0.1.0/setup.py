import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="htmlfy",
    version="0.1.0",
    author="Alexey Schebelev",
    description="Python package for HTML minification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlexxNB/htmlfy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)