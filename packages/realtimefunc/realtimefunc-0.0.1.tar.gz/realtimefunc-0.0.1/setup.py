import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="realtimefunc",
    version="0.0.1",
    author="Graywd",
    author_email="nowreturnlong@gmail.com",
    description="A decorator is used to update a function at runtime.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Graywd/realtimefunc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
