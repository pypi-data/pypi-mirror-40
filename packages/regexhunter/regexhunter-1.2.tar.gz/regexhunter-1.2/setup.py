import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="regexhunter",
    version="1.2",
    author="Tom Moritz",
    author_email="tom.moritz@outlook.fr",
    description="A small package allowing you to search for regex pre-formatted for you.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SevenOfHurt/RegexHunter/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)