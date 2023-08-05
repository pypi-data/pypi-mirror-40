import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="token_utf8",
    version="1.0",
    author="Joseph wondarash, Naol Berhanu",
    author_email="naolberhanu6@gmail.com",
    description="utf8 csv word frequency analyzer",
    long_description=['re','operator','csv'],
    long_description_content_type="text/markdown",
    url="https://github.com/nolla123/char_utf8",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

