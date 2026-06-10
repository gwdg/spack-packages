# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tkdiff(Package):
    """TkDiff is a graphical front end to the diff program.
    It provides a side-by-side view of the differences between two text files,
    along with several innovative features such as diff bookmarks,
    a graphical map of differences for quick navigation, and a facility
    for slicing diff regions to achieve exactly the merge output desired."""

    homepage = "https://tkdiff.sourceforge.io/"
    url = "https://downloads.sourceforge.net/project/tkdiff/tkdiff/5.7/tkdiff-5-7.zip"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers("github_user1", "github_user2")

    license("GPL-2.0-or-later")

    version("6.0", sha256="4fa27c87846c1d6635da5beaa90ce4561638ee25a9169e455175afcf5288e453")
    version("5.7", sha256="e2dec98e4c2f7c79a1e31290d3deaaa5915f53c8220c05728f282336bb2e405d")

    def url_for_version(self, version):
        url = "https://downloads.sourceforge.net/project/tkdiff/tkdiff/{}/tkdiff-{}.zip"
        return url.format(version, version.dashed)

    depends_on("tk")

    def install(self, spec, prefix):
        mkdirp(prefix.doc)
        mkdirp(prefix.bin)
        install("README.txt", prefix.doc)
        install("LICENSE.txt", prefix.doc)
        install("tkdiff", prefix.bin)
