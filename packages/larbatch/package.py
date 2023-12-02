# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Larbatch(Package):
    """package for batch job submission featuring project.py"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larbatch-web-client/wiki"
    url = "https://github.com/LArSoft/larbatch/archive/refs/tags/v01_51_15.tar.gz"

    version("01_59_03", sha256="9c32bc2c2f6a86df58409fda7468e02f02360580bfc367098cc459b83cc21883")
    version("01_51_15", sha256="0a105ec7deb46a9a16a31ab1e8f0864417be9e2fbe770542e9793b10424dbbd0")

    depends_on("sam-web-client", type=("run"))
    depends_on("python", type=("run"))

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PYTHONPATH", self.prefix.bin)
        run_env.prepend_path("PYTHONPATH", self.prefix + "/python")
