import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example_test_package",
    version="1.0.0",
    author="Bruce Zhang",
    author_email="zttt183525594@gmail.com",
    description="A example package with some pre-releases.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BruceZhang1993",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
