from setuptools import setup

with open("README.md", 'r') as fh:
    long_description = fh.read()

setup (
    name="ecoclib",
    version="0.0.7",
    description="Error Correcting Output code with flexibile learning methods for multi-class classification",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pkgprateek/ecoclib",
    author="Prateek Kumar Goel",
    author_email="pkgprateek@gmail.com",
    install_requires=["numpy", "scikit-learn"],
    py_modules=["ecoclib"],
    package_dir={'' : 'src'},
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ]
)