# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class CalculixAdapter(MakefilePackage):
    """preCICE adapter for CalculiX - provides the ccx_preCICE coupled solver executable."""

    homepage = "https://precice.org/adapter-calculix-get-adapter.html"
    url = "https://github.com/precice/calculix-adapter/archive/refs/tags/v2.20.1.tar.gz"

    license("GPL-3.0-only")

    version("2.20.1", sha256="3372e0d66321c2173899e1db4841c6c4f3c16ffb99067c36dba04e8a34e35d39")

    resource(
        name="ccx_src",
        url="http://www.dhondt.de/ccx_2.20.src.tar.bz2",
        sha256="63bf6ea09e7edcae93e0145b1bb0579ea7ae82e046f6075a27c8145b72761bcf",
        placement="ccx_src",
        when="@2.20.1",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
    depends_on("mpi", type="build")
    depends_on("precice")
    depends_on("spooles")
    depends_on("arpack-ng")
    depends_on("lapack")
    depends_on("blas")
    depends_on("yaml-cpp")

    def edit(self, spec, prefix):
        import glob
        import os

        mf = FileFilter("Makefile")

        mf.filter(r"^CCX\s*=.*", "CCX = ccx_src/ccx_2.20/src")

        mf.filter(
            r"^SPOOLES_INCLUDE\s*=.*",
            "SPOOLES_INCLUDE = -I{0}".format(spec["spooles"].prefix.include),
        )
        mf.filter(
            r"^SPOOLES_LIBS\s*=.*",
            "SPOOLES_LIBS = {0} {1}".format(
                join_path(str(spec["spooles"].prefix.lib), "libspoolesMT.a"),
                join_path(str(spec["spooles"].prefix.lib), "libspooles.a"),
            ),
        )

        mf.filter(r"^ARPACK_INCLUDE\s*=.*", "ARPACK_INCLUDE = ")

        arpack_lib = None
        for libdir in ("lib", "lib64", "lib32"):
            candidates = glob.glob(join_path(str(spec["arpack-ng"].prefix), libdir, "libarpack*"))
            if candidates:
                arpack_lib = candidates[0]
                break

        if arpack_lib is None:
            raise InstallError("libarpack not found under {0}".format(spec["arpack-ng"].prefix))

        mf.filter(
            r"^ARPACK_LIBS\s*=.*",
            "ARPACK_LIBS = {0} {1} {2}".format(
                arpack_lib, spec["blas"].libs.ld_flags, spec["lapack"].libs.ld_flags
            ),
        )

        mf.filter(
            r"^YAML_INCLUDE\s*=.*", "YAML_INCLUDE = -I{0}".format(spec["yaml-cpp"].prefix.include)
        )
        mf.filter(
            r"^YAML_LIBS\s*=.*", "YAML_LIBS = -L{0} -lyaml-cpp".format(spec["yaml-cpp"].prefix.lib)
        )

        mf.filter(r"-Wall\s+-O3\s+-fopenmp", "-Wall -O3 -fopenmp -fallow-argument-mismatch")

        precice_lib = (
            str(spec["precice"].prefix.lib64)
            if os.path.isdir(str(spec["precice"].prefix.lib64))
            else str(spec["precice"].prefix.lib)
        )

        mf.filter(
            r"\$\(shell pkg-config --cflags libprecice\)",
            "-I{0}".format(spec["precice"].prefix.include),
        )
        mf.filter(
            r"\$\(shell pkg-config --libs libprecice\)", "-L{0} -lprecice".format(precice_lib)
        )

        if spec.satisfies("%gcc@14:") or spec.satisfies("%oneapi"):
            mf.filter(r"^(CFLAGS\s*=.*)", r"\1 -Wno-error=implicit-function-declaration")

        if spec.satisfies("%gcc@15:"):
            mf.filter(r"^(CFLAGS\s*=.*)", r"\1 -Wno-error=incompatible-pointer-types")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("bin/ccx_preCICE", join_path(prefix.bin, "ccx_preCICE"))
