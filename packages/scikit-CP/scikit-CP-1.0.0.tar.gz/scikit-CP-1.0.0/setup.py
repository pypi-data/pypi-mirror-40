import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scikit-CP",
    version="1.0.0",
    author="Nawaf Abdullah",
    author_email="nawaf97k@gmail.com",
    description="Computational physics simulation and modeling python scientific library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MentalN/scikit-CP",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
