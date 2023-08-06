import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tree-storage",
    version="0.1.11",
    author="Valerii Duz",
    author_email="duz.valera.od@ex.ua",
    description="Tree hash-storage files",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    test_suite="tests",
    tests_require=['Pillow']
)
