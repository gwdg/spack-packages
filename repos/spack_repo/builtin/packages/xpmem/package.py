# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Xpmem(AutotoolsPackage):
    """XPMEM is a Linux kernel module that enables a process to map the memory
    of another process into its virtual address space."""

    # Development has moved to https://github.com/openucx/xpmem
    homepage = "https://github.com/openucx/xpmem"
    url = "https://github.com/openucx/xpmem/archive/v2.7.4.tar.gz"
    git = "https://https://github.com/openucx/xpmem.git"

    maintainers("skosukhin")

    license("LGPL-2.1-or-later")

    # Released versions:
    version("2.7.4", sha256="738c70041ce09dcc66b64d80aebc1479e779efe12a9c02217fba610e2ae61f18")

    depends_on("c", type="build")  # generated

    variant("kernel-module", default=False, description="Enable building the kernel module")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    # Ideally, we should list all non-Linux-based platforms here:
    conflicts("+kernel-module", when="platform=darwin")

    # All compilers except for gcc are in conflict with +kernel-module:
    requires("%gcc", when="+kernel-module", msg="Linux kernel module must be compiled with gcc")

    def autoreconf(self, spec, prefix):
        Executable("./autogen.sh")()

    @run_before("build")
    def override_kernel_compiler(self):
        # Override the compiler for kernel module source files. We need
        # this additional argument for all installation phases.
        if "+kernel-module" in self.spec:
            make.add_default_arg("CC={0}".format(spack_cc))

    def configure_args(self):
        args = []

        if "~kernel-module" in self.spec:
            # The kernel module is enabled by default. An attempt of explicit
            # enabling with '--enable-kernel-module' disables the module.
            args.append("--disable-kernel-module")

        return args
