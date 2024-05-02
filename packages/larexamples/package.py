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


class Larexamples(CMakePackage):
    """Larexamples"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larexamples"
    git = "https://github.com/LArSoft/larexamples.git"
    url = "https://github.com/LArSoft/larexamples/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larexamples/tags"

    version("09.09.05", sha256="5181fbc02b5e59978543b76fe40ec8c8da8208853f63b9b3829abfc906672e66")
    version("09.09.04", sha256="6125aa34a9d27704130521329eb091f96d334520da5926edda231e65c4b4e727")
    version("09.09.03", sha256="6684ce334b3f994ff578d53f1ae514bfde0a5669887784d3f3c801cd655757e5")
    version("09.09.02", sha256="2d01cf0b0017a04043d23c8602aaafc25c8ac36dbf1ed7f65708d59475741d56")
    version("09.09.01", sha256="ecf10eeafada90f1a2f047322f82ad2481c07f529b2dfb162d05ae92a8967fc1")
    version("09.09.00", sha256="1c7afa6a78e145ebd2150e3282516596facf65cde115bdaaa366d09755aa60fa")
    version("09.08.18", sha256="8a02583245a27d278ab724d16744dbec88ea55c41aabd3bf7721bb1437d21e00")
    version("09.08.17", sha256="ba788e436b3cc9813c9ba4e2ed42d314a8ca0c557a0b8c3e4f756128048fb1dd")
    version("09.08.16", sha256="214877680af0770308e110723f08dc96d53ff2e19c730ad18fcbd7d3dc8d79de")
    version("09.08.15", sha256="94e12ce1e64009c574413fccd4b1668b8e246dc30b85308aa03aaa0b07f8b8e0")
    version("09.08.14", sha256="4bc085578ae747e9ace62e089cb2f0fd9fd79a31e63bd9748cee4684d4a15928")
    version("09.08.13", sha256="d1f3de784d8cc844037c91a37736f8825867f3a51d81a6c3339dd145efe52f23")
    version("09.08.12", sha256="0008efbe77d3ea8c768e40ffc7cb6976daf5b654a09fa627e5d9d2bca043f9cf")
    version("09.08.11", sha256="c112fe5ce50f8e51e81b0d889e1c76236c66a4cfd577687ad91c9d79b96dcf67")
    version("09.08.10", sha256="4ca06e9aef4df0031de5ee89aee60fa22c9b365f2ac7521124c78d4f353cc37f")
    version("09.08.07", sha256="18c15b664d1c9dcd470d18b80231c84046e8a657c562cde990e45c367bd272c6")
    version("09.08.04", sha256="842ef4901801286c9d86002b81f3cd220cfc4211e43db92a90d508170cb2168f")
    version(
        "09.02.08.02", sha256="144ffc2e740c7aa73155b3e1f02a4bf0016ac25c9e5092162aefb4fb507ce1c3"
    )
    version(
        "09.02.08.01", sha256="8745a14211001dd321b23b0a591e65aecd188d4393b5f6cac26a42f9e2f66075"
    )
    version("09.02.05", sha256="4b2bfdb5c9e1354c12f4581185c3214f37b178de14e4f630f924a6aa9dabcfde")
    version("09.02.03", sha256="dc34d8563a7baee2698edb3573063818b5852ce7b0092d201587e12eea7eb8e8")
    version("09.02.02", sha256="063a962e804fa3d72235ebecb8708d2859ec4f0b41f68b3785354cd2a483e044")
    version("09.02.01", sha256="12ac083b4ba5f13b37bae0038a6e06c8a562a17a24c131d11ba74de579d8b658")
    version("09.02.00", sha256="798a3c74fc510d5a9777f47bffebcbdb9cb76aa62f2ec19b39e7194e6acc2aef")
    version("09.01.20", sha256="1ea2eaae8189605f387d7822d016f4d19a3c123fc8ab60073a99d9927ee1104e")
    version("09.01.19", sha256="3e22003f17f9101beb9ea7df375c14b31b4aadd3e7e0e5e304dbf9f231773d2a")
    version("09.01.18", sha256="609d23c317863c2167b33cb32fe28d9255c08608a04452fc9611c58ca72e692a")
    version("09.01.17", sha256="43edeed8b818581b4ed0ca0f2fb58bea07ed7bc5561aa58f252485e63c8eae9b")
    version(
        "mwm1", tag="mwm1", git="https://github.com/marcmengel/larexamples.git", get_full_repo=True
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

    patch("v09_02_05.patch", when="@09.02.05")
    # patch('v09_02_08_01.patch', when='@09.02.08.01')
    patch("v09_02_08_02.patch", when="@09.02.08.02")

    depends_on("larsim")
    depends_on("root")
    depends_on("cetmodules", type="build")
    depends_on("larsoft-data", type="build")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]
        return args

    def setup_build_environment(self, spack_env):
        spack_env.prepend_path("LD_LIBRARY_PATH", str(self.spec["root"].prefix.lib))
        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        # Set path to find fhicl files
        spack_env.prepend_path("FHICL_FILE_PATH", os.path.join(self.build_directory, "fcl"))
        # Set path to find gdml files
        spack_env.prepend_path("FW_SEARCH_PATH", os.path.join(self.build_directory, "fcl"))
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
        # Set path to find fhicl files
        run_env.prepend_path("FHICL_FILE_PATH", os.path.join(self.prefix, "fcl"))
        # Set path to find gdml files
        run_env.prepend_path("FW_SEARCH_PATH", os.path.join(self.prefix, "fcl"))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
