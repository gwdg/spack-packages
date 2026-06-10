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
#     spack install chimerax
#
# You can edit this file again by typing:
#
#     spack edit chimerax
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os

from spack.package import *


class Chimerax(Package):
    """UCSF ChimeraX (or simply ChimeraX) is the next-generation molecular visualization program from the Resource for Biocomputing, Visualization, and Informatics (RBVI), following UCSF Chimera."""

    # Add a proper url for your package's homepage here.
    homepage = "https://www.cgl.ucsf.edu/chimerax/"

    # Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list.
    license("UNKNOWN")

    version(
        "1.9",
        url="file:///opt/sw/mirror/chimerax/ucsf-chimerax-1.9-1.el8.x86_64.rpm.tgz",
        sha256="643e55c5732f29a0eb9004406e93187a31ca81050ba6109f17c3ce6a560055ec",
        expand=False,
    )

    # Add dependencies if required.
    depends_on("ffmpeg")
    depends_on("libffi")

    def install(self, spec, prefix):
        tar = which("tar")
        tar("-xf", self.stage.archive_file, "-C", prefix)

        for f in os.listdir(prefix + "/usr/libexec/UCSF-ChimeraX"):
            move(prefix + "/usr/libexec/UCSF-ChimeraX/" + f, prefix)

        rmtree(prefix + "/usr")

    def setup_run_environment(self, env):
        # Allow QtWebEngine (or its underlying chromium process) to run on a node without user network namespaces
        env.set("QTWEBENGINE_DISABLE_SANDBOX", "1")
