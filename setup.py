from setuptools import setup, find_packages

requires = ["click", "attrs"]

dev_requires = ["bump2version", "pytest", "pytest-sugar"]

setup(
    name="tic-tac-toe",
    version="0.1.0",
    description="Backend for Tic-Tac-Toe.",
    author="Tobias Knuth",
    packages=find_packages(),
    install_requires=requires,
    extras_require={"dev": dev_requires},
)
