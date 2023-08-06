import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swirl_cli",
    version="0.1.2",
    author="William Naslund",
    author_email="admin@starlightconsultants.com",
    description="Provides access to SWIRL CLI projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.starlightconsultants.com/swirl/python-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
