# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import sys

from spack import *

libdir = "%s/var/spack/repos/fnal_art/lib" % os.environ["SPACK_ROOT"]
if libdir not in sys.path:
    sys.path.append(libdir)


def patcher(x):
    cetmodules_20_migrator(".", "dk2nugenie", "01.08.00")


class Dk2nugenie(CMakePackage):
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
    depends_on("libxml2")
    depends_on("log4cpp")
    depends_on("genie")
    depends_on("dk2nudata")
    depends_on("tbb")

    parallel = False

    def patch(self):
        patch("dk2nu.patch", when="^genie@3.00.00:", working_dir="v{0}".format(self.version))
        cmakelists = FileFilter("{0}/genie/CMakeLists.txt".format(self.stage.source_path))
        cmakelists.filter(r"\$\{GENIE\}/src", "${GENIE}/include/GENIE")
        cmakelists.filter(r"\$ENV", "$")
        cmakelists.filter("execute_process", "#execute_process")

    #root_cmakelists_dir = "dk2nu"

    def cmake_args(self):
        prefix = self.prefix
        args = [
            "-DCMAKE_INSTALL_PREFIX=%s" % prefix,
            "-DGENIE_ONLY=ON",
            "-DTBB_LIBRARY=%s/libtbb.so" % self.spec["tbb"].prefix.lib64,
            "-DGENIE_INC=%s/GENIE" % self.spec["genie"].prefix.include,
            "-DGENIE=%s" % self.spec["genie"].prefix,
            "-DGENIE_VERSION=%s" % self.spec["genie"].version,
            "-DDK2NUDATA_DIR=%s" % self.spec["dk2nudata"].prefix.lib,
            "-DLIBXML2_INC=%s" % self.spec["libxml2"].prefix.include,
            "-DLOG4CPP_INC=%s" % self.spec["log4cpp"].prefix.include,
        ]

        return args

    def setup_dependent_build_environment(self, spack_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.set("DK2NUGENIE_LIB", self.prefix.lib)
        spack_env.set("DK2NUGENIE_INC", self.prefix.include)
