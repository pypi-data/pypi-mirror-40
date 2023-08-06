import os
from setuptools import setup

requirements = [
    "grpcio",
    "protobuf",
    "sense-core>=0.0.18"
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sense-text-extractor',
    version='0.0.1',
    packages=[
            "sense_text_extractor",
    ],
    license='BSD License',  # example license
    description='sense_text_extractor',
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    author='kafka0102',
    author_email='yujianjia@sensedeal.ai',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)