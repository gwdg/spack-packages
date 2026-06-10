# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Pocl(CMakePackage):
    """Portable Computing Language (pocl) is an open source implementation
    of the OpenCL standard which can be easily adapted for new targets
    and devices, both for homogeneous CPU and heterogeneous
    GPUs/accelerators."""

    homepage = "https://portablecl.org"
    url = "https://github.com/pocl/pocl/archive/v1.1.tar.gz"
    git = "https://github.com/pocl/pocl.git"

    license("MIT")

    version("main", branch="main")
    version("7.1", sha256="1110057cb0736c74819ad65238655a03f7b93403a0ca60cdd8849082f515ca25")
    version("7.0", sha256="f55caba8c3ce12bec7b683ce55104c7555e19457fc2ac72c6f035201e362be08")
    version("6.0", sha256="de9710223fc1855f833dbbf42ea2681e06aa8ec0464f0201104dc80a74dfd1f2")
    version("5.0", sha256="fd0bb6e50c2286278c11627b71177991519e1f7ab2576bd8d8742974db414549")
    version("4.0", sha256="7f4e8ab608b3191c2b21e3f13c193f1344b40aba7738f78762f7b88f45e8ce03")
    version("3.1", sha256="82314362552e050aff417318dd623b18cf0f1d0f84f92d10a7e3750dd12d3a9a")
    version("3.0", sha256="a3fd3889ef7854b90b8e4c7899c5de48b7494bf770e39fba5ad268a5cbcc719d")
    version("1.8", sha256="0f63377ae1826e16e90038fc8e7f65029be4ff6f9b059f6907174b5c0d1f8ab2")
    version("1.7", sha256="5f6bbc391ba144bc7becc3b90888b25468460d5aa6830f63a3b066137e7bfac3")
    version("1.6", sha256="b0a4c0c056371b6f0db726b88fbb76bbee94948fb2abd4dbc8d958f7c42f766c")
    version("1.5", sha256="4fcf4618171727d165fc044d465a66e3119217bb4577a97374f94fcd8aed330e")
    version("1.4", sha256="ec237faa83bb1c803fbdf7c6e83d8a2ad68b6f0ed1879c3aa16c0e1dcc478742")
    version("1.3", sha256="6527e3f47fab7c21e96bc757c4ae3303901f35e23f64642d6da5cc4c4fcc915a")
    version("1.2", sha256="0c43e68f336892f3a64cba19beb99d9212f529bedb77f7879c0331450b982d46")
    version("1.1", sha256="1e8dd0693a88c84937754df947b202871a40545b1b0a97ebefa370b0281c3c53")
    version("1.0", sha256="94bd86a2f9847c03e6c3bf8dca12af3734f8b272ffeacbc3fa8fcca58844b1d4")

    conflicts("@:1.5", when="target=a64fx", msg="a64fx is supported by pocl v1.6 and above.")

    # < 3.0 provided full OpenCL 1.2 support and some intermediate level of
    # OpenCL 2.0 support.  >= 3.0 provides full OpenCL 3.0 support when using
    # llvm >= 14.
    provides("opencl@2.0", when="^llvm@:13")
    provides("opencl@3.0", when="@3: ^llvm@14:")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake @3.12:", type="build", when="@4:")
    depends_on("cmake @3.9:", type="build", when="@3:")
    depends_on("cmake @3.3:", type="build", when="@1.6:")
    depends_on("cmake @2.8.12:", type="build")
    depends_on("hwloc")
    depends_on("hwloc@:1", when="@:1.1")
    depends_on("libtool", type="link", when="@:1.3")  # links against libltdl
    depends_on("pkgconfig", type="build")

    depends_on("llvm +clang")
    # PoCL aims to support **the latest LLVM version** at the time of PoCL release,
    # **plus the previous** LLVM version
    depends_on("llvm @17:21", when="@master")
    depends_on("llvm @17:21", when="@7.1")
    depends_on("llvm @17:21", when="@7.0")
    depends_on("llvm @17:19", when="@6.0")
    depends_on("llvm @16:17", when="@5.0")
    depends_on("llvm @15:16", when="@4.0")
    depends_on("llvm @14:15", when="@3.1")
    depends_on("llvm @13:14", when="@3.0")
    depends_on("llvm @12:13", when="@1.8")
    depends_on("llvm @11:12", when="@1.7")
    depends_on("llvm @10:11", when="@1.6")
    depends_on("llvm @9:10", when="@1.5")
    depends_on("llvm @8:9", when="@1.4")
    depends_on("llvm @7:8", when="@1.3")
    depends_on("llvm @6:7", when="@1.2")
    depends_on("llvm @5:6", when="@1.1")
    depends_on("llvm @4:5", when="@1.0")

    variant(
        "cpu_targets",
        description="CPU targets to be able to build kernels for. disto means a wide compatible combination.",
        values=disjoint_sets(
            ("native",),
            ("distro",),
            (
                # Specific architectures.
                "broadwell",
                "cascadelake",
                "haswell",
                "sapphirerapids",
                "skylake-avx512",
                "znver1",
                "znver2",
                "znver3",
                "znver4",
                # Generic architectures.
                "x86-64",
                "x86-64-v2",
                "x86-64-v3",
                "x86-64-v4",
                # Feature levels.
                "sse2",
                "sse3",
                "sse41",
                "avx",
                "avx_f16c",
                "avx_fma4",
                "avx2",
                "avx512",
            ),
        )
        .prohibit_empty_set()
        .with_error("'native' or 'distro' cannot be activated along with other targets")
        .with_default("native"),
    )
    variant("half", default=False, description="Support half (fp16) precision.", when="@4.0:")
    variant("cuda", default=False, description="CUDA backend.", when="@3.1:")
    variant("level0", default=False, description="Level 0 backend.", when="@4.0:")
    variant("client", default=False, description="Remote client support.", when="@5.0:")
    variant("server", default=False, description="Remote server support.", when="@5.0:")
    variant(
        "rdma",
        default=False,
        description="Add support for RDMA transfer for remote client/server.",
        when="@5:",
    )
    conflicts(
        "+rdma",
        when="~client ~server",
        msg="+rdma support is only meaningful for +client and/or +server.",
    )

    variant("dlopen", default=False, description="Open drivers with dlopen at runtime.")
    variant(
        "dlopen",
        default=True,
        when="~client ~server",
        description="Open drivers with dlopen at runtime.",
    )
    conflicts("+dlopen", when="+client", msg="+dlopen is not supported for +client")
    conflicts("+dlopen", when="+server", msg="+dlopen is not supported for +server")

    variant("icd", default=False, description="Support a system-wide ICD loader")

    depends_on("ocl-icd", when="+icd")
    depends_on("llvm @16:", when="+half")
    depends_on("cuda @11:", when="+cuda")
    depends_on("oneapi-level-zero", when="+level0")
    depends_on("rdma-core", when="+rdma")

    def url_for_version(self, version):
        if version >= Version("1.0"):
            url = "https://github.com/pocl/pocl/archive/v{0}.tar.gz"
        else:
            url = "https://portablecl.org/downloads/pocl-{0}.tar.gz"

        return url.format(version.up_to(2))

    def cmake_args(self):
        args = [
            self.define("INSTALL_OPENCL_HEADERS", True),
            self.define("ENABLE_LLVM", True),
            self.define("STATIC_LLVM", True),
            self.define(
                "KERNELLIB_HOST_CPU_VARIANTS", ";".join(self.spec.variants["cpu_targets"].value)
            ),
            self.define_from_variant("ENABLE_LOADABLE_DRIVERS", "dlopen"),
            self.define_from_variant("ENABLE_ICD", "icd"),
        ]
        # If +dlopen, we have to add {prefix}/lib64/pocl to the RPATH or else
        # the ICD loader will not be able to find the needed libraries.
        if "+dlopen" in self.spec:
            rpath = self.rpath
            rpath.append(self.prefix.lib64)
            rpath.append(os.path.join(self.prefix.lib64, "pocl"))
            args.append("-DCMAKE_INSTALL_RPATH=%s" % ":".join(rpath))
        # Options for variants that only exist for certain versions.
        if self.spec.satisfies("@3.1:"):
            args.append(self.define_from_variant("ENABLE_CUDA", "cuda"))
        if self.spec.satisfies("@4.0:"):
            args.append(self.define_from_variant("ENABLE_LEVEL0", "level0"))
        if self.spec.satisfies("@5.0:"):
            args.append(self.define_from_variant("ENABLE_REMOTE_CLIENT", "client"))
            args.append(self.define_from_variant("ENABLE_REMOTE_SERVER", "server"))
            args.append(self.define_from_variant("ENABLE_RDMA", "rdma"))
        return args

    @run_after("install")
    def symlink_opencl(self):
        symlink("CL", self.prefix.include.OpenCL)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        # Build and run a small program to test the installed OpenCL library
        spec = self.spec
        print("Checking pocl installation...")
        checkdir = "spack-check"
        with working_dir(checkdir, create=True):
            source = join_path(os.path.dirname(self.module.__file__), "example1.c")
            cflags = spec["pocl"].headers.cpp_flags.split()
            ldflags = [f"-L{self.prefix.lib}", "-lOpenCL", "-lpoclu"]
            output = compile_c_and_execute(source, cflags, ldflags)
            compare_output_file(
                output, join_path(os.path.dirname(self.module.__file__), "example1.out")
            )
