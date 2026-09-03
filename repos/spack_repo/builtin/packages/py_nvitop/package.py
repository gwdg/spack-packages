# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyNvitop(PythonPackage):
    """
    An interactive NVIDIA-GPU process viewer and beyond,
    the one-stop solution for GPU process management.
    """

    homepage = "https://nvitop.readthedocs.io/"
    pypi = "nvitop/nvitop-1.4.0.tar.gz"

    maintainers("nboelte")

    license("Apache-2.0", checked_by="nboelte")

    version("1.7.1", sha256="3803112a1d4a7e01989ae5bf5a5e42f0366bf791d68ad8e3b1859d7ed747140c")
    version("1.6.2", sha256="267b341b66ac3819f116ad11819f4da2e121fe2be1dde979026b6526966211e9")
    version("1.5.3", sha256="ab50fbcfb986607d36f4dd07e124cb5582290d7f7efb2e1d97635b4487fac1fb")
    version("1.4.0", sha256="92f313e9bd89fe1a9d54054e92f490f34331f1b7847a89ddaffd6a7fde1437bb")

    depends_on("py-nvidia-ml-py@11.450.51:13.596.0a0", type=("build", "run"), when="@1.7.1")
    depends_on("py-nvidia-ml-py@11.450.51:13.591.0a0", type=("build", "run"), when="@1.6.2")
    depends_on("py-nvidia-ml-py@11.450.51:13.581.0a0", type=("build", "run"), when="@1.5.3")
    depends_on("py-nvidia-ml-py@11.450.51:12.561.0a0", type=("build", "run"), when="@1.4.0")
    depends_on("py-psutil@5.6.6:", type=("build", "run"))
    # The dependencies cachetools and termcolor were vendored in 1.4.2
    depends_on("py-cachetools@1.0.1:", type=("build", "run"), when="@:1.4.1")
    depends_on("py-termcolor@1.0.0:", type=("build", "run"), when="@:1.4.1")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    # Windows support would require the package py-windows-curses to be available in spack.
    # depends_on("py-colorama@0.4:", when="platform=windows", type=("build", "run"))
    # depends_on("py-windows-curses@2.2.0:", when="platform=windows", type=("build", "run"))
    conflicts("platform=windows")
