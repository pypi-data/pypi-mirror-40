"""
A proxy for installing seleniumbase dependencies and plugins
"""

from setuptools import setup, find_packages  # noqa

setup(
    name='pytest-seleniumbase',
    version='0.1.0',
    description='Reliable Browser Automation & Testing Framework',
    long_description='Reliable Browser Automation & Testing Framework',
    url='https://github.com/seleniumbase/SeleniumBase',
    platforms=["Windows", "Linux", "Unix", "Mac OS-X"],
    author='Michael Mintz',
    author_email='mdmintz@gmail.com',
    maintainer='Michael Mintz',
    license="MIT",
    install_requires=[
        'seleniumbase',
        ],
    packages=[
        ],
    entry_points={
        'nose.plugins': [
            ],
        'pytest11': [
            ]
        }
    )

print("\n*** SeleniumBase Installation Complete! ***\n")
