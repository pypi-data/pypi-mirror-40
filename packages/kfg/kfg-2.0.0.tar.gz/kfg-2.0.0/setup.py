import io
import os
from setuptools import setup, find_packages


def local_file(*name):
    return os.path.join(
        os.path.dirname(__file__),
        *name)


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def read_version():
    """Read the `(version-string, version-info)` from
    `src/kfg/version.py`.
    """

    version_file = local_file(
        'src', 'kfg', 'version.py')
    local_vars = {}
    with open(version_file) as handle:
        exec(handle.read(), {}, local_vars)  # pylint: disable=exec-used
    return (local_vars['__version__'], local_vars['__version_info__'])


long_description = read(local_file('README.rst'), mode='rt')

setup(
    name='kfg',
    version=read_version()[0],
    packages=find_packages('src'),

    author='Austin Bingham',
    author_email='austin@sixty-north.com',
    description='A configuration library for Python',
    license='MIT',
    keywords='',
    url='http://github.com/abingham/kfg',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
    ],
    platforms='any',
    include_package_data=True,
    package_dir={'': 'src'},
    # package_data={'kfg': . . .},
    install_requires=[
        'pyyaml',
    ],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax, for
    # example: $ pip install -e .[dev,test]
    extras_require={
        # 'dev': ['check-manifest', 'wheel'],
        # 'doc': ['sphinx', 'cartouche'],
        'test': ['hypothesis', 'pytest', 'tox'],
    },
    entry_points={
        # 'console_scripts': [
        #    'kfg = kfg.cli:main',
        # ],
    },
    long_description=long_description,
)
