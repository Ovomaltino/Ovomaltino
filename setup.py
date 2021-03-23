import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Ovomaltino",
    version="1.0.0",
    author="Matheus Nobre Gomes",
    author_email="matt-gomes@live.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ovomaltino/Ovomaltino",
    packages=['ovomaltino'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
    ],
)
