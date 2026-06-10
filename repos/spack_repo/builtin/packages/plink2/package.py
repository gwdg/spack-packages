# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Plink2(MakefilePackage):
    """PLINK2: Whole genome association analysis toolset, designed to perform a
    range of basic, large-scale analyses in a computationally efficient manner."""

    homepage = "https://www.cog-genomics.org/plink/2.0/"
    url = "https://github.com/chrchang/plink-ng/archive/refs/tags/v2.00a5.11.tar.gz"
    list_url = "https://github.com/chrchang/plink-ng/tags"

    license("GPLv3", checked_by="teaguesterling")
    # See: https://github.com/chrchang/plink-ng/blob/master/2.0/COPYING

    maintainers("teaguesterling")

    version(
        "2.0.0-a6.32", sha256="9d529d6fd5d1cf2893e36920db0b1ff4e6bad96fb9fa60a2ceee7b1e94dd8aab"
    )
    version(
        "2.0.0-a5.39", sha256="d91d0e80c40ffe805f73c49cc12f2ec5e0e4db40be51e209b6318665d1c0878b"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")
    depends_on("zlib@1.2.12:", when="^[virtuals=zlib-api] zlib")
    depends_on("zstd@1.5.2:")
    depends_on("libdeflate@1.10:")
    depends_on("blas")
    depends_on("lapack")

    # TODO: MKL support with gomp needs multiple changes to the makefile
    conflicts("intel-oneapi-mkl")

    build_directory = "2.0/build_dynamic"

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            makefile = FileFilter("Makefile")
            if "avx2" in spec.target:
                makefile.filter(r"^NO_AVX2 = 1", "NO_AVX2 =")
            elif "sse4_2" in spec.target:
                makefile.filter(r"^NO_SSE42 = 1", "NO_SSE42 =")
            makefile.filter(r"^STATIC_ZSTD = 1", "STATIC_ZSTD =")
            if self.spec["blas"].package.name == "amdblis":
                makefile.filter(
                    r"^([ ]*CFLAGS[ ]*=.*)$",
                    r"\1  " + self.spec["blas"].headers.include_flags + "/blis",
                )
                makefile.filter(
                    r"^([ ]*CXXFLAGS[ ]*=.*)$",
                    r"\1 " + self.spec["blas"].headers.include_flags + "/blis",
                )
            makefile.filter(
                r"^[ ]*BLASFLAGS=-llapack -lblas -lcblas -latlas",
                "BLASFLAGS={0} {1}".format(
                    spec["blas"].libs.ld_flags, spec["lapack"].libs.ld_flags
                ),
            )

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make()

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        with working_dir(self.build_directory):
            install("plink2", prefix.bin)
            install("pgen_compress", prefix.bin)
