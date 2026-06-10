# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Psi4(CMakePackage):
    """Psi4 is an open-source suite of ab initio quantum chemistry
    programs designed for efficient, high-accuracy simulations of
    a variety of molecular properties."""

    homepage = "https://www.psicode.org/"
    url = "https://github.com/psi4/psi4/archive/v1.3.2.tar.gz"

    version("1.10", sha256="2d0ffcec6ff61141fbf13e8ee7ba984e28fc268659f67833352303a6356cc4e4")
    version("1.9.1", sha256="ccd69bdc1d8319470513b4d3c1e0d737fc7788a50d7e48f8db762a0fcf795dad")
    # New version since the previous one failed to build @nboelte
    version("1.8.2", sha256="0b356f29e6eefa6496e5ad58e09b7d090f12971e2ccb3d824e787713f1dd4a82")
    version("1.3.2", sha256="ed76c67803b6420f35f57a6dd31c47108b9145b8c9fced5c94cdc179f6b5fbf3")

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )
    variant("ecpint", default=False, description="Build with LibECPInt support")

    # Required dependencies
    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("blas")
    depends_on("lapack")
    depends_on("boost+chrono+filesystem+python+regex+serialization+system+timer+thread")
    depends_on("python")
    depends_on("py-pydantic", type="run")
    depends_on("py-pint", type="run")
    depends_on("py-py-cpuinfo", type="run")
    depends_on("py-psutil", type="run")
    depends_on("py-scipy", type="run")
    depends_on("py-networkx", type="run")
    depends_on("py-msgpack", type="run")
    depends_on("cmake@3.3:", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pip", type=("build"))
    depends_on("py-setuptools", type=("build"))
    depends_on("eigen")

    # Optional dependencies
    # TODO: add packages for these
    # depends_on('perl')
    # depends_on('erd')
    # depends_on('pcm-solver')
    # depends_on('chemps2')

    def cmake_args(self):
        spec = self.spec

        cmake_args = [
            "-DBLAS_TYPE={0}".format(spec["blas"].name.upper()),
            "-DBLAS_LIBRARIES={0}".format(spec["blas"].libs.joined()),
            "-DLAPACK_TYPE={0}".format(spec["lapack"].name.upper()),
            "-DLAPACK_LIBRARIES={0}".format(spec["lapack"].libs.joined()),
            "-DBOOST_INCLUDEDIR={0}".format(spec["boost"].prefix.include),
            "-DBOOST_LIBRARYDIR={0}".format(spec["boost"].prefix.lib),
            "-DENABLE_CHEMPS2=OFF",
        ]
        if spec.satisfies("+ecpint"):
            cmake_args.append("-DENABLE_ecpint=ON")

        return cmake_args

    @run_after("install")
    def filter_compilers(self):
        """Run after install to tell the configuration files to
        use the compilers that Spack built the package with.

        If this isn't done, they'll have PLUGIN_CXX set to
        Spack's generic cxx. We want it to be bound to
        whatever compiler it was built with."""

        spec = self.spec
        prefix = spec.prefix

        kwargs = {"ignore_absent": True, "backup": False, "string": True}

        cc_files = ["bin/psi4-config"]
        cxx_files = ["bin/psi4-config", "include/psi4/psiconfig.h"]
        template = "share/psi4/plugin/Makefile.template"

        for filename in cc_files:
            filter_file(
                os.environ["CC"], self.compiler.cc, os.path.join(prefix, filename), **kwargs
            )

        for filename in cxx_files:
            filter_file(
                os.environ["CXX"], self.compiler.cxx, os.path.join(prefix, filename), **kwargs
            )

        # The binary still keeps track of the compiler used to install Psi4
        # and uses it when creating a plugin template
        filter_file("@PLUGIN_CXX@", self.compiler.cxx, os.path.join(prefix, template), **kwargs)

        # The binary links to the build include directory instead of the
        # installation include directory:
        # https://github.com/psi4/psi4/issues/410
        filter_file(
            "@PLUGIN_INCLUDES@",
            "-I{0}".format(
                " -I".join(
                    [
                        os.path.join(spec["psi4"].prefix.include, "psi4"),
                        os.path.join(spec["boost"].prefix.include, "boost"),
                        os.path.join(spec["python"].headers.directories[0]),
                        spec["lapack"].prefix.include,
                        spec["blas"].prefix.include,
                        spec["eigen"].prefix.include,
                        "/usr/include",
                    ]
                )
            ),
            os.path.join(prefix, template),
            **kwargs,
        )
