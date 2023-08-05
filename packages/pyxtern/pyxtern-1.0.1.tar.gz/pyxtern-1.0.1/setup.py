import setuptools
import os

with open("README.md", "r") as f:
    long_description = f.read()

"""if os.environ.get("CI_COMMIT_TAG"):
    version = os.environ["CI_COMMIT_TAG"]
else:
    version = os.environ["CI_JOB_ID"]"""

version = "1.0.1"

setuptools.setup(
    name="pyxtern",
    version=version,
    author="Martin Grignard",
    author_email="mar.grignard@gmail.com",
    description="A small package to run external command lines.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mar.grignard/pyxtern",
    packages=setuptools.find_packages()
)
