# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation

"""
Invoke tasks for Python development.

Copyright ©  2018 Justin Stout <justin@jstout.us>

"""
import importlib.util
import os

from invoke import task


def _get_pkg_version(ctx):
    """Extract __version__ from __init__.py."""
    path = 'src/{}/{}/__init__.py'.format(ctx.app.pkg_name, ctx.app.pkg_name)
    spec = importlib.util.spec_from_file_location(ctx.app.pkg_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    return mod.__version__


@task(help={'single-file': 'package as a single file'})
def build_binary(ctx, single_file=False):
    """Build pyinstaller binary package."""
    dist_path = 'build/bin'
    os.makedirs(dist_path)

    options = [
        '--name {}'.format(ctx.app.bin_name),
        '--specpath src/{}'.format(ctx.app.pkg_name)
        ]

    if single_file:
        options.append('--onefile')

    cmd = 'pyinstaller {} src/{}/{}/__main__.py --distpath {}'.format(' '.join(options),
                                                                      ctx.app.pkg_name,
                                                                      ctx.app.pkg_name,
                                                                      dist_path
                                                                      )
    ctx.run(cmd)


@task()
def build_wheel(ctx):
    """Build Python wheel and sdist."""
    with ctx.cd('src/{}'.format(ctx.app.pkg_name)):
        ctx.run('python3 setup.py build sdist bdist_wheel')


@task
def clean(ctx, bytecode=False, build=False, tox=False):
    """Clean package repo. Default is to clean all."""
    clean_all = True not in (bytecode, build, tox,)
    pkg_path = 'src/{}/{}'.format(ctx.app.pkg_name, ctx.app.pkg_name)

    if bytecode or clean_all:
        ctx.run('find . | grep __pycache__ | xargs rm -rf')

    if build or clean_all:
        patterns = ('build',
                    'target',
                    'dist',
                    '{}.egg-info'.format(pkg_path),
                    '{}.spec'.format(pkg_path),
                    'src/{}/build'.format(ctx.app.pkg_name),
                    'src/{}/dist'.format(ctx.app.pkg_name),
                    )

        for pattern in patterns:
            ctx.run('rm -rf {}'.format(pattern))

    if tox or clean_all:
        ctx.run('rm -rf src/{}/.tox'.format(ctx.app.pkg_name))


@task(help={'name': 'major, minor, or patch'})
def bump_version(ctx, name):
    """Bump version."""
    path = 'src/{}/{}/__init__.py'.format(ctx.app.pkg_name, ctx.app.pkg_name)
    version = _get_pkg_version(ctx)

    cmd = 'bumpversion --current-version {} {} {}'.format(version, name, path)
    ctx.run(cmd)


@task
def install(ctx):
    """Perform editable user install of module."""
    cmd = 'python3 -m pip install --user -e src/{}'.format(ctx.app.pkg_name)
    ctx.run(cmd)


@task
def test(ctx, errors=False, unit=False, integration=False, regression=False,  # pylint: disable=too-many-arguments
         lint=False, tox=False, verbose=False):
    """Run tests. Default runs all tests with all but lint executed in tox."""
    run_all = True not in (errors, unit, integration, regression, lint, tox,)

    pkg_path = 'src/{}/{}'.format(ctx.app.pkg_name, ctx.app.pkg_name)

    if errors or run_all:
        cmd = 'pylint --errors-only {}'.format(pkg_path)
        ctx.run(cmd)

    options = []

    if verbose:
        options.append('--verbose')

    pytest_cmd = 'pytest {} src/{}/'.format(' '.join(options), ctx.app.pkg_name)
    pytest_cmd += 'tests/{}'

    if unit:
        cmd = pytest_cmd.format('unit')
        ctx.run(cmd)

    if integration:
        cmd = pytest_cmd.format('integration')
        ctx.run(cmd)

    if regression:
        cmd = pytest_cmd.format('regression')
        ctx.run(cmd)

    if lint or run_all:
        cmd = 'pylint --rcfile=src/{}/pylintrc {}'.format(ctx.app.pkg_name, pkg_path)
        ctx.run(cmd)

        cmd = 'pycodestyle --max-line-length=120 {}'.format(pkg_path)
        ctx.run(cmd)

        cmd = 'pydocstyle {}'.format(pkg_path)
        ctx.run(cmd)

    if tox or run_all:

        with ctx.cd('src/{}'.format(ctx.app.pkg_name)):
            ctx.run('tox')
