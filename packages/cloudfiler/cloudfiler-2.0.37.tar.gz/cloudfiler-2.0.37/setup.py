import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cloudfiler",
    version="2.0.37",
    author="Colin Wills",
    author_email="colin@nuvovis.com",
    description="An S3 file storage GUI client with pre-internet, TNO encryption.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.cloudfiler.org/",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["boto", "passlib", "keyring", "pycrypto"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
