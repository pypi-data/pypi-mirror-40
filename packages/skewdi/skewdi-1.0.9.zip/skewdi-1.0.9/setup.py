
from setuptools import setup
import os.path


HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()


setup(
    name="skewdi",
    version="1.0.9",
    description="Fetch Website Content",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Sam",
    author_email="samprits5@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["skewdi"],
    include_package_data=True,
    install_requires=[
        "requests", "bs4"
    ],
)