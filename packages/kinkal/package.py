# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
import os

class Kinkal(CMakePackage):
    """Kinematic Kalman filter track fit code package"""

    homepage = "https://github.com/KFTrack/KinKal#readme"
    url = "https://github.com/KFTrack/KinKal/archive/refs/tags/v2.4.2.tar.gz"

    # notify when the package is updated.
    # maintainers("github_user1", "github_user2")
    maintainers = ['mengel']

    version("2.5.0", sha256="45bfd2fd9b0eea7f78345bf31d280baf6ae17214a3afab97a54bd6c02a332017")
    version("2.4.3", sha256="543b9b3569242f298c7c433ba45945e38a440c4fb410029946318d2e2202ee6e")
    version("2.4.2", sha256="7a9aebf925fb2f354ccd5483078661767db7ced59e826ce234effe0e7bc49aa7")
    version("2.4.1", sha256="ee239f6f9d396d02da6523fb4961f78c55494439775ffcef83aa1362854d2f19")
    version("2.4.0", sha256="638323087e11d03a10f6499080ef8e5a6edcb976f79843ee39b81bfbda3dca2a")
    version("2.3.1", sha256="25dbfcbd684010cd61eb34b46c4416a52ca53ab1c95b5d9e20f551da5cab2fbb")
    version("2.3.0", sha256="33522e797cbfa0b4953de74028ef573ffe7c2067eafa4d27bc51627b1c64ab6d")
    version("2.2.1", sha256="6fa99d0d4265d7d857936f02f2d2a605e2d6109b7e017f74568ef2f2cf4525c3")
    version("2.2.0", sha256="a3e4269339dd3cebdd709aa7d474dc5a5db905c2181cf9d5e08bd9233c4ec895")
    version("2.1.0", sha256="8232f5e9862db1dc2c73bad1e52b64b8524c2be1d7ea966943f27516b6f34fae")
    version("2.0.1", sha256="d845e1232168dd22b8e1b2ddde6ff4da6f511c81aa8b56c2cf64b9dfa27c0203")
    version("2.0.0", sha256="90286168ebf222fdc227adcbb8fed0b60208f7431511afe128f85f1e76fc10b0")

    depends_on("root+mlp")

    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )

    def patch(self):
        filter_file(
            r"(set\(CMAKE_CXX_STANDARD )17\)",
            r"\1 %s)" % self.spec.variants["cxxstd"].value,
            "CMakeLists.txt",
        )

    def cmake_args(self):
        args = ["-DPROJECT_SOURCE_DIR=%s" % self.stage.source_path, self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),]
        return args

    @run_before('build')
    def makelink(self):
        with working_dir(self.stage.path):
            os.symlink('%s/spack-src' % self.stage.path, '%s/KinKal' % self.stage.path)

    @run_after('install')
    def copy_headers(self):
        with working_dir(self.stage.path):
            copy('%s/spack-src/General/PhysicalConstants.h' % self.stage.path,
                    '%s/include/KinKal/General/PhysicalConstants.h' % self.prefix)
            copy('%s/spack-src/General/SystemOfUnits.h' % self.stage.path,
                    '%s/include/KinKal/General/SystemOfUnits.h' % self.prefix)
