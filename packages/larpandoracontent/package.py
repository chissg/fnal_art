# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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


class Larpandoracontent(CMakePackage):
    """Larpandoracontent"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larpandoracontent/wiki"
    git = "https://github.com/LArSoft/larpandoracontent.git"
    url = "https://github.com/LArSoft/larpandoracontent/archive/refs/tags/v03_26_01.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larpandoracontent/tags"

    version("develop", branch="develop", get_full_repo=True)
    version("04.08.01", sha256="6fecd809d9736a61f324a7bbb60baf0d6f36908470e233fc71b73ce455cc3f4f")
    version("04.08.00", sha256="0baa41654f706244dc2585565c675475c59ab99c7d97fadd4bbd6e991d64fe92")
    version("04.07.02", sha256="cfeccd40c01245b92446dc1043b7914641f3487d1c43c44a3a2b676a320fca50")
    version("04.07.01", sha256="d0161c65b15c976f63b1712a0d1b1c1ba13cd019b5e3208d20059cb063a6e70b")
    version("04.07.00", sha256="1b8649d221ec03d3521b6dc69863e23b7fafc3e4c56a29560b3fe0d58ff70bbb")
    version("04.06.02", sha256="6727acb9cd22827b993eb69091037ab1434ef61369495f5abc7ac3b6b1c982a9")
    version("04.06.01", sha256="8125390bf354e7da7be41870cfb3c3bf65dd021a9b55eb0545a95c60fdcdfb9b")
    version("04.06.00", sha256="c78118cf8bebace0922a9561f06f6359b54bc69d3a7a1ae59b5bb2fa32f9565a")
    version("04.05.01", sha256="97b1d27fb9652cfa36e14bcdc5385914ba1c79c747b182b64c7f0f3861336136")
    version("04.05.00", sha256="6556e1ebbd1d1a68b876ac0e732c38b90cdc8896ea5f6d2c5bddafec6506b439")
    version(
        "03.26.01.01", sha256="f7c38678f3b7631df1287ca63ee3479d62c33b6d82134e9b98b7e6de90c4ce5c"
    )
    version("03.26.01", sha256="fdd00d2b3954fe2388ed5e754ffe2f82bea6f627bf037e6d6b799555b0afef96")
    version(
        "mwm1",
        tag="mwm1",
        git="https://github.com/marcmengel/larpandoracontent.git",
        get_full_repo=True,
    )
    version("03.22.11.01", tag="v03_22_11_01", get_full_repo=True)

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

    # patch('v03_26_01.patch', when='@03.26.01')
    patch("v03_26_01_01.patch", when="@03.26.01.01")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    variant("monitoring", default=True, description="Enable PandoraMonitoring when building.")

    depends_on("cetmodules", type="build")
    depends_on("eigen")
    depends_on("pandora +monitoring", when="+monitoring")
    depends_on("pandora ~monitoring", when="~monitoring")
    depends_on("py-torch")

    def patch(self):
        filter_file(r"set\(PANDORA_MONITORING TRUE\)", "", "CMakeLists.txt")

        if not self.spec.variants["monitoring"].value:
            filter_file(
                r"(PandoraPFA::PandoraMonitoring|MONITORING)",
                "",
                "larpandoracontent/CMakeLists.txt",
            )

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-DCMAKE_MODULE_PATH={0}/cmakemodules".format(self.spec["pandora"].prefix),
            "-DPANDORA_MONITORING={0}".format(
                "ON" if self.spec.variants["monitoring"].value else "OFF"
            ),
            "-DLAR_CONTENT_LIBRARY_NAME=LArPandoraContent",
            "-DPandoraSDK_DIR={0}/cmakemodules".format(self.spec["pandora"].prefix),
            "-DPandoraMonitoring_DIR={0}/cmakemodules".format(self.spec["pandora"].prefix),
            "-DCMAKE_PREFIX_PATH={0}/lib/python{1}/site-packages/torch".format(
                self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2)
            ),
        ]
        return args

    def setup_build_environment(self, env):
        env.set("CETBUILDTOOLS_VERSION", "cetmodules")

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", self.prefix.bin)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.append_path("CET_PLUGIN_PATH", self.prefix.lib)

