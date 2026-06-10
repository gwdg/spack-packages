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
#     spack install imagej
#
# You can edit this file again by typing:
#
#     spack edit imagej
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack_repo.builtin.build_systems.maven import MavenPackage

from spack.package import *


class Imagej(MavenPackage):
    """ImageJ is public domain software for processing and analyzing scientific images.
    It is written in Java, which allows it to run on many different platforms.
    For further information, see:
      The ImageJ website, the primary home of this project.
      The ImageJ wiki, a community-built knowledge base covering ImageJ and its derivatives and flavors, including ImageJ2, Fiji, and others.
      The ImageJ mailing list and Image.sc Forum for community support.
      The Contributing page of the ImageJ wiki for details on how to contribute.
    """

    # Add a proper url for your package's homepage here.
    homepage = "https://www.imagej.net"
    url = "https://github.com/imagej/ImageJ/archive/refs/tags/v1.54k.tar.gz"

    # Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list.
    license("UNKNOWN")

    version("1.54r", sha256="a80447365b2edcb24eacbd8c460fdae6a297686a9a03b6aab2ca014f0516304b")
    version("1.54p", sha256="afb1ddfdcc43828754936821a13f46061cba421d4ade0238368c951cb6e6103b")
    version("1.54k", sha256="85678e7f400c7dc53fbef7cc9c5bb951edda35e5225d1e82bcb757227adcdb2d")

    depends_on("java")
    depends_on("maven", type="build")

    patch("maven-source.patch")

    @run_after("install")
    def create_runner(self):
        target = self.prefix + "/target/ij-1.x-SNAPSHOT.jar"
        mkdir(self.prefix + "/bin")
        with open(self.prefix + "/bin/ImageJ.sh", "w") as f:
            f.write(
                '#!/bin/sh\nif ! command -v java 2>&1 >/dev/null; then\n  echo"Java not found ..."\nelse\n  exec java -jar '
                + target
                + "\nfi\n"
            )
            set_executable(self.prefix + "/bin/ImageJ.sh")
