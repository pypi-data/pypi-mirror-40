import sys

try:
    from setuptools import setup
except ImportError:
    from distutils import setup

DEV_REQUIRES = []

#Mock is only required for Python 2
PY2 = sys.version_info[0] == 2

if PY2:
    DEV_REQUIRES.append('mock>=2.0.0')

readme = open('README.rst', 'r')
README_TEXT = readme.read()
readme.close()

setup(
    name='attotime',
    version='0.1.3',
    description='Arbitrary precision datetime library.',
    long_description=README_TEXT,
    author='Brandon Nielsen',
    author_email='nielsenb@jetfuse.net',
    url='https://bitbucket.org/nielsenb/attotime',
    extras_require={
        'dev': DEV_REQUIRES
    },
    packages=[
        'attotime',
        'attotime.objects',
        'attotime.util'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='datetime decimal',
    project_urls={
        'Source': 'https://bitbucket.org/nielsenb/attotime',
        'Tracker': 'https://bitbucket.org/nielsenb/attotime/issues'
    }
)
