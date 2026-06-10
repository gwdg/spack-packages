# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Transabyss(Package):
    """de novo assembly of RNA-Seq data using ABySS"""

    git = "https://github.com/bcgsc/transabyss.git"

    version(
        "2.0.1",
        url="https://github.com/bcgsc/transabyss/releases/download/2.0.1/transabyss-2.0.1.zip",
        sha256="542779af2d1232ca872a57b922cfd32e1c6e9e7e0b5fae56ef2e7682dfdf6040",
        expand=False,
    )

    # Build dependencies
    depends_on("python", type=("build", "run"))
    depends_on("abyss", type=("build", "run"))
    depends_on("py-igraph", type=("build", "run"))
    depends_on("blat", type=("build", "run"))

    def install(self, spec, prefix):
        bsdtar = which("bsdtar")
        bsdtar("-xvzf", self.stage.archive_file, "-C", self.prefix, "--strip-components=1")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)
