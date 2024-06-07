# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
import os
import shutil


class Btrk(SConsPackage):
    """Mu2e experiment: Refactoring BField Interface package
    """

    homepage = "https://github.com/KFTrack/Btrk#readme"
    url = "https://github.com/KFTrack/BTrk/archive/refs/tags/v1_02_43.tar.gz"

    version("1.02.46", sha256="5cc136cef7835a9cc792cd857b6fb6e94e788fd1ace07938d4599562e6740e4d")
    version("1.02.45", sha256="59d7c5afdedadb774c8a2c5ba3bbbe003d7cb09510c7a44d280cef4f511059a8")
    version("1.02.43", sha256="55eb787f156f380c80240b9f91d99963db47f015988d4cbdd3ee09e95af7759e")
    version("1.02.41", sha256="4b233ebe252f82a1f4d857c04b44c6a62a49049ed69172cb347a1b180b50770c")

    def url_for_version(self, version):
        url = "https://github.com/KFTrack/BTrk/archive/refs/tags/v{0}.tar.gz"
        return url.format(version.underscored)

    depends_on("root")
    depends_on("clhep")

    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )

    def patch(self):
        filter_file(r"for var in \[ 'LD_LIBRARY_PATH',  'GCC_FQ_DIR',  'PATH', 'PYTHONPATH',  'ROOTSYS', 'PYTHON_ROOT', 'PYTHON_DIR' \]:",
                r"for var in os.environ.keys():",
                    "%s/spack-src/python/helpers.py" % self.stage.path)
        filter_file(r'(std=c\+\+)17', r'\1%s' % self.spec.variants["cxxstd"].value,
                    "%s/spack-src/python/helpers.py" % self.stage.path)
        filter_file(r"(os.environ\['ROOTSYS'\] \+ '/lib',)",
                    r"\1 os.environ['ROOTSYS'] + '/lib/root',",
                    "%s/spack-src/SConstruct" % self.stage.path)

    def build_args(self, spec, prefix):
        args = []
        return args

    def install(self, spec, prefix):
        move('%s/lib' % self.stage.source_path, prefix.lib)
        install_tree(self.stage.source_path, prefix.source)
        mkdirp(prefix.include)
        headerlist = find_all_headers(self.stage.source_path)
        for d in headerlist.directories:
            mkdirp(join_path(prefix.include, os.path.relpath(d,self.stage.source_path)))
        for f in headerlist.headers:
             install(f, join_path(prefix.include, os.path.relpath(f,self.stage.source_path)))

    def setup_build_environment(self, env):
        env.append_path("PYTHONPATH", "%s/spack-src/python" % self.stage.path)
        env.set("BUILD_BASE", "%s/build" % self.stage.path)
        env.set("PACKAGE_SOURCE", "%s/spack-src" % self.stage.path)
        env.set("CLHEP_INC", "%s" % self.spec["clhep"].prefix.include)
        env.set("CLHEP_LIB_DIR", "%s" % self.spec["clhep"].prefix.lib)
        env.set("ROOT_INC", "%s/include/root" % self.spec["root"].prefix)
        env.set("GCC_VERSION", "{}".format(self.spec.compiler.version))
        env.set("DEBUG_LEVEL", "prof")
        env.set("BTRK_INC", prefix.include)

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        env.set("BTRK_INC", prefix.include)
