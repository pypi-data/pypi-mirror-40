import sys
import os
import io
from setuptools import setup, find_packages

sys.path.insert(0, os.path.abspath('lib'))
from gitlab_caller import __prog__, __descr__, __author__, __version__


with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()


static_setup_params = dict(
    name=__prog__,
    version=__version__,
    description=__descr__,
    long_description=readme,
    author=__author__,
    python_requires='>=3.5',
    package_dir={'': 'lib'},
    packages=find_packages('lib'),
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    # Installing as zip files would break due to references to __file__
    zip_safe=False
)


def main():
    """Invoke installation process using setuptools."""
    setup(**static_setup_params)


if __name__ == '__main__':
    main()
