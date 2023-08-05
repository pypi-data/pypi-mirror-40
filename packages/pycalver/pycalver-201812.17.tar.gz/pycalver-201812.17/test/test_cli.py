import os
import io
import time
import shutil
import pathlib2 as pl
import subprocess as sp

import pytest

from click.testing import CliRunner

import pycalver.config as config
import pycalver.version as version
import pycalver.__main__ as pycalver


SETUP_CFG_FIXTURE = """
[metadata]
license_file = LICENSE

[bdist_wheel]
universal = 1
"""

PYCALVER_TOML_FIXTURE = """
"""

PYPROJECT_TOML_FIXTURE = """
[build-system]
requires = ["setuptools", "wheel"]
"""

ENV = {
    'GIT_AUTHOR_NAME'    : "pycalver_tester",
    'GIT_COMMITTER_NAME' : "pycalver_tester",
    'GIT_AUTHOR_EMAIL'   : "pycalver_tester@nowhere.com",
    'GIT_COMMITTER_EMAIL': "pycalver_tester@nowhere.com",
    'HGUSER'             : "pycalver_tester",
}


def sh(*cmd):
    return sp.check_output(cmd, env=ENV)


@pytest.fixture
def runner(tmpdir):
    runner   = CliRunner(env=ENV)
    orig_cwd = os.getcwd()

    _debug = 0
    if _debug:
        tmpdir = pl.Path("..") / "tmp_test_pycalver_project"
        if tmpdir.exists():
            time.sleep(0.2)
            shutil.rmtree(str(tmpdir))
        tmpdir.mkdir()

    os.chdir(str(tmpdir))

    yield runner

    os.chdir(orig_cwd)

    if not _debug:
        shutil.rmtree(str(tmpdir))


def test_help(runner):
    result = runner.invoke(pycalver.cli, ['--help', "--verbose"])
    assert result.exit_code == 0
    assert "PyCalVer" in result.output
    assert "bump " in result.output
    assert "test " in result.output
    assert "init " in result.output
    assert "show " in result.output


def test_version(runner):
    result = runner.invoke(pycalver.cli, ['--version', "--verbose"])
    assert result.exit_code == 0
    assert " version v20" in result.output
    match = version.PYCALVER_RE.search(result.output)
    assert match


def test_incr(runner):
    old_version     = "v201701.0999-alpha"
    initial_version = config._initial_version()

    result = runner.invoke(pycalver.cli, ['test', old_version, "--verbose"])
    assert result.exit_code == 0
    new_version = initial_version.replace(".0001-alpha", ".11000-alpha")
    assert f"PyCalVer Version: {new_version}\n" in result.output


def test_incr_to_beta(runner):
    old_version     = "v201701.0999-alpha"
    initial_version = config._initial_version()

    result = runner.invoke(pycalver.cli, ['test', old_version, "--verbose", "--release", "beta"])
    assert result.exit_code == 0
    new_version = initial_version.replace(".0001-alpha", ".11000-beta")
    assert f"PyCalVer Version: {new_version}\n" in result.output


def test_incr_to_final(runner):
    old_version     = "v201701.0999-alpha"
    initial_version = config._initial_version()

    result = runner.invoke(pycalver.cli, ['test', old_version, "--verbose", "--release", "final"])
    assert result.exit_code == 0
    new_version = initial_version.replace(".0001-alpha", ".11000")
    assert f"PyCalVer Version: {new_version}\n" in result.output


def test_incr_invalid(runner, caplog):
    old_version = "v201701.0999-alpha"

    result = runner.invoke(pycalver.cli, ['test', old_version, "--verbose", "--release", "alfa"])
    assert result.exit_code == 1


def _add_project_files(*files):
    if "README.md" in files:
        with io.open("README.md", mode="wt", encoding="utf-8") as fh:
            fh.write("Hello World v201701.0002-alpha !\n")

    if "setup.cfg" in files:
        with io.open("setup.cfg", mode="wt", encoding="utf-8") as fh:
            fh.write(SETUP_CFG_FIXTURE)

    if "pycalver.toml" in files:
        with io.open("pycalver.toml", mode="wt", encoding="utf-8") as fh:
            fh.write(PYCALVER_TOML_FIXTURE)

    if "pyproject.toml" in files:
        with io.open("pyproject.toml", mode="wt", encoding="utf-8") as fh:
            fh.write(PYPROJECT_TOML_FIXTURE)


def test_nocfg(runner, caplog):
    _add_project_files("README.md")
    result = runner.invoke(pycalver.cli, ['show', "--verbose"])
    assert result.exit_code == 1
    assert any(
        bool("Could not parse configuration. Perhaps try 'pycalver init'." in r.message)
        for r in caplog.records
    )


def test_novcs_nocfg_init(runner):
    _add_project_files("README.md")
    result = runner.invoke(pycalver.cli, ['init', "--verbose"])
    assert result.exit_code == 0

    with io.open("pycalver.toml", mode="r", encoding="utf-8") as fh:
        cfg_content = fh.read()

    base_str = config.DEFAULT_TOML_BASE_TMPL.format(initial_version=config._initial_version())
    assert base_str                          in cfg_content
    assert config.DEFAULT_TOML_README_MD_STR in cfg_content

    result = runner.invoke(pycalver.cli, ['show', "--verbose"])
    assert result.exit_code == 0
    assert f"Current Version: {config._initial_version()}\n" in result.output
    assert f"PEP440 Version : {config._initial_version_pep440()}\n" in result.output


def test_novcs_setupcfg_init(runner):
    _add_project_files("README.md", "setup.cfg")
    result = runner.invoke(pycalver.cli, ['init', "--verbose"])
    assert result.exit_code == 0

    with io.open("setup.cfg", mode="r", encoding="utf-8") as fh:
        cfg_content = fh.read()

    base_str = config.DEFAULT_CONFIGPARSER_BASE_TMPL.format(
        initial_version=config._initial_version()
    )
    assert base_str                                  in cfg_content
    assert config.DEFAULT_CONFIGPARSER_README_MD_STR in cfg_content

    result = runner.invoke(pycalver.cli, ['show', "--verbose"])
    assert result.exit_code == 0
    assert f"Current Version: {config._initial_version()}\n" in result.output
    assert f"PEP440 Version : {config._initial_version_pep440()}\n" in result.output


def test_novcs_pyproject_init(runner):
    _add_project_files("README.md", "pyproject.toml")
    result = runner.invoke(pycalver.cli, ['init', "--verbose"])
    assert result.exit_code == 0

    with io.open("pyproject.toml", mode="r", encoding="utf-8") as fh:
        cfg_content = fh.read()

    base_str = config.DEFAULT_TOML_BASE_TMPL.format(initial_version=config._initial_version())
    assert base_str                          in cfg_content
    assert config.DEFAULT_TOML_README_MD_STR in cfg_content

    result = runner.invoke(pycalver.cli, ['show'])
    assert result.exit_code == 0
    assert f"Current Version: {config._initial_version()}\n" in result.output
    assert f"PEP440 Version : {config._initial_version_pep440()}\n" in result.output


def _vcs_init(vcs):
    assert not pl.Path(f".{vcs}").exists()
    sh(f"{vcs}", "init")
    assert pl.Path(f".{vcs}").is_dir()

    sh(f"{vcs}", "add", "README.md")
    sh(f"{vcs}", "commit", "-m", "initial commit")


def test_git_init(runner):
    _add_project_files("README.md")
    _vcs_init("git")

    result = runner.invoke(pycalver.cli, ['init', "--verbose"])
    assert result.exit_code == 0

    result = runner.invoke(pycalver.cli, ['show'])
    assert result.exit_code == 0
    assert f"Current Version: {config._initial_version()}\n" in result.output
    assert f"PEP440 Version : {config._initial_version_pep440()}\n" in result.output


def test_hg_init(runner):
    _add_project_files("README.md")
    _vcs_init("hg")

    result = runner.invoke(pycalver.cli, ['init', "--verbose"])
    assert result.exit_code == 0

    result = runner.invoke(pycalver.cli, ['show'])
    assert result.exit_code == 0
    assert f"Current Version: {config._initial_version()}\n" in result.output
    assert f"PEP440 Version : {config._initial_version_pep440()}\n" in result.output


def test_git_tag_eval(runner):
    _add_project_files("README.md")
    _vcs_init("git")

    # This will set a version that is older than the version tag
    # we set in the vcs, which should take precedence.
    result = runner.invoke(pycalver.cli, ['init', "--verbose"])
    assert result.exit_code == 0
    initial_version    = config._initial_version()
    tag_version        = initial_version.replace(".0001-alpha", ".0123-beta")
    tag_version_pep440 = tag_version[1:7] + ".123b0"

    sh("git", "tag", "--annotate", tag_version, "--message", f"bump version to {tag_version}")

    result = runner.invoke(pycalver.cli, ['show', "--verbose"])
    assert result.exit_code == 0
    assert f"Current Version: {tag_version}\n" in result.output
    assert f"PEP440 Version : {tag_version_pep440}\n" in result.output


def test_hg_tag_eval(runner):
    _add_project_files("README.md")
    _vcs_init("hg")

    # This will set a version that is older than the version tag
    # we set in the vcs, which should take precedence.
    result = runner.invoke(pycalver.cli, ['init', "--verbose"])
    assert result.exit_code == 0
    initial_version    = config._initial_version()
    tag_version        = initial_version.replace(".0001-alpha", ".0123-beta")
    tag_version_pep440 = tag_version[1:7] + ".123b0"

    sh("hg", "tag", tag_version, "--message", f"bump version to {tag_version}")

    result = runner.invoke(pycalver.cli, ['show', "--verbose"])
    assert result.exit_code == 0
    assert f"Current Version: {tag_version}\n" in result.output
    assert f"PEP440 Version : {tag_version_pep440}\n" in result.output


def test_novcs_bump(runner):
    _add_project_files("README.md")

    result = runner.invoke(pycalver.cli, ['init', "--verbose"])
    assert result.exit_code == 0

    result = runner.invoke(pycalver.cli, ['bump', "--verbose"])
    assert result.exit_code == 0

    calver = config._initial_version()[:7]

    with io.open("README.md") as fh:
        content = fh.read()
        assert calver + ".0002-alpha !\n" in content

    result = runner.invoke(pycalver.cli, ['bump', "--verbose", "--release", "beta"])
    assert result.exit_code == 0

    with io.open("README.md") as fh:
        content = fh.read()
        assert calver + ".0003-beta !\n" in content


def test_git_bump(runner):
    _add_project_files("README.md")
    _vcs_init("git")

    result = runner.invoke(pycalver.cli, ['init', "--verbose"])
    assert result.exit_code == 0

    result = runner.invoke(pycalver.cli, ['bump', "--verbose"])
    assert result.exit_code == 0

    calver = config._initial_version()[:7]

    with io.open("README.md") as fh:
        content = fh.read()
        assert calver + ".0002-alpha !\n" in content


def test_hg_bump(runner):
    _add_project_files("README.md")
    _vcs_init("hg")

    result = runner.invoke(pycalver.cli, ['init', "--verbose"])
    assert result.exit_code == 0

    result = runner.invoke(pycalver.cli, ['bump', "--verbose"])
    assert result.exit_code == 0

    calver = config._initial_version()[:7]

    with io.open("README.md") as fh:
        content = fh.read()
        assert calver + ".0002-alpha !\n" in content
