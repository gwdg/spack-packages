# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install chimera
#
# You can edit this file again by typing:
#
#     spack edit chimera
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os

from spack.package import *


class Chimera(Package):
    """UCSF CHIMERA: an Extensible Molecular Modeling System"""

    homepage = "https://www.cgl.ucsf.edu/chimera/"

    license("UNKNOWN")

    # Add proper versions here.
    version(
        "1.18",
        url="file:///opt/sw/mirror/chimera/chimera-1.18-linux_x86_64.bin",
        sha256="fe3558a2f27eb77f83632227f187614b69f448b518375a8ae681eccbf70682fd",
        expand=False,
    )

    # Add dependencies if required.
    depends_on("unzip", type=("build"))

    def install(self, spec, prefix):
        unzip = which("unzip")
        unzip(self.stage.archive_file)

        set_executable(os.getcwd() + "/chimera.bin")
        installer = Executable(os.getcwd() + "/chimera.bin")
        installer("-d", prefix)

        set_executable(prefix + "/bin/.compileall")
        compileall = Executable(prefix + "/bin/.compileall")
        filter_file(r"^PATH=/bin.*$", "CHIMERA=" + prefix, prefix + "/bin/.compileall")
        compileall(fail_on_error=False)
