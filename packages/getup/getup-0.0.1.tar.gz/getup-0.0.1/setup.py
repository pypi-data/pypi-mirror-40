import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="getup",
    version="0.0.1",
    author="Jussi Arpalahti",
    author_email="jussi.arpalahti@gmail.com",
    description="First package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/jussiarpalahti/getup",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
)
