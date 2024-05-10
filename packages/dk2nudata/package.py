# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Dk2nudata(CMakePackage):
    """This package consolidates the disparate formats of neutrino beam simulation "flux" files."""

    url = "https://github.com/NuSoftHEP/dk2nu/archive/refs/tags/v01_10_01.tar.gz"

    version("01.10.01", sha256="8680ffae5182dc1c0a04a3410cf687c4b7c0d9420e2aabc5c3c4bb42c69c3dd0")
    version("01_10_01", sha256="8680ffae5182dc1c0a04a3410cf687c4b7c0d9420e2aabc5c3c4bb42c69c3dd0")

    def url_for_version(self, version):
        url = "https://github.com/NuSoftHEP/dk2nu/archive/refs/tags/v{0}.tar.gz"
        return url.format(version.underscored)

# Variant is still important even though it's not passed to compiler
    # flags (use of ROOT, etc.).
    variant(
        "cxxstd",
        default="11",
        values=("11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cmake", type="build")
    depends_on("root")
    depends_on("tbb")
    depends_on("libxml2")
    depends_on("log4cpp")

    parallel = False

   # root_cmakelists_dir = "dk2nu"

    def cmake_args(self):
        if os.path.exists(self.spec["tbb"].prefix.lib64):
            tbblib=self.spec["tbb"].prefix.lib64
        else:
            tbblib=self.spec["tbb"].prefix.lib
        args = ["-DWITH_GENIE=OFF", "-DTBB_LIBRARY=%s/libtbb.so" % tbblib]
        return args

    def setup_dependent_build_environment(self, spack_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.set("DK2NUDATA_LIB", self.prefix.lib)
        spack_env.set("DK2NUDATA_INC", self.prefix.include)

    def setup_run_environment(self, run_env):
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
