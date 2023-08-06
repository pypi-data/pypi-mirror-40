from setuptools import setup, find_packages

setup(
    name="bidtool",
    version="0.0.1",
    description="bid tool sdk",
    packages=find_packages(),
    install_requires=[
        'pandas==0.23.4',
        'requests==2.21.0'
    ]
)
