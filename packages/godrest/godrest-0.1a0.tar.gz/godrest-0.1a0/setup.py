"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject

"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as fh:
    long_description = fh.read()


setup(
    name='godrest',  # Required
    version='0.1a',  # Required
    description='',  # Required
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bukowa/godrest",
    author='Mateusz Kurowski',  # Optional
    license='MIT License',
    package_dir={'': 'src'},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages('src'),  # Required
    # test_suite='',
    install_requires=[
    ],
)