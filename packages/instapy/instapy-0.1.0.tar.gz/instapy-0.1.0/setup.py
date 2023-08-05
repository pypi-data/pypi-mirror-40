"""
A setuptools based setup module
See:
    https://packaging.python.org/en/latest/distributing.html
    https://github.com/pypa/sampleproject
"""

# always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import and use built-in open()
from io import open as io_open


# VERIFY ME
__version__ = "0.1.0"
__author__ = "Tim Grossmann"

# UPDATE ME
description = "Instagram Like, Comment and Follow Automation Script"
project_homepage = "https://github.com/timgrossmann/InstaPy"

# load requirements.txt
with open("requirements.txt") as f:
    dependencies = f.read().splitlines()

# load README.md
here = path.abspath(path.dirname(__file__))
with io_open(path.join(here, "README.md"), encoding="utf-8") as doc_file:
    documentation = ('\n' + doc_file.read())


setup(
    # There are some restrictions on what makes a valid project name
    # specification here:
    # https://packaging.python.org/specifications/core-metadata/#name
    name="instapy",
    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    #
    # For a discussion on single-sourcing the version across setup.py and the
    # project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,
    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#summary
    description=description,
    # This is an optional longer description of your project that represents
    # the body of text which users will see when they visit PyPI.
    #
    # Often, this is the same as your README, so you can just read it in from
    # that file directly (as we have already done above)
    # This field corresponds to the "Description" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=documentation,
    long_description_content_type="text/markdown",
    author=__author__,
    author_email='contact.timgrossmann@gmail.com',
    maintainer="InstaPy Community at Github",
    url=project_homepage,
    download_url=project_homepage+"/archive/master.zip",
    project_urls={
        "How Tos": project_homepage+"/tree/master/docs",
        "Examples": project_homepage+"/tree/master/quickstart_templates",
        "Bug Reports": project_homepage+"/issues",
        "Funding": "https://www.paypal.me/supportInstaPy",
        "Say Thanks!": "http://saythanks.io/to/uluQulu",
        "Source": project_homepage
    },
    # what to exclude? hmm
    packages=["instapy"],
    # include_package_data=True,
    # package_dir={'': "instapy"},
    package_data={
        # '': ["*.md", "*.ico", "*.png", "*.icns"],
        "instapy": ["../icons/*.*"]
    },
    license="GPLv3",
    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    # Note that this is a string of words separated by whitespace, not a list.
    keywords=("python, instagram, automation, promotion",
              "marketing, instapy, bot, selenium"
              ),
    # list of classifiers: https://pypi.org/classifiers/
    classifiers=["Development Status :: 5 - Production/Stable",
                 "Environment :: Console",
                 "Environment :: Win32 (MS Windows)",
                 "Environment :: MacOS X",
                 "Environment :: Web Environment",
                 "Intended Audience :: End Users/Desktop",
                 "Intended Audience :: Developers",
                 "Operating System :: Microsoft :: Windows",
                 "Operating System :: POSIX :: Linux",
                 "Operating System :: MacOS :: MacOS X",
                 "Operating System :: Unix",
                 "Programming Language :: Python",
                 "Programming Language :: JavaScript",
                 "Programming Language :: SQL",
                 "Topic :: Utilities",
                 "Topic :: Software Development :: Build Tools",
                 "Natural Language :: English",
                 "Programming Language :: Python :: 2",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.4",
                 "Programming Language :: Python :: 3.5",
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7"
                 ],
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=dependencies,
    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install instapy[test]
    extras_require={"test": ["pytest", "tox"]},
    python_requires=">=2.7",
    platforms=["win32", "linux", "linux2", "darwin"],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={
        "console_scripts": []
    }
)



