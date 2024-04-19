# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.util.spack_json as sjson
from spack.package import *
from pathlib import Path
import re

version_re = re.compile(f"^v")


def preset_args(source_path):
    if (Path(source_path) / "CMakePresets.json").exists():
        return ["--preset", "default"]
    return []


def sanitize_environments(env, *env_vars):
    for var in env_vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)


def dotted_version_str(name):
    linted = version_re.sub("", name)
    return Version(linted).dotted


def github_version_url(organization, repo_name, native_version_str):
    return f"https://github.com/{organization}/{repo_name}/archive/{native_version_str}.tar.gz"


def fetch_remote_tags(organization, repo_name, url):
    _, _, request = spack.util.web.read_from_url(url, accept_content_type="application/json")
    return {
        dotted_version_str(d["name"]): github_version_url(organization, repo_name, d["name"])
        for d in sjson.load(request)
    }


class Utilities(Package):
    """Dummy package to provide utilities to real packages.
    This package cannot be installed.
    """

    homepage = "None"

    license("UNKNOWN")
