import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tdctlauthcard",
    version="0.0.13",
    author="Bishaka Samuel",
    author_email="sbishaka@gmail.com",
    description="Auth utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teradactol/authcard.py",
    packages=setuptools.find_packages(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    install_requires=[
          'python-jose[cryptography]',
          'bcrypt'      
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)