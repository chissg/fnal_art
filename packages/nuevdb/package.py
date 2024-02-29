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


class Nuevdb(CMakePackage):
    """Nuevdb"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/nuevdb/wiki"
    git = "https://github.com/NuSoftHEP/nuevdb.git"
    url = "https://github.com/NuSoftHEP/nuevdb/archive/refs/tags/v1_05_05.tar.gz"
    list_url = "https://api.github.com/repos/NuSoftHEP/nuevdb/tags"

    version("1.08.01", sha256="5bbf54e6c772e8f73e8ad2f7629f47e8b15731dd7af80c51b2060976c8c7a013")
    version("1.08.00", sha256="3357833402e4717aee8f562a6ea59eb47f1be6372215a049e354f9eeaa903ac9")
    version("1.07.03", sha256="264e74ada3a6f7561f9278d18a9b02bd1e397c1bbafb1c0ee1e363a091136389")
    version("1.07.02", sha256="8d429ca966d481f7ad46b18c5fdb77b67cfb949ac709f5cb9a733995835387d9")
    version("1.07.01", sha256="32d32c340a055242ed214098296c6bea0b87beb7ba0356fcc52fc72673000cef")
    version("1.06.00", sha256="5a9dc5dd235ed4a16f26ebf09070d806f132bb22c6750a019c6ca7a3797d5d51")
    version("1.05.06", sha256="76050a5dea93202b39ce81e09a4b66411ad845340bef935fe50d6d54e1a90126")
    version("1.05.05", sha256="e5bbd1c523f8befcb63b4a6a529e6eed592519ddefd31a2504ffd25e312e1115")
    version("mwm1", tag="mwm1")
    version("develop", branch="develop", get_full_repo=True)

    def url_for_version(self, version):
        url = "https://github.com/NuSoftHEP/{0}/archive/v{1}.tar.gz"
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
                    if d["name"].startswith("v")
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

    patch("cetmodules2.patch", when="@develop")
    patch("v1_05_05.patch", when="@1.05.05")
    patch("v1_05_06.patch", when="@1.05.06")

    depends_on("cetmodules", type="build")
    depends_on("art-root-io")
    depends_on("art")
    depends_on("root")
    depends_on("libwda")
    depends_on("nusimdata")
    depends_on("postgresql")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("CRYHOME", self.spec["cry"].prefix),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", 1),
            "-Dlibwda_DIR:PATH={0}".format(self.spec["libwda"].prefix),
        ]
        return args

    def setup_build_environment(self, spack_env):
        spack_env.set("POSTGRESQL_LIBRARIES", self.spec["postgresql"].prefix.lib)
        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        # Cleaup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        # Binaries.
        run_env.prepend_path("PATH", os.path.join(self.prefix, "bin"))
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            run_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/job".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
        sanitize_environments(spack_env)

    def setup_dependent_run_environment(self, run_env, dspec):
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("PATH", self.prefix.bin)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.append_path("FHICL_FILE_PATH", "{0}/job".format(self.prefix))
        run_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
        sanitize_environments(run_env)
