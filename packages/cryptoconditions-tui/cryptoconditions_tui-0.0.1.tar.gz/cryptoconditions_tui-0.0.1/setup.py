import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cryptoconditions_tui",
    version="0.0.1",
    author="Anton Lysakov",
    author_email="tlysakov@gmail.com",
    description="Terminal user interfaces for Komodo CryptoConditions smart-contracts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tonymorony/GatewaysCC-TUI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
