import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="signals-vulcan",
    version="1.0.1",
    description="A interface for uniform data sourcing",
    long_description=README,
    long_description_type="text/markdown",
    url="http://github.com/warrendev3190/vulcan",
    author="Warren Sadler",
    license="MIT",
    packages=find_packages(exclude=("tests",))
)
