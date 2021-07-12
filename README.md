# Gem5 baseline template
This is a template repository to setup gem5 simulation environment along with [gem5art](https://gem5art.readthedocs.io/en/latest/index.html#). gem5art is python packages that manage artifacts (inputs and outputs of gem5) using [Mongo Database](https://www.mongodb.com/) and monitor running gem5 processes using [Celery](https://docs.celeryproject.org/en/stable/). This repository include all the necessary source files to run a simulation such as gem5, linux kernel, disk image, benchmark suite.

This repository provides [Dockerfile](docker-container/Dockerfile) to save your time to set up your host machine. If you want to use your host machine directly without docker, you can refer to [Dockerfile](docker-container/Dockerfile) to install all the required packages. The following is the step by step instruction to create artifacts of gem5 simulation and run/monitor gem5 simulation.

### Repository Structure
```bash
├── docker-container/
│   └── Dockerfile                    # docker build file
├── disk-image/         
│   ├── packer                        # packer tool that generates disk image
│   ├── parsec/                       
│   │   ├── parsec-benchmark         
│   │   ├── parsec-image              # disk image will be stored in this folder.      
│   │   ├── parsec.json               # input file to packer tool. It show overall flow of disk image building process.
│   │   ├── parsec-install.sh         # Commands to build parsec benchmarks
│   │   ├── post-installation.sh     
│   │   └── runscript.sh 
│   ├── parsec-image/    
│   │   └── parsec                    # disk image for parsec benchmarks
│   └── shared/
├── linux-4.19.83-stable/
├── linux-config/
├── gem5/                             # version 19.0.0
├── configs-parsec-tests/             # this folder stores files to create gem5 system
│   ├── run_parsec.py                 # root script that is input to gem5.opt
│   └── system/                       # scripts that creates gem5 system
├── celery-run.sh
├── docker-build.sh
├── docker-run.sh
├── docker-mongo.sh
└── launch_parsec_tests.py
```

### MyArtifact and Register actifacts
Each artifact are registered to mongodb through [MyArtifact](MyArtifact.py). This class is extention of [Artifact](https://github.com/darchr/gem5art/blob/master/artifact/gem5art/artifact/artifact.py) to search the same artifact from db and download if it exists. MyArtifact class takes takes parameters that used to create the artifact. These parameters will be used to generate hash to identify. If you register a new artifact, you need to create it before register. Please refer to [gem5art document](https://gem5art.readthedocs.io/en/latest/main-doc/artifacts.html) for more detail about registering an artifact

### Linux Kernel Repo and Binary
The following is a snippet in [launch_parsec_tests.py](launch_parsec_tests.py) to download or register linux kernel repository and its binary. If your mangodb does not have these two artifacts, you can run the command which is the first parameter of MyArtifact.
```
linux_repo = MyArtifact(
        command = '''git clone --branch v4.19.83 --depth 1 https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git;
        mv linux linux-4.19.83-stable''',
        type = 'git repo',
        name = 'linux-4.19.83-stable',
        path =  'linux-4.19.83-stable/',
        cwd = './',
        documentation = 'linux kernel source code repo version 4.19.83').getArtifact()
        
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
```

### Disk Image build
[Packer](https://www.packer.io) is used to build a disk image. For now, this template provides a disk image with parsec benchmarks. As you can see in the following code snippet in [launch_parsec_tests.py](launchparsec_test.py), you need artifacts of packer, exeriments_repo, m5_binary, parsec_repo. They are already created included in this repository, so you don't have to create them.
```
disk_image = MyArtifact(
        command = './packer build parsec/parsec.json',
        type = 'disk image',
        name = 'parsec',
        cwd = 'disk-image',
        path = 'disk-image/parsec/parsec-image/parsec',
        inputs = [packer, experiments_repo, m5_binary, parsec_repo,],
        documentation = 'Ubuntu with m5 binary and PARSEC installed.').getArtifact()
```

### Docker install
If your system does not have docker, go to [this link](https://docs.docker.com/get-docker/) and install docker.

### Enable MongoDB using docker
If you want to use existing mongodb, you can replace __GEM5ART_DB__ environment variable through [setupenv.sh](setupenv.sh) as the follow:
```
export GEM5ART_DB="mongodb://[ip address or docker container id:[port]"
```
If you create your own mongodb, run the [docker-mongo.sh](docker-mongo.sh) and update __GEM5ART_DB__.
```docker-mong.sh
./docker-mongo.sh
```

### gem5art docker image
As virtual environment is critical to run multiple projects in a single host machine, this reposory also provides docker image to run gem5 simulations.
It is posted in [Docker Hub](https://hub.docker.com/repository/docker/danguria/gem5art) so you can pull it down to the host machine.
```
docker pull danguria/gem5art:latest
```
If you want to costomize the docker image, you can modify [Dockerfile](docker-container/Dockerfile) and build the image as follows.
```
sudo docker build docker-container/ -t danguria/gem5art  # replace danguria/gem5art with your own name.
```
This is written in [docker-build.sh](docker-build.sh)
Now, you are ready to run gem5art docker. Run the script [docker-run.sh](docker-run.sh)
```
./docker-run.sh
```

### Build gem5
You need to build gem5 binary which is one of the artifacts we need. The follwoing is the example and refer to [gem5 document](https://www.gem5.org/documentation/general_docs/building) for more inforamtion.
```
scons build/X86/gem5.opt -j4
```

### Launch simulation
This repository provides a script to register artifacts and launch the gem5 full system simulation of [parsec benchmark suite](https://github.com/darchr/parsec-benchmark.git). You can run the following commands. It sources environment variaables, launch celery server, and start simulations.
```
source setupenv.sh ; \
./celery-run.sh; \
python3 launch_parsec_tests.py
```

### Monitoring Status
Once simulations are started, you can monitor their status through [Flower](https://flower.readthedocs.io/en/latest/).
Open your web brower and enter `https://[ip-address]:5555`, then you'll see the status as the follows. To see configuratoin of celery and flower server, refer to [celery-run.sh](celery-run.sh) script.
![celery-dashboard](https://user-images.githubusercontent.com/1031755/125143300-dd4be700-e0df-11eb-83e7-7ed340074371.PNG)
![celery-tasks](https://user-images.githubusercontent.com/1031755/125143303-e046d780-e0df-11eb-925d-b0d03c06ba88.PNG)



## References
* https://gem5art.readthedocs.io/en/latest/index.html#
* https://arch.cs.ucdavis.edu/assets/papers/ispass21-gem5art.pdf
* https://docs.docker.com/
* https://docs.celeryproject.org/en/stable/
* https://flower.readthedocs.io/en/latest/
* https://www.mongodb.com/


### attach and detach docker container
attach - docker exec -it [container name] bash
dettach - Ctrl-p Ctrl-q
