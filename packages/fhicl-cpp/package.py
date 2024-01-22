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


class FhiclCpp(CMakePackage):
    """A C++ implementation of the FHiCL configuration language for the art
    suite.
    """

    homepage = "https://art.fnal.gov/"
    git = "https://github.com/art-framework-suite/fhicl-cpp.git"
    url = "https://github.com/art-framework-suite/fhicl-cpp/archive/refs/tags/v4_18_02.tar.gz"

    version("4.18.03", sha256="c08fd6ce37225e58d3d893f9205b321ae2fff2d8b5c96c2e22ac24708a4309af")
    version("4.18.02", sha256="ca96ed2f524061b0b9c03aef50d9ef9aad1295d331195e07f7584da7b63ba946")
    version("4.18.01", sha256="ad99cdf48b912fc51852229e04896c04db6db55a7c49f873156dae6665d8bfa7")
    version("4.18.00", sha256="cd5c7c0bef5e235264bf22819db283bd3ebfd512ecab06fb3722142cec0a0a5e")
    version("4.17.00", sha256="07fbba4aed129fcc5edbd9a7304dc3ccd53d2405830779e7c2d71a8b73a99247")
    version("4.15.03", sha256="99ae2b7557c671d0207dea96529e7c0fca2274974b6609cc7c6bf7e8d04bd12b")
    version("develop", branch="develop", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )
    conflicts("cxxstd=17", when="@develop")

    depends_on("boost+program_options+test")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("cetmodules@3.19.02:", type="build")
    depends_on("cmake@3.21:", type="build")
    depends_on("hep-concurrency", type="build")
    depends_on("openssl")
    depends_on("py-pybind11", type="build")
    depends_on("python")
    depends_on("sqlite")
    depends_on("tbb")

    patch("test_build.patch", when="@:4.17.00")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    def url_for_version(self, version):
        url = "https://github.com/art-framework-suite/fhicl-cpp/archive/refs/tags/v{0}.tar.gz"
        return url.format(version.underscored)

    def cmake_args(self):
        return preset_args(self.stage.source_path) + [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")
        ]

    def setup_build_environment(self, env):
        prefix = self.build_directory
        # Path for tests.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))
        # Cleanup
        sanitize_environments(env, "PATH")

    def setup_run_environment(self, env):
        bindir = self.prefix.bin
        # Bash completions.
        env.from_sourcing_file(os.path.join(bindir, "fhicl-dump_completions"))
        env.from_sourcing_file(os.path.join(bindir, "fhicl-expand_completions"))
        env.from_sourcing_file(os.path.join(bindir, "fhicl-get_completions"))
