from setuptools import setup, find_packages


with open("README.rst") as f:
    README = f.read()

setup(
    name="pimple",
    version="0.1.1",
    description="Summarize your unit tests",
    long_description=README,
    author="Samuel Searles-Bryant",
    author_email="devel@samueljsb.co.uk",
    url="https://github.com/samueljsb/pimple",
    packages=find_packages(exclude=("tests", "docs")),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
    ],
)
