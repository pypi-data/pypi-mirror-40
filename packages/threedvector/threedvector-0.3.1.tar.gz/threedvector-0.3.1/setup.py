import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="threedvector",
    version="0.3.1",
    author="Paul Nel",
    author_email="gpaul.nel@gmail.com",
    description="A package to work with 3D vectors in Spherical and Cartesian coordinates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/gpaul.nel/threedvector",
    packages=setuptools.find_packages(exclude=["UnitTests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
