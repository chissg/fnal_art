# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.util.spack_json as sjson
from spack import *


def sanitize_environments(*args):
    for env in args:
        for var in (
            "PATH",
            "CET_PLUGIN_PATH",
            "LDSHARED",
            "LD_LIBRARY_PATH",
            "DYLD_LIBRARY_PATH",
            "LIBRARY_PATH",
            "CMAKE_PREFIX_PATH",
            "ROOT_INCLUDE_PATH",
        ):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Larsimdnn(CMakePackage):
    """Larsim"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larsim"
    git = "https://github.com/LArSoft/larsimdnn.git"
    url = "https://github.com/LArSoft/larsimdnn/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larsimdnn/tags"

    version("09.06.05", sha256="48009e7f9f89f8035b27d4cd585c5bb16ab443cde3588d1e14098a1e71bec63d")
    version("09.06.04", sha256="b5312d3040f8a052b965392b6d6a90e9dc4597af95429d14d3f1f11ef1825740")
    version("09.06.03", sha256="97499538f187664a0402cfe9197e29b37783505f90055abab3cce5ae6c9df43f")
    version("09.06.02", sha256="d3553adc87ef6c0c63c6d32ccd3eb45b5485c7b6556b49802c83d3869f22c704")
    version("09.06.01", sha256="3c53c4ea258ba71d90c6c3f88299a2731ce6d5e1b0eb47c9a2f90bdbf7260404")
    version("09.06.00", sha256="7ff5fa3b548d2831db8e23519ddf8bdfde6d5e280c23355ff26b7fb27c29a6cd")
    version("09.05.18", sha256="e935b0b61325adc1dceee1025c9de6af0a81693f2ede98cfc4a4e5c830dbe8c3")
    version("09.05.17", sha256="1b764c51dca314146a220befa7c085fa0e6d88d2a76e23c12d7002f3df3648ad")
    version("09.05.16", sha256="062abb4b78d27eeae26351af0b8208612f7a492c744af4e4a848af0f5fe647dc")
    version("09.05.15", sha256="cc65a11c4f8771496806c2b3cc6c8799a9333ea36a5389109e4c1a6503f13b88")
    version("09.05.14", sha256="8ae48586caf02a02c3bbf8002e43f644d2ed24d8d93abd04764c33425df11710")
    version("09.05.13", sha256="dca784aab810cea44d20b6328cbb8db3c512fcaa50c539ab55d777458064587f")
    version("09.05.12", sha256="1a104cb60770c3bba8241d5f394e9323f8e54bbcb6074a71948276df382efc0a")
    version("09.05.11", sha256="e7aa552575a12481504765510c17c01c9e4b0a08c8e0cec60bd046e07445cbf2")
    version("09.05.10", sha256="245b7a56cb1cefca75be0ca84ee993a6a6390623223bd2b76e155ae0347be6e8")
    version(
        "mwm1", tag="mwm1", git="https://github.com/marcmengel/larsimdnn.git", get_full_repo=True
    )
    version("develop", branch="develop", get_full_repo=True)

    def url_for_version(self, version):
        url = "https://github.com/LArSoft/{0}/archive/v{1}.tar.gz"
        return url.format(self.name, version.underscored)

    def fetch_remote_versions(self, concurrency=None):
        return dict(
            map(
                lambda v: (v.dotted, self.url_for_version(v)),
                [
                    Version(d["name"][1:])
                    for d in sjson.load(
                        spack.util.web.read_from_url(
                            self.list_url, accept_content_type="application/json"
                        )[2]
                    )
                    if d["name"].startswith("v") and not d["name"].endswith(")")
                ],
            )
        )

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("larsoft-data")
    depends_on("larevt")
    depends_on("marley")
    depends_on("genie")
    depends_on("ifdhc")
    depends_on("xerces-c")
    depends_on("libxml2")
    depends_on("clhep")
    depends_on("nug4")
    depends_on("nugen")
    depends_on("nurandom")
    depends_on("artg4tk")
    depends_on("larsim")
    depends_on("ppfx")
    depends_on("cetmodules", type="build")
    depends_on("larfinder", type="build")
    depends_on("nufinder", type="build")

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-DIFDH_INC={0}".format(self.spec["ifdhc"].prefix.include),
            "-DIFDH_LIB={0}".format(self.spec["ifdhc"].prefix),
            "-DGENIE_INC={0}".format(self.spec["genie"].prefix.include),
            "-DGENIE_VERSION=v{0}".format(self.spec["genie"].version.underscored),
            "-DLARSOFT_DATA_DIR=v{0}".format(self.spec["larsoft-data"].prefix),
            "-DLARSOFT_DATA_VERSION=v{0}".format(self.spec["larsoft-data"].version.underscored),
        ]
        return args

    def setup_build_environment(self, spack_env):
        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.build_directory, "perllib"))
        # Cleaup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            run_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("LARANA_INC", self.prefix.include)
        spack_env.set("LARANA_LIB", self.prefix.lib)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
