# -*- coding: utf-8 -*-
"""Setup file.

:copyright: (c) 2019, Serge Émond
:license: BSD 3-Clause, http://opensource.org/licenses/BSD-3-Clause

"""

from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="golden-borders",
    python_requires=">=3.3",
    author="Serge Émond",
    author_email="serge@sergeemond.com",
    zip_safe=True,
    packages=["golden_borders"],
    url="https://github.com/semond/golden-borders",
    description="Optically center the window of a print by computing the mat/print sizes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "Topic :: Utilities",
    ],
    install_requires=["click", "mpmath"],
    extras_require={
        "dev": [
            "flake8",
            "flake8-docstrings",
            "flake8-import-order",
            "flake8-bugbear",
            "black",
            "isort",
        ]
    },
    version_format="{tag}.dev{commitcount}+{gitsha}",
    setup_requires=["setuptools-git-version"],
    entry_points="""
    [console_scripts]
    golden-borders=golden_borders:main
    """,
)
