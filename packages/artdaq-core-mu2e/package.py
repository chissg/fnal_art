# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *


def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)


class ArtdaqCoreMu2e(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://github.com/Mu2e/artdaq_core_mu2e"
    url = "https://github.com/Mu2e/artdaq_core_mu2e/archive/refs/tags/v1_08_04.tar.gz"
    git = "https://github.com/Mu2e/artdaq_core_mu2e.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v2_01_02", commit="8ef7971")
    version("v2_01_01", commit="e3d4664")
    version("v2_00_00", commit="b4f0ff0")
    version("v1_09_02", commit="6490f81")
    version("v1_08_04", commit="17ff9a2")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/artdaq_core_mu2e/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cetmodules", type="build")

    depends_on("mu2e-pcie-utils")
    depends_on("artdaq-core")

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")
        env.set("ARTDAQ_CORE_MU2E_INC", prefix.include)

    def setup_dependent_build_environment(self, env, dependent_spec):
        prefix = self.prefix
        env.set("ARTDAQ_CORE_MU2E_INC", prefix.include)
