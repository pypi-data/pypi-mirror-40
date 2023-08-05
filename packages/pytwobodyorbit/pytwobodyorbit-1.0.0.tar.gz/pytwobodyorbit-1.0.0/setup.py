import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytwobodyorbit",
    license="MIT",
    version="1.0.0",
    author="whiskie14142",
    author_email="whiskie14142@gmail.com",
    description="A module that provides various computations about two-body orbits",
    keywords="two-body orbit Keplerian Cartesian Lambert",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/whiskie14142/pytwobodyorbit",
    py_modules=["pytwobodyorbit"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)