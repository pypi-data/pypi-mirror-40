import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="recollect_waste",
    version="1.0.0",
    author="stealthhacker",
    description="Python 3 API for Recollect Waste to track waste pickup and types.",
    long_description="Refer to Github for a full description.",
    url="https://github.com/stealthhacker/python-recollect-waste",
    packages=['recollect_waste'],
    install_requires=['requests>=2.21.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)