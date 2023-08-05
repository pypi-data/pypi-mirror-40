#!/usr/bin/env python
# This file is part of the pycalver project
# https://gitlab.com/mbarkhau/pycalver
#
# Copyright (c) 2018 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
"""
CLI module for PyCalVer.

Provided subcommands: show, test, init, bump
"""

import sys
import click
import logging
import typing as typ

from . import vcs
from . import parse
from . import config
from . import version
from . import rewrite


_VERBOSE = 0


try:
    import backtrace

    # To enable pretty tracebacks:
    #   echo "export ENABLE_BACKTRACE=1;" >> ~/.bashrc
    backtrace.hook(align=True, strip_path=True, enable_on_envvar_only=True)
except ImportError:
    pass


click.disable_unicode_literals_warning = True


log = logging.getLogger("pycalver.cli")


def _init_logging(verbose: int = 0) -> None:
    if verbose >= 2:
        log_format = "%(asctime)s.%(msecs)03d %(levelname)-7s %(name)-15s - %(message)s"
        log_level  = logging.DEBUG
    elif verbose == 1:
        log_format = "%(levelname)-7s - %(message)s"
        log_level  = logging.INFO
    else:
        log_format = "%(levelname)-7s - %(message)s"
        log_level  = logging.INFO

    logging.basicConfig(level=log_level, format=log_format, datefmt="%Y-%m-%dT%H:%M:%S")
    log.debug("Logging initialized.")


def _validate_release_tag(release: str) -> None:
    if release == 'final' or release in parse.VALID_RELEASE_VALUES:
        return

    log.error(f"Invalid argument --release={release}")
    log.error(f"Valid arguments are: final, {', '.join(parse.VALID_RELEASE_VALUES)}")
    sys.exit(1)


@click.group()
@click.version_option(version="v201812.0017")
@click.help_option()
@click.option('-v', '--verbose', count=True, help="Control log level. -vv for debug level.")
def cli(verbose: int = 0):
    """Automatically update PyCalVer version strings on python projects."""
    global _VERBOSE
    _VERBOSE = verbose


@cli.command()
@click.argument("old_version")
@click.option('-v', '--verbose', count=True, help="Control log level. -vv for debug level.")
@click.option(
    "--release", default=None, metavar="<name>", help="Override release name of current_version"
)
def test(old_version: str, verbose: int = 0, release: str = None) -> None:
    """Increment a version number for demo purposes."""
    _init_logging(verbose=max(_VERBOSE, verbose))

    if release:
        _validate_release_tag(release)

    new_version    = version.incr(old_version, release=release)
    pep440_version = version.pycalver_to_pep440(new_version)

    print("PyCalVer Version:", new_version)
    print("PEP440 Version  :", pep440_version)


def _update_cfg_from_vcs(cfg: config.Config, fetch: bool) -> config.Config:
    try:
        _vcs = vcs.get_vcs()
        log.debug(f"vcs found: {_vcs.name}")
        if fetch:
            log.info(f"fetching tags from remote (to turn off use: -n / --no-fetch)")
            _vcs.fetch()

        version_tags = [tag for tag in _vcs.ls_tags() if version.PYCALVER_RE.match(tag)]
        if version_tags:
            version_tags.sort(reverse=True)
            log.debug(f"found {len(version_tags)} tags: {version_tags[:2]}")
            latest_version_tag    = version_tags[0]
            latest_version_pep440 = version.pycalver_to_pep440(latest_version_tag)
            if latest_version_tag > cfg.current_version:
                log.info(f"Working dir version        : {cfg.current_version}")
                log.info(f"Latest version from {_vcs.name:>3} tag: {latest_version_tag}")
                cfg = cfg._replace(
                    current_version=latest_version_tag, pep440_version=latest_version_pep440
                )

        else:
            log.debug("no vcs tags found")
    except OSError:
        log.debug("No vcs found")

    return cfg


@cli.command()
@click.option('-v', '--verbose', count=True, help="Control log level. -vv for debug level.")
@click.option(
    "-f/-n", "--fetch/--no-fetch", is_flag=True, default=True, help="Sync tags from remote origin."
)
def show(verbose: int = 0, fetch: bool = True) -> None:
    """Show current version."""
    _init_logging(verbose=max(_VERBOSE, verbose))

    ctx: config.ProjectContext = config.init_project_ctx(project_path=".")
    cfg: config.MaybeConfig    = config.parse(ctx)

    if cfg is None:
        log.error("Could not parse configuration. Perhaps try 'pycalver init'.")
        sys.exit(1)

    cfg = _update_cfg_from_vcs(cfg, fetch=fetch)

    print(f"Current Version: {cfg.current_version}")
    print(f"PEP440 Version : {cfg.pep440_version}")


@cli.command()
@click.option('-v', '--verbose', count=True, help="Control log level. -vv for debug level.")
@click.option(
    "--dry", default=False, is_flag=True, help="Display diff of changes, don't rewrite files."
)
def init(verbose: int = 0, dry: bool = False) -> None:
    """Initialize [pycalver] configuration."""
    _init_logging(verbose=max(_VERBOSE, verbose))

    ctx: config.ProjectContext = config.init_project_ctx(project_path=".")
    cfg: config.MaybeConfig    = config.parse(ctx)

    if cfg:
        log.error("Configuration already initialized in {ctx.config_filepath}")
        sys.exit(1)

    if dry:
        print("Exiting because of '--dry'. Would have written to setup.cfg:")
        cfg_lines = config.default_config(ctx)
        print("\n    " + "\n    ".join(cfg_lines))
        return

    config.write_content(ctx)


def _assert_not_dirty(vcs, filepaths: typ.Set[str], allow_dirty: bool):
    dirty_files = vcs.status()

    if dirty_files:
        log.warn(f"{vcs.name} working directory is not clean:")
        for dirty_file in dirty_files:
            log.warn("    " + dirty_file)

    if not allow_dirty and dirty_files:
        sys.exit(1)

    dirty_pattern_files = set(dirty_files) & filepaths
    if dirty_pattern_files:
        log.error("Not commiting when pattern files are dirty:")
        for dirty_file in dirty_pattern_files:
            log.warn("    " + dirty_file)
        sys.exit(1)


def _bump(cfg: config.Config, new_version: str, allow_dirty: bool = False) -> None:
    _vcs: typ.Optional[vcs.VCS]

    try:
        _vcs = vcs.get_vcs()
    except OSError:
        log.warn("Version Control System not found, aborting commit.")
        _vcs = None

    filepaths = set(cfg.file_patterns.keys())

    if _vcs:
        _assert_not_dirty(_vcs, filepaths, allow_dirty)

    rewrite.rewrite(new_version, cfg.file_patterns)

    if _vcs is None or not cfg.commit:
        return

    for filepath in filepaths:
        _vcs.add(filepath)

    _vcs.commit(f"bump version to {new_version}")

    if cfg.commit and cfg.tag:
        _vcs.tag(new_version)

    if cfg.commit and cfg.tag and cfg.push:
        _vcs.push(new_version)


@cli.command()
@click.option("-v", "--verbose", count=True, help="Control log level. -vv for debug level.")
@click.option(
    "-f/-n", "--fetch/--no-fetch", is_flag=True, default=True, help="Sync tags from remote origin."
)
@click.option(
    "--dry", default=False, is_flag=True, help="Display diff of changes, don't rewrite files."
)
@click.option(
    "--release",
    default=None,
    metavar="<name>",
    help=(
        f"Override release name of current_version. Valid options are: "
        f"{', '.join(parse.VALID_RELEASE_VALUES)} and final."
    ),
)
@click.option(
    "--allow-dirty",
    default=False,
    is_flag=True,
    help=(
        "Commit even when working directory is has uncomitted changes. "
        "(WARNING: The commit will still be aborted if there are uncomitted "
        "to files with version strings."
    ),
)
def bump(
    release    : typ.Optional[str] = None,
    verbose    : int  = 0,
    dry        : bool = False,
    allow_dirty: bool = False,
    fetch      : bool = True,
) -> None:
    """Increment the current version string and update project files."""
    verbose = max(_VERBOSE, verbose)
    _init_logging(verbose)

    if release:
        _validate_release_tag(release)

    ctx: config.ProjectContext = config.init_project_ctx(project_path=".")
    cfg: config.MaybeConfig    = config.parse(ctx)

    if cfg is None:
        log.error("Could not parse configuration. Perhaps try 'pycalver init'.")
        sys.exit(1)

    cfg = _update_cfg_from_vcs(cfg, fetch=fetch)

    old_version = cfg.current_version
    new_version = version.incr(old_version, release=release)

    log.info(f"Old Version: {old_version}")
    log.info(f"New Version: {new_version}")

    if dry or verbose >= 2:
        print(rewrite.diff(new_version, cfg.file_patterns))

    if dry:
        return

    _bump(cfg, new_version, allow_dirty)
