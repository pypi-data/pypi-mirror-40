import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="persianutils",
    version="0.1.0",
    author="Iman Nazari",
    author_email="imannazari@hotmail.com",
    description="A [getting wonderfull] package to preprocess your Persian text for Search, Standardizing & NLP processes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ishto7/persianutils",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)