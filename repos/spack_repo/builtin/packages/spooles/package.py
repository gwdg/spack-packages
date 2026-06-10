# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Spooles(MakefilePackage):
    """SPOOLES is a library for solving sparse real and complex linear systems of equations."""

    homepage = "https://www.netlib.org/linalg/spooles/spooles.2.2.html"
    url = "https://www.netlib.org/linalg/spooles/spooles.2.2.tgz"

    license("UNKNOWN", checked_by="github_user1")

    version("2.2", sha256="a84559a0e987a1e423055ef4fdf3035d55b65bbe4bf915efaa1a35bef7f8c5dd")

    patch("invalid-cast-wint.patch")
    patch("invalid-cast-wint-factormpi.patch")
    patch("Make_inc.patch")

    depends_on("c", type="build")
    depends_on("mpi", type="build")

    def build(self, spec, prefix):
        make("lib", parallel=False)
        make(parallel=False)

    def install(self, spec, prefix):
        import os
        import shutil

        mkdirp(prefix.lib)

        install("spooles.a", prefix.lib + "/libspooles.a")

        if os.path.exists("MT/src/spoolesMT.a"):
            install("MT/src/spoolesMT.a", prefix.lib + "/libspoolesMT.a")

        for root, dirs, files in os.walk("."):
            for f in files:
                if not f.endswith(".h"):
                    continue
                src_path = os.path.join(root, f)
                rel_path = os.path.relpath(src_path, ".")
                dest_path = join_path(str(prefix.include), rel_path)
                mkdirp(os.path.dirname(dest_path))
                shutil.copy(src_path, dest_path)
