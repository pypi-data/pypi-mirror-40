import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crossywords",
    version="0.0.5",
    author="Andrey Volkov",
    author_email="andrey@volkov.tech",
    description="Word matrix generator that creates the word matrix in a way to have multiple words in one 5x5 matrix.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AndreyVolkovBI/CrossyWords",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)