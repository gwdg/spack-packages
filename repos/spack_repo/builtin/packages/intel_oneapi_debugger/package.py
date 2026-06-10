# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class IntelOneapiDebugger(Package):
    """Intel® oneAPI Application Debugger (gdb-oneapi)"""

    homepage = (
        "https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-gdb.html"
    )

    has_code = False

    version("2025.3.2")

    depends_on("intel-oneapi-compilers@2025.3.2", type="run", when="@=2025.3.2")

    def install(self, spec, prefix):
        # Symlink executables similar to intel-oneapi-compilers-classic
        mkdirp(prefix.bin)

        compiler_prefix = self.spec["intel-oneapi-compilers"].prefix

        gdb_prefix = compiler_prefix.debugger.join(str(self.spec.version.up_to(2)))

        for entry in os.listdir(gdb_prefix.bin):
            src_path = os.path.join(gdb_prefix.bin, entry)
            dest_path = os.path.join(prefix.bin, entry)

            os.symlink(src_path, dest_path)
        os.symlink(gdb_prefix.lib, prefix.lib)
        os.symlink(gdb_prefix.opt, prefix.opt)
        os.symlink(gdb_prefix.share, prefix.share)

    def setup_run_environment(self, env):

        compiler_prefix = self.spec["intel-oneapi-compilers"].prefix
        gdb_prefix = compiler_prefix.debugger.join(str(self.spec.version.up_to(2)))

        env.prepend_path("LD_LIBRARY_PATH", gdb_prefix.lib)
        env.set("INTEL_PYTHONHOME", gdb_prefix.opt.debugger)
        env.prepend_path("MANPATH", gdb_prefix.share.man)
        env.prepend_path("INFOPATH", gdb_prefix.share.info)
        env.prepend_path("GDB_INFO", gdb_prefix.share.info)
