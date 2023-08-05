# setup.py
from setuptools import setup

setup(
    name="rocket_moea",
    version="0.1",
    description="A framework to develop evolutionary algorithms",
    #url="http://github.com/storborg/funniest",
    author="Auraham Camacho",
    author_email="auraham.cg@gmail.com",
    license="MIT",
    packages=["rocket_moea", "rocket_moea.fronts", "rocket_moea.helpers"],
    #zip_safe=False
    )
