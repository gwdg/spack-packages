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
#     spack install dynamo
#
# You can edit this file again by typing:
#
#     spack edit dynamo
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Dynamo(Package):
    """Dynamo is a software environment for subtomogram averaging of cryo-EM data."""

    homepage = "https://www.dynamo-em.org/w/index.php?title=Main_Page"

    # Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list.
    license("UNKNOWN")

    # Add proper versions here.
    version(
        "1.1.552",
        url="file:///opt/sw/mirror/dynamo/dynamo-v-1.1.552_MCR-24.1.0_GLNXA64.tar",
        sha256="d6d7bcaa2dff711a74999207c09b9358aa08e4c2c211b7be097e4cbbaa0833b0",
        expand=False,
    )

    # FIXME: Add dependencies if required.
    # depends_on("foo")

    def install(self, spec, prefix):
        # This package only needs to be extracted
        tar = which("tar")
        tar("-xf", self.stage.archive_file, "-C", prefix)
