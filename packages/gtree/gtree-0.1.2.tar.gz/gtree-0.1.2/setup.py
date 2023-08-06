import setuptools
import gtree

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gtree",
    version=gtree.version,
    description="A general tree implementation and provides convinient methods for defining trees in JSON or YAML files.",
    long_description=long_description,
    url="https://github.com/lunjon/gtree",
    author="Jonathan Lundholm",
    author_email="jon.lundholm@gmail.com",
    license="MIT",
    packages=["gtree"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)