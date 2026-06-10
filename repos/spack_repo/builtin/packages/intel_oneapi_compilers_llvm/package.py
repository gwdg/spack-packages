# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class IntelOneapiCompilersLlvm(Package):
    """The internal LLVM components of the Intel oneAPI Compilers.
    Includes: clang, clang++, llvm-ar, llvm-profgen, ..."""

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi.html"

    has_code = False

    version("2025.3.2")

    depends_on("intel-oneapi-compilers@2025.3.2", type="run", when="@=2025.3.2")

    def install(self, spec, prefix):
        # Symlink executables similar to intel-oneapi-compilers-classic
        mkdirp(prefix.bin)

        oneapi_pkg = self.spec["intel-oneapi-compilers"].package

        llvm_prefix = oneapi_pkg.component_prefix.bin.compiler

        for entry in os.listdir(llvm_prefix):
            src_path = os.path.join(llvm_prefix, entry)
            dest_path = os.path.join(prefix.bin, entry)

            os.symlink(src_path, dest_path)
