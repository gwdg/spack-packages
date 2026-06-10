from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage

from spack.package import *


class Mhm2(CMakePackage, CudaPackage):
    """
    MetaHipMer (MHM) is a de novo metagenome short-read assembler,
    which is written in UPC++, CUDA and HIP, and runs efficiently
    on both single servers and on multinode supercomputers,
    where it can scale up to coassemble terabase-sized metagenomes.
    """

    homepage = "https://bitbucket.org/berkeleylab/mhm2/"
    url = "https://bitbucket.org/berkeleylab/mhm2/downloads/mhm2-v2.1.0.tar.gz"

    version("2.2.0.0", sha256="b966b1bf7c0f3e64b3324689f7807a408c241590c6da7371d5b86b5c4bc4db72")
    version("2.1.0", sha256="2da09f80d509c3036a06fefd8c2dc095cbf6abd67bf2f042452972ff084be2b3")
    version("2.0.1.2", sha256="0845f239befd1769a4a1920dbb3a92abad857e0314a36023870e071ce87d5cdc")

    variant("build_type", default="Release", description="CMAKE build type")
    variant("ipo", default=True, description="CMake interprocedural optimization")
    variant("conduit", default="mpi", description="Conduit used by gasnet")

    variant("cuda", default=False, description="enable compute on gpu")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    # depends_on('gcc@9.3.0')
    depends_on("upcxx+mpi")
    depends_on("openmpi")

    depends_on("cuda", when="+cuda")

    patch("changed-runcommand-from-upcxxrun-to-srun.patch")

    def cmake_args(self):

        args = [
            # '-DCMAKE_CXX_COMPILER={0}'.format(self.spec['gcc'].prefix + '/bin/g++')
            "-DCMAKE_CXX_COMPILER={0}".format(self.spec["mpi"].mpicxx)
        ]

        if "+cuda" in self.spec:
            cuarch_list = self.spec.variants["cuda_arch"].value
            cuarch = cuarch_list[0]
            if "none" == cuarch:
                cuarch = "70"  # Default minimum
            print("CUARCH: ", cuarch)

            args += ["-DENABLE_CUDA=ON", "-DCMAKE_CUDA_ARCHITECTURES=" + cuarch]
        else:
            args += ["-DENABLE_CUDA=OFF"]

        return args

    def setup_run_environment(self, env):
        if self.spec.variants["conduit"].value == "mpi":
            env.set("UPCXX_GASNET_CONDUIT", "mpi")
            env.set("GASNET_IBV_MODEL_WARN", "0")
            env.set("GASNET_PHYSMEM_PROBE", "0")
            env.set("OMPI_MCA_mtl", "ofi")
            env.set("OMPI_MCA_btl", "ofi")
            env.set("OMPI_MCA_osc", "ucx")
        else:
            env.set("UPCXX_GASNET_CONDUIT", self.spec.variants["conduit"].value)
