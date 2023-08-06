import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="googlehomepush",
    version="0.1.0",
    author="Thomas Deblock",
    author_email="deblock.thomas.62@gmail.com",
    description="library to push text message or sond to Google Home.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deblockt/google-home-push",
    packages=setuptools.find_packages(),
    install_requires=list(val.strip() for val in open('requirements.txt')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)