import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='OAIParser',
    version='0.1',
    author="Devdutt Shenoi",
    author_email="devdutt@outlook.in",
    description="An Open API parser for hydrus by HTTP-APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/de-sh/OAIParser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
