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


class Larana(CMakePackage):
    """Larana"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larana"
    git = "https://github.com/LArSoft/larana.git"
    url = "https://github.com/LArSoft/larana/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larana/tags"

    version("09.15.05", sha256="9997c564bc5b95f4949033b51930c349d93ff48a932f0a6105a451020b722489")
    version("09.15.04", sha256="25a1f5c4e32eac31890952840312df8624ad8749ef3fee7bfb6873a9c6801e4f")
    version("09.15.03", sha256="4b3c8ec9961a4f4c2792b0d7371a40e1d970efdbf1d2bc6ada406fae3a7eca15")
    version("09.15.02", sha256="682905953f69993cc033de0c5490ca7a87984967e19345a9621f16d04a1d6837")
    version("09.15.01", sha256="49e48447acc1242e3dccfbdd55c3b6286a32d9ac8c930bc644bc7f28d472b7f5")
    version("09.15.00", sha256="2e92752004a01f3557210eb2727573ab780e179147f79197c40aa6b754eb7c87")
    version("09.14.19", sha256="dee4e0c3f666e30ec13e8b566f7e3b911ed132056268f5a848626ed45e066623")
    version("09.14.18", sha256="6fca10443975d0ca6a179c5b82861a6aedf7653debd6685398cad302489a0427")
    version("09.14.17", sha256="4175b7471b8bc4029a33296a92a63abb9e8ae0a70db4b1c18ea50d5ac8bfcdd6")
    version("09.14.16", sha256="ba636ae1228c1b6db43714436519c0cb9cdad42779a43c787deb667060d6b83c")
    version("09.14.15", sha256="39058e4097d02581c6adf7b605e5e8c928c4a3bc3b8af7af24995077a96b98a4")
    version("09.14.14", sha256="9493f8618f62c68f11b00deb95b34795f4fbc9cac12284e101dfc90c488400f7")
    version("09.14.13", sha256="28ea19d1b6ff0a7b532ea9f6c105579454604da5468304c3918ab7c9a5889044")
    version("09.14.12", sha256="004e67aae1050b85119eb27d3baf73f8beb87f967e886a1737277b0afd9fc61b")
    version("09.14.11", sha256="fbcdf7a2bcef81fb31a10b87b86d8f3af2b1de7dbde192e4a6caf2d2e6fe00bf")
    version("09.14.10", sha256="39e6b27ccd0e7b70da6e975a7bef0be4c2bc78674ab448d8ff75af45f5e92c26")
    version("09.14.09", sha256="c6f9c23b1ac159d802d7ab082258c69b26544f9dc31f01aa8053e77d8a2b0a06")
    version("09.14.08", sha256="61fa67c3764f37112af55fff17ab3e573a9ae4b068b3c8e437aca184741d14a3")
    version("09.14.07", sha256="22483ee81137924c4864c7a38c936327f223a598048d6d0d2aecf11784ed2520")
    version("09.14.06", sha256="6e67c3e46d4b424886681ae95b3e2d8a74241a1862b5a3cc26e6ea59c55f4cfb")
    version(
        "09.03.09.01", sha256="162712cd2506c443799b5e055a63370977ce9384d7a88925f0fda030362b95bf"
    )
    version("09.03.06", sha256="e0eca0c9cdce510ec552151c5ced3e5821f97b479b632995ea43950e9a58eefc")
    version("09.03.05", sha256="017796fe891f12d1caaa17a12d753f47b263c0bdc8b44c14934b0d5d70ab82bd")
    version("09.03.04", sha256="8464e9e96f9dc3822bdd00e0bbad78004799bfab2c6ba066fe6a1770443a8fc0")
    version("09.03.03", sha256="21a81310d5f92f953cc51a7155aa524574336c7ef4a297027e63cb34e4cf74c2")
    version("09.03.02", sha256="b4a88aa04797dc74a05340d8706f543fb842e44542527fcef719b50ffa32ac7c")
    version("09.03.01", sha256="c6efb390d2af631b7efd0ddc3d709744642bad02cd8c7107fcc519d047e1a941")
    version("09.03.00", sha256="8394314e855c62735b9317eef219b7b452dcecba4d3cee24857c4764244b9b30")
    version("09.02.17", sha256="af487034b6e9106b863fbad341d47e36defac3e6ad3c2e84d97cee021407650a")
    version("09.02.16", sha256="517ee39ebdb1d55137799eb8cef5de783ad51b7c838f5271e3d5f29a0bc44105")
    version("09.02.15", sha256="95653ea8022539bf367da7938f9e9d284ce2791f80a31ba578bfdf5b5c74a75d")
    version("09.02.14", sha256="0aafe08d52d360d648e1d63905384103cfb3d167b632f3b469ad355312209f47")
    version("mwm1", tag="mwm1", git="https://github.com/marcmengel/larana.git", get_full_repo=True)
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

    patch("v09_03_06.patch", when="@09.03.06")
    patch("v09_03_09_01.patch", when="@09.03.09.01")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("larreco")
    depends_on("cetmodules", type="build")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]
        return args

    def setup_build_environment(self, spack_env):
        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False,
            cover="nodes",
            order="post",
            deptype=("link"),
            direction="children",
        ):
            spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.build_directory, "perllib"))
        # Cleaup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", self.prefix.bin)
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False,
            cover="nodes",
            order="post",
            deptype=("link"),
            direction="children",
        ):
            run_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        run_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        run_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
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

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
        return (flags, None, None)
