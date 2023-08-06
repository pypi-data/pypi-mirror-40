import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="igrepper",
    version="0.0.1",
    author="Gustav Larsson",
    author_email="gustav.e.larsson@gmail.com",
    description="Interactive grepper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/igoyak/igrepper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
