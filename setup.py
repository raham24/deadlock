from setuptools import setup, find_packages

setup(
    name='vessel',
    version='1.0.0',
    packages=find_packages(),  # This finds 'vessel' as a package
    include_package_data=True,
    install_requires=[
        'click',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            # Point to 'cli' in 'vessel.main'
            'vessel = vessel.main:cli'
        ]
    },
)
