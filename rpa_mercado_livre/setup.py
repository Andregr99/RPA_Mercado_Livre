from setuptools import setup, find_packages

setup(
    name="rpa_mercado_livre",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'playwright',
        'pandas',
        ]
)