from KPHMMER import (
    __author__,
    __author_email__,
    __version__,
    __release__
)

from setuptools import setup
from setuptools import find_packages

import sys


# validation
if sys.version_info < (3, 4):
    print("Building SAMPLE_PROJECT requires at least Python 3.4 to run.")
    sys.exit(1)


def main():
    description = "KPHMMER"

    setup(
        name="KPHMMER",
        version=__version__,
        author=__author__,
        author_email=__author_email__,
        url="www.example.jp",
        description=description,
        long_description=description,
        zip_safe=False,
        include_package_data=True,
        packages=[
            "KPHMMER"
        ],
        install_requires=[],
        tests_require=[],
        setup_requires=[],
        scripts=[
            "bin/kphmmer"
        ],
        license="GNU Lesser General Public License v3 or later (LGPLv3+)",
        keywords="",
        platforms="Linux",
        classifiers=["Intended Audience :: System Administrators",
                     "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
                     "Natural Language :: Japanese",
                     "Programming Language :: Python :: 3.4",
                     ],
    )


if __name__ == "__main__":
    main()
