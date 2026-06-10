# Copyright 2025 GWDG
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Ffnvcodec(MakefilePackage):
    """FFmpeg version of headers required to interface with Nvidias codec APIs."""

    homepage = "https://git.videolan.org/?p=ffmpeg/nv-codec-headers.git"
    url = "https://git.videolan.org/git/ffmpeg/nv-codec-headers.git"
    git = "https://git.videolan.org/git/ffmpeg/nv-codec-headers.git"

    license("MIT")

    version("13.0.19.0", tag="n13.0.19.0")
    version("12.2.72.0", tag="n12.2.72.0")
    version("12.1.14.0", tag="n12.1.14.0")
    version("12.0.16.1", tag="n12.0.16.1")
    version("12.0.16.0", tag="n12.0.16.0")
    version("11.1.5.3", tag="n11.1.5.3")

    depends_on("gmake", type="build")
    depends_on("sed", type="build")

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("PKG_CONFIG_PATH", self.prefix.lib.pkgconfig)

    def build(self, spec, prefix):
        make("all", f"PREFIX={self.prefix}")

    def install(self, spec, prefix):
        make("install", f"PREFIX={self.prefix}")
