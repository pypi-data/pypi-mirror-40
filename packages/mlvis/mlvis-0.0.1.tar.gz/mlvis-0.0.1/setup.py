import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlvis",
    version="0.0.1",
    author="Yang Wang",
    author_email="gnavvy@gmail.com",
    description="Machine Learning Visualizations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gnavvy/mlvis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)