# Copyright 2024 GWDG
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Clpeak(CMakePackage):
    """Simple OpenCL performance benchmark tool."""

    homepage = "https://github.com/krrishnarraj/clpeak"
    url = "https://github.com/krrishnarraj/clpeak/archive/1.1.4.tar.gz"

    version("1.1.4", sha256="c9ba6d46d17e94fe8074821047a6d59b011e600293ec27b8c52dd04370fcff5d")
    version("1.1.3", sha256="207650bb0ef4f35e137153b307cd75ec3e573284fee1a6ed63668f674eb0aef5")
    version("1.1.2", sha256="7bc7beba6b3307290650abc4f13fe9389b271c1a64601fa333461516950d745b")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.5:", type="build")

    depends_on("opencl@1.2:")
    depends_on("opencl-clhpp", type="build")
