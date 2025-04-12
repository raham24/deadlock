from setuptools import setup, find_packages

setup(
    name="vessel",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click==8.1.8",
        "colorama==0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "vessel=vessel.cli:cli",
        ],
    },
)