# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from pathlib import Path

sys.path.append(str(Path(__file__).parents[2] / "lib"))
from utilities import *

from spack.package import *


def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)


class Gallery(CMakePackage):
    """A library to allow reading of Root output files produced by the art
    suite.
    """

    homepage = "https://art.fnal.gov/"
    git = "https://github.com/art-framework-suite/gallery.git"
    url = "https://github.com/art-framework-suite/gallery/archive/refs/tags/v1_21_01.tar.gz"

    version("develop", branch="develop", get_full_repo=True)
    version("1.22.01", sha256="86dd9bbc88f765e1b7ea75b49e6f3af401b9f92461e91bd9d65b407bad5a14cb")
    version("1.21.01", sha256="e932c2469de4abb87527defe7357ea6423e8dbc18ef9d9b5148e5e658c3ffc91")
    version("1.21.02", sha256="0eb3eff1a173d09b698e1ba174ab61d9af72937067b300f1b73d0eca73349294")
    version("1.21.03", sha256="b1f41e1e4efcaf73b6c90c12dc513217ea5591ce369a9335d2ca6f4d0f2b1728")
    version("1.20.02", sha256="433e2b5727b9d9cf47206d9a01db5eab27c5cbb76407bb0ec14c0fd4e4dc41f9")

    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )
    conflicts("cxxstd=17", when="@develop")

    depends_on("canvas")
    depends_on("canvas-root-io")
    depends_on("cetlib")
    depends_on("cetmodules", type="build")
    depends_on("cmake@3.21:", type="build")
    depends_on("range-v3", type=("build", "link", "run"))
    depends_on("root+python")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    def url_for_version(self, version):
        url = "https://github.com/art-framework-suite/gallery/archive/refs/tags/v{0}.tar.gz"
        return url.format(version.underscored)

    def cmake_args(self):
        return preset_args(self.stage.source_path) + [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")
        ]

    def setup_dependent_build_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH")
