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
#     spack install fiji
#
# You can edit this file again by typing:
#
#     spack edit fiji
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack_repo.builtin.build_systems.maven import MavenPackage

from spack.package import *


class Fiji(MavenPackage):
    """Fiji is a "batteries-included" distribution of ImageJ, a popular, free scientific image processing application which includes a lot of plugins organized into a coherent menu structure. Fiji compares to ImageJ as Ubuntu compares to Linux.

    The main focus of Fiji is to assist research in life sciences.

    At the moment, the following platforms are supported:
      - Windows Intel 32-bit/64-bit
      - Linux Intel 32-bit/64-bit
      - MacOSX Intel 32-bit/64-bit (partial support for PowerPC 32-bit)
      - all platforms supporting Java and a POSIX shell, via bin/ImageJ.sh

    The setup is as easy as unpacking the portable archive and double-clicking the ImageJ launcher.
    Fiji is intended to be the most painless, easy, quick and convenient way to install ImageJ and plugins and keep everything up-to-date.
    """

    # Add a proper url for your package's homepage here.
    homepage = "https://imagej.net/"
    url = "https://github.com/fiji/fiji/archive/refs/tags/fiji-2.16.0.tar.gz"

    # Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list.
    license("GPL-3.0")

    version("2.17.0", sha256="ebb8de79fa7c950c0f8e8c8d0b2c17f9bcee5fb52b496eafcbfed74a419efc4d")
    version("2.16.0", sha256="77b089560a11e4092e1b88699f73d39a07c9bd7edd507b3854846157c53d1f9b")

    # Add dependencies if required.
    depends_on("java@8")
    depends_on("maven", type="build")

    @run_after("install")
    def populate(self):
        populate_path = self.prefix + "/bin/populate-app.sh"
        filter_file(r"^\s*test -z \"\$win32\".*", "", populate_path)
        filter_file(r"^\s*test -z \"\$win64\".*", "", populate_path)
        filter_file(r"^\s*test -z \"\$macosx\".*", "", populate_path)
        filter_file(r"^\s*test -z \"\$linux32\".*", "", populate_path)

        populate = Executable(populate_path)
        populate(self.prefix)

        launcher = Executable(self.prefix + "/bin/download-launchers.sh")
        launcher("release", "linux64")

    def setup_run_environment(self, env):
        env.remove_path("PATH", self.prefix.bin)
        env.append_path("PATH", self.prefix)
