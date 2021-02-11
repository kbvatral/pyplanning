import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyplanning",
    version="0.1",
    author="Caleb Vatral",
    author_email="caleb.m.vatral@vanderbilt.edu",
    description="Implementation of AI Planning Algorithms in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kbvatral/pyplanning",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
