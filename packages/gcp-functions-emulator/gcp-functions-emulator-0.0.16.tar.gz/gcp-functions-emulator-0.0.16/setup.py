from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    install_requires=['Flask'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['gcpfemu'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
