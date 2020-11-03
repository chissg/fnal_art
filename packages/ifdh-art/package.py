# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
libdir="%s/var/spack/repos/fnal_art/lib" % os.environ["SPACK_ROOT"]
if not libdir in sys.path:
    sys.path.append(libdir)
from cetmodules_patcher import cetmodules_20_migrator


def patcher(x):
    cetmodules_20_migrator(".","artg4tk","9.07.01")



class IfdhArt(CMakePackage):
    """The ifdh_art package provides ART service access to the libraries 
from the ifdhc package."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/ifdh-art/wiki"
    url      = "https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git"

    patch = patcher

    version('MVP1a', git='https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', branch='feature/Spack-MVP1a')
    version('2.10.02',  git='https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', tag='v2_10_02')
    version('2.10.01',  git='https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', tag='v2_10_01')
    version('2.10.00',  git='https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', tag='v2_10_00')
    version('2.10.02',  git='https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', tag='v2_10_02')
    version('2.10.04',  git='https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', tag='v2_10_04')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('art')
    depends_on('ifdhc')
    depends_on('ifbeam')
    depends_on('nucondb')
    depends_on('libwda')
    depends_on('cetmodules@2.00:', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)               ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)

