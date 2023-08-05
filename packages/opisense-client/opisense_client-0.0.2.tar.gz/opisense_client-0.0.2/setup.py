import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="opisense_client",
    version="0.0.2",
    author="Opinum",
    author_email="support@opinum.com",
    description="Package to interract with the Opisense API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/opinum/opisense_client/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)