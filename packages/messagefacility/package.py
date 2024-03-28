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


class Messagefacility(CMakePackage):
    """A configurable message logging facility for the art suite."""

    homepage = "https://art.fnal.gov/"
    git = "https://github.com/art-framework-suite/messagefacility.git"
    url = (
        "https://github.com/art-framework-suite/messagefacility/archive/refs/tags/v2_10_03.tar.gz"
    )

    version("2.10.05", sha256="cd99c85b81f7d4d23195fb6f84d8815c73d6eedbb4c543dc10c9616a5c31368d")
    version("2.10.04", sha256="5c63a26c974c69677eeb8c927a581aa40bd7ff8f6abf6ebcdd20cc423e145df9")
    version("2.10.03", sha256="94700d414a59111200dff1d77839d2edcb72f05530c039f6bdddb470be6e2252")
    version("2.10.02", sha256="1dfed808595316ce1d619e48a20b3f0cfd18afa32d807d6c3e822fd41b042fa2")
    version("2.10.01", sha256="b9572b4ccf0e61edcaf4fc4548d616be00754c9ae04aa594640d992c1047c315")
    version("2.09.00", sha256="0d596b10691d92b73a396c974846211ea7d65e819685a39b3fa1d9d4126746f0")
    version("2.08.04", sha256="dcf71449b0f73b01e2d32d1dc5b8eefa09a4462d1c766902d916ed6869b6c682")
    version("2.08.03", sha256="bf10264d94e77e14c488e02107e36e676615fa12c9e2795c4caccf0c913ba7b9")
    version("2.08.00", sha256="a2c833071dfe7538c40a0024d15f19ba062fd5f56b26f83f5cb739c12ff860ec")
    version("develop", branch="develop")

    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )
    conflicts("cxxstd=17", when="@develop")

    depends_on("boost+filesystem+program_options+system")
    depends_on("catch2@3.3.0:", when="@2.10.00:")
    depends_on("catch2@2.3.0:2", when="@:2.09", type=("build", "test"))
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("cetmodules", type="build")
    conflicts("cetmodules@:3.21.00", when="catch2@3:")
    depends_on("fhicl-cpp@4.16.00:", when="@2.08.05:")
    depends_on("fhicl-cpp@4.15", when="@2.08.01:2.08.04")
    depends_on("fhicl-cpp@:4.14", when="@:2.08.00")
    depends_on("hep-concurrency@1.07.05:", when="@2.08.00:2.10.03")
    depends_on("hep-concurrency@:1.07.04", when="@:2.07")
    depends_on("perl", type=("build", "run"))
    depends_on("py-pybind11", type="build")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    def url_for_version(self, version):
        url = (
            "https://github.com/art-framework-suite/messagefacility/archive/refs/tags/v{0}.tar.gz"
        )
        return url.format(version.underscored)

    def cmake_args(self):
        return preset_args(self.stage.source_path) + [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")
        ]

    def setup_build_environment(self, env):
        prefix = self.build_directory
        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", os.path.join(prefix, "lib"))
        # Perl modules.
        env.prepend_path("PERL5LIB", os.path.join(prefix, "perllib"))
        # Cleaup.
        sanitize_environments(env, "PATH", "CET_PLUGIN_PATH", "PERL5LIB")

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Perl modules.
        env.prepend_path("PERL5LIB", os.path.join(prefix, "perllib"))
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "PERL5LIB")

    def setup_dependent_build_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Perl modules.
        env.prepend_path("PERL5LIB", os.path.join(prefix, "perllib"))
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "PERL5LIB")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Perl modules.
        env.prepend_path("PERL5LIB", os.path.join(prefix, "perllib"))
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "PERL5LIB")
