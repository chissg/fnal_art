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


class ArtRootIo(CMakePackage):
    """Root-based input/output for the art suite."""

    homepage = "https://art.fnal.gov/"
    git = "https://github.com/art-framework-suite/art-root-io.git"
    url = "https://github.com/art-framework-suite/art-root-io/archive/refs/tags/v1_13_01.tar.gz"

    version("develop", branch="develop", get_full_repo=True)
    version("1.13.05", sha256="b60b44776c6b9ffb4ea554b30f4c5c58e9f297ce546d5b0ac30b6c47f1e102bb")
    version("1.13.03", sha256="507181c5caa8a53017783415509b3a01d152864a6ed0334c925eac11d47f6fb9")
    version("1.13.01", sha256="f4a41d448672f0dfa31d3a27787af3af29dd1bf82028d7854652f02d64222366")
    version("1.12.04", sha256="912e01cb3f253de244548a52ee4f9e31b2eb6d1af9bd7cb33e48bab064651273")
    version("1.12.03", sha256="2281435aa910085902f9a8d14c90d69ee980a980637bbb4bb2e1aad1ab5f02af")
    version("1.12.02", sha256="f7fa60cad2947fa135cdd52cb5d39d3e871cca246181288734745067c7c3f555")
    version("1.12.01", sha256="d6594b039567c5f4a7053678d70b82e543a19fef989f0957ca6a6e4862372511")
    version("1.11.03", sha256="a29b64b07709ac1560ccc1b9570cc8a4197a8834d2b9dfea5bbfd293231d4a20")
    version("1.11.00", sha256="1134d1c1e69045249bf678e6e07728f06035ee2ee982af5155184d1c271468ae")
    version("1.08.05", sha256="77f58e4200f699dcb324a3a9fc9e59562d2a1721a34a6db43fdb435853890d21")
    version("1.08.03", sha256="fefdb0803bc139a65339d9fa1509f2e9be1c5613b64ec1ec84e99f404663e4bf")

    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )
    conflicts("cxxstd=17", when="@develop")

    depends_on("art")
    depends_on("boost+filesystem+date_time+program_options")
    depends_on("canvas")
    depends_on("canvas-root-io")
    depends_on("catch2@3:", when="@1.12:", type=("build", "test"))
    depends_on("catch2@2.3.0:", when="@:1.11.99", type=("build", "test"))
    depends_on("cetlib")
    depends_on("cetlib-except")
    # depends_on("cetmodules@3.19.02:", type="build")
    depends_on("cetmodules", type="build")
    # conflicts("cetmodules@:3.21.00", when="catch2@3:")
    depends_on("fhicl-cpp")
    depends_on("hep-concurrency")
    depends_on("messagefacility")
    depends_on("root+python")
    depends_on("sqlite@3.8.2:")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    def url_for_version(self, version):
        url = "https://github.com/art-framework-suite/art-root-io/archive/refs/tags/v{0}.tar.gz"
        return url.format(version.underscored)

    def cmake_args(self):
        return preset_args(self.stage.source_path) + [
            "--trace-expand",
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ]

    def setup_build_environment(self, env):
        prefix = self.build_directory
        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", os.path.join(prefix, "lib"))
        # Cleanup.
        sanitize_environments(env, "PATH", "CET_PLUGIN_PATH")

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Cleanup.
        sanitize_environments(env, "CET_PLUGIN_PATH")

    def setup_dependent_build_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Cleanup.
        sanitize_environments(env, "CET_PLUGIN_PATH")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Cleanup.
        sanitize_environments(env, "CET_PLUGIN_PATH")
