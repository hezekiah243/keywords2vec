import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    "gensim",
    "pandas",
    "Flask",
    "nltk",
    "unidecode",
    "fastprogress",
]

setuptools.setup(
    name='keywords2vec',
    version='0.1',
    # scripts=['keywords2vec'],
    author="Daniel Pérez Rada",
    author_email="dperezrada@gmail.com",
    description="Similar to word2vec, but with keywords",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dperezrada/keywords2vec",
    packages=["keywords2vec"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requires,
)
