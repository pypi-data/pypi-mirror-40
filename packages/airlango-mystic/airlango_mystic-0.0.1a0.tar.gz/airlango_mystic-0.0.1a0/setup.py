
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="airlango_mystic",
    version="0.0.1a",
    author="Airlango Tech Support",
    author_email="it@airlango.com",
    description="This python package provides abilities to control Airlango drone - Mystic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://airlango.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)