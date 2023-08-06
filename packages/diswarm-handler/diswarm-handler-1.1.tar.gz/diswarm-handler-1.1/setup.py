import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="diswarm-handler",
    version="1.1",
    author="iTecX",
    author_email="matteovh@gmail.com",
    description="Handler for DiSwarm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iTecAI/DiSwarm/tree/master/diswarm-handler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['DiSwarm'],
)
