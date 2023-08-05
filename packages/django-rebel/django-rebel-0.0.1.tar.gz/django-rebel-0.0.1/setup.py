"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

try:
    from pip.req import parse_requirements
except ImportError:
    # pip >= 10
    from pip._internal.req import parse_requirements

here = path.abspath(path.dirname(__file__))


def get_requirements(requirements_file):
    """Use pip to parse requirements file."""
    requirements = []
    if path.isfile(requirements_file):
        for req in parse_requirements(requirements_file, session="hack"):
            if req.markers:
                requirements.append("%s;%s" % (req.req, req.markers))
            else:
                requirements.append("%s" % req.req)
    return requirements


if __name__ == "__main__":
    INSTALL_REQUIRES = get_requirements(path.join(here, "requirements", "requirement-main.txt"))
    TESTING_REQUIRES = get_requirements(path.join(here, "requirements", "requirement-main.txt"))

    # Get the long description from the README file
    with open(path.join(here, 'README.MD'), encoding='utf-8') as f:
        long_description = f.read()


setup(
    name='django-rebel',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.1',

    description='Mailgun Backend for Django',
    long_description=long_description,

    # The project's main homepage.
    url='https://gitlab.com/socivy/django-rebel',

    # Author details
    author='Socivy Developers',
    author_email='info@socivy.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='mail mailgun django',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=INSTALL_REQUIRES,

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'test': TESTING_REQUIRES,
    }
)
