from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='videosplit',
    description="Utility to extract frames out of a video",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    version='0.4.1',
    author="Johan Cervantes",
    python_requires='==3.*'
)
