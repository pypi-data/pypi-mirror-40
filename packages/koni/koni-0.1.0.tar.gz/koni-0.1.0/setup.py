# pylint: disable=C0111
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()


setup(
    name="koni",
    version="0.1.0",
    author="Markus Ecker",
    author_email="markus.ecker@gmail.com",
    description="Koni Machine Learning Environment",
    license="MIT",
    keywords="ai deep learning",
    url="http://github.com/koni-ml/koni",
    packages=find_packages(),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    include_package_data=True,
    install_requires=[],
    entry_points="""
    [console_scripts]
    koni = koni.__main__:main
    """
)
