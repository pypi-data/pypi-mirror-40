"""Setup configuration."""
import setuptools
from adguard.version import __version__

with open("README.md", "r") as fh:
    LONG = fh.read()
setuptools.setup(
    name="adguard",
    version=__version__,
    author="Joakim Sorensen",
    author_email="ludeeus@gmail.com",
    description="",
    long_description=LONG,
    install_requires=['aiohttp', 'async_timeout'],
    long_description_content_type="text/markdown",
    url="https://github.com/ludeeus/adguard",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
