from setuptools import setup

from pysampling.version import __version__

# ---------------------------------------------------------------------------------------------------------
# GENERAL
# ---------------------------------------------------------------------------------------------------------


__name__ = "pysampling"
__author__ = "Julian Blank"
__url__ = "https://www.egr.msu.edu/coinlab/blankjul/pysampling/"

data = dict(
    name=__name__,
    version=__version__,
    author=__author__,
    url=__url__,
    python_requires='>=3.6',
    author_email="blankjul@egr.msu.edu",
    description="Multi-Objective Optimization in Python",
    license='Apache License 2.0',
    keywords="optimization",
    install_requires=['numpy>=1.15'],
    platforms='any',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Mathematics'
    ]
)


# ---------------------------------------------------------------------------------------------------------
# OTHER METADATA
# ---------------------------------------------------------------------------------------------------------

def readme():
    with open('README.rst') as f:
        return f.read()


data['long_description'] = readme()
data['packages'] = ['pysampling', 'pysampling.algorithms', 'pysampling.resources']

# ---------------------------------------------------------------------------------------------------------
# SETUP
# ---------------------------------------------------------------------------------------------------------

setup(**data)
