import os
import sys
from gem5art.run import gem5Run
from gem5art.tasks.tasks import run_gem5_instance
from MyArtifact import MyArtifact

print("Registering packer")
packer = MyArtifact(
        command = '''wget https://releases.hashicorp.com/packer/1.4.3/packer_1.4.3_linux_amd64.zip;
        unzip packer_1.4.3_linux_amd64.zip;''',
        type = 'binary',
        name = 'packer',
        path =  'disk-image/packer',
        cwd = 'disk-image',
        documentation = 'Program to build disk images. Downloaded sometime in August from hashicorp.').getArtifact()

print("Registering experiments_repo")
experiments_repo = MyArtifact(
        command = '',#'git clone https://your-remote-add/parsec-tests.git'
        type = 'git repo',
        name = 'gem5-baseline',
        path =  './',
        cwd = '../',
        documentation = 'gem5-baseline repository').getArtifact()

print("Registering parsec_repo")
parsec_repo = MyArtifact(
        command = '''cd parsec;
        git clone https://github.com/darchr/parsec-benchmark.git;''',
        type = 'git repo',
        name = 'parsec_repo',
        path =  './disk-image/parsec/parsec-benchmark/',
        cwd = './disk-image/',
        documentation = 'main repo to copy parsec source to the disk-image').getArtifact()

print("Registering gem5_repo")
gem5_repo = MyArtifact(
        command = '''
        git clone https://gem5.googlesource.com/public/gem5 gem5;
        cd gem5
        git checkout v19.0.0.0''',
        type = 'git repo',
        name = 'gem5',
        path =  'gem5/',
        cwd = './',
        documentation = 'cloned gem5 source file with version v19.0.0.0').getArtifact()

print("Registering m5_binary")
m5_binary = MyArtifact(
        command = '''cp Makefile.x86 Makefile;
        make;''',
        type = 'binary',
        name = 'm5',
        path =  'gem5/util/m5/m5',
        cwd = 'gem5/util/m5',
        inputs = [gem5_repo,],
        documentation = 'm5 utility').getArtifact()

print("Registering disk_image")
disk_image = MyArtifact(
        command = './packer build parsec/parsec.json',
        type = 'disk image',
        name = 'parsec',
        cwd = 'disk-image',
        path = 'disk-image/parsec/parsec-image/parsec',
        inputs = [packer, experiments_repo, m5_binary, parsec_repo,],
        documentation = 'Ubuntu with m5 binary and PARSEC installed.').getArtifact()

print("Registering gem5_binary")
gem5_binary = MyArtifact(
        command = 'scons build/X86/gem5.opt -j4',
        type = 'gem5 binary',
        name = 'gem5',
        cwd = 'gem5/',
        path =  'gem5/build/X86/gem5.opt',
        inputs = [gem5_repo,],
        documentation = 'gem5 binary version v19.0.0.0').getArtifact()

print("Registering linux_repo")
linux_repo = MyArtifact(
        command = '''git clone --branch v4.19.83 --depth 1 https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git;
        mv linux linux-4.19.83-stable''',
        type = 'git repo',
        name = 'linux-4.19.83-stable',
        path =  'linux-4.19.83-stable/',
        cwd = './',
        documentation = 'linux kernel source code repo version 4.19.83').getArtifact()

print("Registering linux_binary")
linux_binary = MyArtifact(
        name = 'vmlinux-4.19.83',
        type = 'kernel',
        path = 'linux-4.19.83-stable/vmlinux-4.19.83',
        cwd = 'linux-4.19.83-stable/',
        command = '''
        cp ../linux-config/config.4.19.83 .config;
        make -j8;
        cp vmlinux vmlinux-4.19.83;
        ''',
        inputs = [experiments_repo, linux_repo,],
        documentation = "kernel binary for v4.19.83").getArtifact()

if __name__ == "__main__":
    print('main')
    num_cpus = ['1']
    benchmarks = ['blackscholes', 'bodytrack', 'canneal', 'dedup','facesim', 'ferret', 'fluidanimate', 'freqmine', 'raytrace', 'streamcluster', 'swaptions', 'vips', 'x264']

    sizes = ['simsmall', 'simlarge', 'native']
    cpus = ['kvm', 'timing']


# ./build/ARM_MESI_Two_Level/gem5.opt 
# --outdir=/data/sungkeun/HWSecurity/m5out/restore/asplos20-results-upto-500m-vc16-16/blackscholes-8-simmedium-arm-UnsafeBaseline-vc16-16./configs/example/fs.py \
# --script=./scripts/blackscholes_simmedium_8.rcS \
# --kernel=/home/sungkeun/gem5-kernel/arm_parsec/binaries/vmlinux.aarch64.20140821 \
# --disk-image=/home/sungkeun/gem5-kernel/arm_parsec/disks/parsec-aarch64-ubuntu-trusty-headless.img \
# --dtb-file=/home/sungkeun/gem5-kernel/arm_parsec/binaries/vexpress.aarch64.20140821.dtb \
# --machine-type=VExpress_EMM64 \
# --cpu-type=DerivO3CPU \
# --checkpoint-dir=/data/sungkeun/HWSecurity/m5out/ckpts/blackscholes-8-simmedium-arm \
# --checkpoint-restore=1 \
# --num-cpus=8 \
# --mem-size=2GB \
# --ruby \
# --has-victim \
# --l1d-vc-size=16 \
# --l2-vc-size=16 \
# --num-l2caches=8 \
# --num-dirs=8 \
# --l1d_assoc=8 \
# --l2_assoc=16 \
# --l1i_assoc=4 \
# --network=garnet2.0 \
# --topology=Mesh_XY \
# --mesh-rows=4 \
# --scheme=UnsafeBaseline \
# --maxinsts=500000000

    for cpu in cpus:
        for num_cpu in num_cpus:
            for size in sizes:
                if cpu == 'timing' and size != 'simsmall':
                    continue
                for bm in benchmarks:
                    run = gem5Run.createFSRun(
                            'parsec_tests',    
                            'gem5/build/X86/gem5.opt',
                            'configs-parsec-tests/run_parsec.py',
                            f'''results/run_parsec/{bm}/{size}/{cpu}/{num_cpu}''',
                            gem5_binary, gem5_repo, experiments_repo,
                            'linux-4.19.83-stable/vmlinux-4.19.83',
                            'disk-image/parsec/parsec-image/parsec',
                            linux_binary, disk_image,
                            cpu, bm, size, num_cpu,
                            timeout = 24*60*60 #24 hours
                            )
                    print('creating FS run :%s' % (run))
                    run_gem5_instance.apply_async((run, os.getcwd(), ))
