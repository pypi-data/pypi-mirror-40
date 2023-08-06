import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tdctlauthcard",
    version="0.0.12",
    author="Bishaka Samuel",
    author_email="sbishaka@gmail.com",
    description="Auth utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teradactol/authcard.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)