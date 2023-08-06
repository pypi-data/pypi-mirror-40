import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RatingCF",
    version="0.1.1",
    author="Tianjian Yang",
    author_email="kaversoniano@gmail.com",
    description="Collaborative Filtering for Rating-Based Recommender System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kaversoniano/Python-package-RatingCF",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)