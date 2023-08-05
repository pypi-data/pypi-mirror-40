import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple_sql_formatter",
    version="1",
    author="Natan Anael",
    author_email="natan.anael@gmail.com",
    description="Simple SQL Formatter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/natansilva/sql_formatter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
