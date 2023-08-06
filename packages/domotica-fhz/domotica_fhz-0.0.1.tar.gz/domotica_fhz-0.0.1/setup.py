"""Setup for using the FHZ 1000/FHZ 1300/FS20 components in python."""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="domotica_fhz",
    version="0.0.1",
    author="Johan Kunnen",
    author_email="domotica@kunnen.frl",
    description="""Package for using the FHZ 1000/FHZ 1300/FS20
    components in python""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/JohanKunnen/domotica_fhz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
