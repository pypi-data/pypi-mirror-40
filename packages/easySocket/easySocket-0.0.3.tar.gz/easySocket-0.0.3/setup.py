import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easySocket",
    version="0.0.3",
    author="N-Ziermann",
    author_email="N-Ziermann@protonmail.com",
    description="A tool, based on socket, to make sending big files(like images) easier/simpler.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/N-Ziermann/easySocket",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
