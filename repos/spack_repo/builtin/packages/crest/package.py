# Copyright 2013-2022 GWDG
# HPC team Developers
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Crest(Package):
    """Conformer-Rotamer Ensemble Sampling Tool"""

    homepage = "https://github.com/crest-lab/crest"
    url = "https://github.com/crest-lab/crest/releases/download/v2.12/crest.zip"

    version("2.12", sha256="c55e0f075a6223317b33a5f0fae593ce0ad55c1229c382937b0a0c2dcaf72ef6")

    depends_on("xtb")

    phases = ["install"]

    def install(self, spec, prefix):
        unzip = which("unzip")
        unzip(self.stage.archive_file, "-d", self.prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)
