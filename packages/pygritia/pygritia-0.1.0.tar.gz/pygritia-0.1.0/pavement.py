"""Pavement for Pygritia"""
import shlex
import sys
import paver.doctools  # pylint: disable=unused-import
import paver.virtual  # pylint: disable=unused-import
from paver.easy import *  # pylint: disable=unused-wildcard-import,wildcard-import
from paver.options import Bunch
from paver.path import path
from paver.setuputils import setup
from setuptools import find_packages  # type: ignore

if sys.version_info < (3, 7):
    sys.exit("Pygritia requires Python >= 3.7")

options = environment.options  # pylint: disable=invalid-name

HERE = path(__file__).dirname().abspath()

setup_params = dict(  # pylint: disable=invalid-name
    name="pygritia",
    version="0.1.0",
    description="Pygritia: Lazy Symbolic Evaluation",
    long_description=open(HERE / 'README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gwangyi/pygritia",
    author="Sungkwang Lee",
    author_email="gwangyi.kr@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
)

options(
    minilib=Bunch(
        extra_files=['doctools'],
        versioned_name=False,
        extra_packages=[],
    ),
    sphinx=Bunch(
        docroot='sphinx',
        builddir='build',
        sourcedir='source',

        apidoc_opts=['-e'],
    ),
)


setup(**setup_params)


@task
@no_help
def env():
    """Ready env"""
    import os

    def pathify(key, *args):
        paths = os.environ.get(key, '').split(os.path.pathsep)
        os.environ[key] = os.path.pathsep.join(list(args) + paths)

    pathify('MYPYPATH', HERE)
    pathify('PYTHONPATH', HERE, *sys.path)


@task
@needs(['env'])
def test():
    """Run unittest"""
    try:
        import pytest  # type: ignore
    except ImportError:
        raise BuildFailure('install pytest to test')

    pytestopts = ['--cov=' + setup_params['name'], '--cov-report=html', '--cov-report=term']
    dry('pytest {}'.format(' '.join(pytestopts)), pytest.main, pytestopts)


@task
@needs(['env'])
def typecheck():
    """Run mypy"""
    try:
        import mypy.main
    except ImportError:
        raise BuildFailure('install mypy to typecheck')

    mypyopts = ['--strict', '-p', setup_params['name']]
    dry('mypy {}'.format(' '.join(mypyopts)), mypy.main.main, None, mypyopts)


@task
@needs(['env'])
def lint():
    """Run mypy and pylint"""
    try:
        import pylint.lint # type: ignore
    except ImportError:
        raise BuildFailure('install pylint to lint')

    pylintopts = ['pavement.py', 'paverlib', setup_params['name']]
    dry('pylint {}'.format(' '.join(pylintopts)), pylint.lint.Run, pylintopts)


@task
@needs(['env'])
@consume_args
def shell(args):
    """Run shell"""
    import os
    sh(' '.join(shlex.quote(arg) for arg in args)
       if args else os.environ.get('SHELL', '/bin/bash'))


@task
@needs(['env'])
def nvim():
    """Launch neovim with env"""
    import os
    os.environ['BULLETTRAIN_VIRTUALENV_PREFIX'] = 'py'
    sh('nvim "+bot sp +terminal" +NERDTreeToggle')


@task
@needs(['paverlib.doctools.apidoc', 'paverlib.doctools.html'])
def html():
    """Override html task to copy result to 'docs' directory"""
    import shutil
    try:
        shutil.rmtree(HERE / 'docs')
    except FileNotFoundError:
        pass
    shutil.copytree(
        HERE /
        options.sphinx.docroot /
        options.sphinx.builddir /
        'html',
        HERE /
        'docs')

@task
@needs('generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""
