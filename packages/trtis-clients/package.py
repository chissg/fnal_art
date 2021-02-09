# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

# decorator to try a method twice...
def tryagain(f):
    def double_f(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except:
            f(*args, **kwargs)
    return double_f

class TrtisClients(CMakePackage):
    """C++ client code for Triton Inference Server."""

    homepage = "https://github.com/triton-inference-server/server"
    url      = "https://github.com/triton-inference-server/server/archive/v2.6.0.tar.gz"

    maintainers = ['marcmengel', 'github_user2']

    version('2.6.0',                    sha256='c4fad25c212a0b5522c7d65c78b2f25ab0916ccf584ec0295643fec863cb403e')

    variant('cuda', default=False)

    depends_on('cmake@3.18:', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-grpcio', type=('build','run'))
    depends_on('py-grpcio-tools', type=('build','run'))
    depends_on('py-numpy')
    depends_on('py-geventhttpclient')
    depends_on('py-python-rapidjson')
    depends_on('rapidjson')
    depends_on('protobuf')
    depends_on('googletest')
    depends_on('google-cloud-cpp')
    depends_on('crc32c')
    depends_on('c-ares')
    depends_on('libb64')
    depends_on('libevent')
    depends_on('libevhtp')
    depends_on('grpc')
    depends_on('prometheus-cpp')
    depends_on('curl@7.56:')
    depends_on('opencv ~videoio~gtk~java~vtk~jpeg', when='~cuda')
    depends_on('opencv ~videoio~gtk~java~vtk~jpeg+cuda+contrib', when='+cuda')
    depends_on('cuda', when='+cuda')
    depends_on('nccl', when='+cuda')
    
    patch('fix_compile_flags.patch')
    patch('use_existing.patch')

    root_cmakelists_dir = 'build'

    # trying doubled build...
    build = tryagain(CMakePackage.build)
  
    def cmake_args(self):
        args = [
            '-DCMAKE_BUILD_TYPE=Release',
            '-DCMAKE_C_COMPILER=cc',
            '-DCMAKE_CXX_COMPILER=c++',
            '-DTRITON_CURL_WITHOUT_CONFIG:BOOL=ON',
        ]

        if ('+cuda' in self.spec):
            args.append('-DTRITON_ENABLE_GPU:BOOL=ON')
            args.append('-DTRITON_ENABLE_METRICS_GPU:BOOL=ON')
        else:
            args.append('-DTRITON_ENABLE_GPU:BOOL=OFF')
            args.append('-DTRITON_ENABLE_METRICS_GPU:BOOL=OFF')

        return args

    #
    # we want our cmake/modules directory in the CMAKE_PREFIX_PATH
    # but its built in _std_args(), and we want all that plus ours...
    #
    @property
    def std_cmake_args(self):
        std_cmake_args = CMakePackage._std_args(self)
        fixed = []
        for arg in std_cmake_args:
            if arg.startswith("-DCMAKE_PREFIX_PATH:STRING="):
                fixed.append(arg + ";" + self.stage.source_path +'/cmake/modules')
            else:
                fixed.append(arg)
        return fixed

    #
    # also push our cmake/modules on the environment CMAKE_PREFIX_PATH for  ExternalPackage calls...
    #
    def setup_build_environment(self, env):
        env.prepend_path('CMAKE_PREFIX_PATH', self.stage.source_path +'/cmake/modules')
        pass

    def flag_handler(self, name, flags):
        if name == 'cxxflags' and  self.spec.compiler.name == 'gcc':
            flags.append('-Wno-error=deprecated-declarations')
            flags.append('-Wno-error=class-memaccess')
        return (flags, None, None)

    def install(self, spec, prefix):
        install_tree(self.stage.source_path+'/install/include', prefix+'/include/trts_clients')
        install_tree(self.stage.source_path+'/install/lib', prefix+'/lib')

