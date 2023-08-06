import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="config-store",
    version="0.0.4",
    author="Felix ZongTing",
    author_email="gary62107@gmail.com",
    description="A python module for env variable and config file management.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZhongTing/config-store",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)