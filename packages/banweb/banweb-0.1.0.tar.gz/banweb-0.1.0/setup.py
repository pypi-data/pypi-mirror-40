from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='banweb',
    version='0.1.0',
    description='Interface with the banner website to access academic information',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Alex979/banweb-python',
    license='MIT',
    packages=['banweb'],
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)