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


class Nug4(CMakePackage):
    """Generator interfaces to art for GENIE and GiBUU."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/nug4"
    git = "https://github.com/NuSoftHEP/nug4.git"
    url = "https://github.com/NuSoftHEP/nug4/archive/refs/tags/v1_10_00.tar.gz"
    list_url = "https://api.github.com/repos/NuSoftHEP/nug4/tags"

    version("1.15.02", sha256="53dcc4998a9e4841739cfbc7ee2e5cb312321cb1be2591af891f39ff7d306ed7")
    version("1.15.01", sha256="839ff89b3f85b9482384df946d5c13a0c7c941e4bdfd2d2955e36c290811d926")
    version("1.15.00", sha256="cc2b39a9e9888898f07f10467c7521b1c99f99e6a3528902b4a77e866a2791c3")
    version("1.14.03", sha256="6ef9cfc8ec87b4e27dda47421cfa293da853738ece6604d2b15994ce05ba74d3")
    version("1.14.02", sha256="30d93e4b0a34ed2d35c0aac3cde447ff9985ceb6ca442692e3022aca77cefda9")
    version("1.14.01", sha256="3438c8633f9b0cd61bdb152b5c00cfce9533c527ca90ddcff0d9719806378210")
    version("1.13.03", sha256="abfcda126d71909a68808eb10fa4428273f5da287ffec1efb7aca69d4bcb2945")
    version("1.12.00", sha256="392e5c8bee1cad0dd997b134de1e7c1ab9e580e7dd87600927a4c4f595afa081")
    version("1.11.01", sha256="18b00de65e442c45fcc1f91c3ef17d79c83aea9b0e1b73acfca53fd21da2d706")
    version("1.11.00", sha256="e612e229100a1cc3e25b390460da208c5e18f858627f441b7959dbb957e2bcf9")
    version("develop", branch="develop", get_full_repo=True)
    version("mwm1", tag="mwm1", get_full_repo=True)

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

    # Build-only dependencies.
    depends_on("cetmodules", type="build")
    depends_on("cetbuildtools", type="build")
    depends_on("cmake", type="build")
    depends_on("art")
    depends_on("art-root-io")
    depends_on("boost")
    depends_on("nusimdata")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("geant4 cxxstd=20", when="cxxstd=20")
    depends_on("geant4 cxxstd=17", when="cxxstd=17")
    depends_on("geant4 cxxstd=14", when="cxxstd=14")
    depends_on("pythia8")

    patch("cetmodules2.patch", when="@develop")
    patch("v1_11_00.patch", when="@1.11.00")
    patch("v1_11_01.patch", when="@1.11.01")

    def cmake_args(self):
        # Set CMake args.
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-DIGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES=1",
        ]
        return args

    def setup_build_environment(self, spack_env):
        spack_env.set("CETBUILDTOOLS_VERSION", self.spec["cetmodules"].version)
        spack_env.set("CETBUILDTOOLS_DIR", self.spec["cetmodules"].prefix)
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
        # Perl modules.
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path("PATH", self.prefix.bin)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # Cleanup.
        sanitize_environments(spack_env)

    def setup_dependent_run_environment(self, run_env, dependent_spec):
        # Binaries.
        run_env.prepend_path("PATH", self.prefix.bin)
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # Cleanup.
        sanitize_environments(run_env)
