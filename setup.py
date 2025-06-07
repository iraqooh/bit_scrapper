from setuptools import setup, find_packages

with open('requirements.txt', encoding='utf-16') as f:
    requirements = [line.strip() for line in f if line.strip()]

setup(
    name='bit_scrapper',
    packages=find_packages(),
    install_requires=requirements,
)