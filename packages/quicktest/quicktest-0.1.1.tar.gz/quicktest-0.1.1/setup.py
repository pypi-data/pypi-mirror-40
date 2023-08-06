import os.path
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as readme:
    README = readme.read()

setup(
    name="quicktest",
    version="0.1.1",
    description="Easily test pure functions.",
    long_description=README,
    url="https://github.com/mlevesquedion/quicktest",
    author="Michaël Lévesque-Dion",
    author_email="mlevesquedion@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["quicktest"],
    include_package_data=True,
    install_requires=[
        'clirainbow',
    ],
)
