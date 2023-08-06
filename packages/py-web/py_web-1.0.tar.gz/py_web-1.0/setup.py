from pathlib import Path
import setuptools

setuptools.setup(
    name="py_web",
    version=1.0,
    description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
