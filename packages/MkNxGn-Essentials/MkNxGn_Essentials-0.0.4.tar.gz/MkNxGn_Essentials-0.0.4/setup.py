import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MkNxGn_Essentials",
    version="0.0.4",
    author="Mark",
    author_email="mark@mknxgn.com",
    description="MkNxGn File Writing and Network Essentials",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mknxgn.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)