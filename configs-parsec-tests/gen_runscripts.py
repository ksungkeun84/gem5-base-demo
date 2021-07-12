import os
import sys

def writeBenchScript(dir, bench, size, nthreads):
    """
    This method creates a script in dir which will be eventually
    passed to the simulated system (to run a specific benchmark
    at bootup).
    """
    file_name = '{}/{}_{}_{}.rcS'.format(dir, bench, size, nthreads)
    bench_file = open(file_name,"w+")
    bench_file.write('cd /home/gem5/parsec-benchmark\n')
    bench_file.write('source env.sh\n')
    bench_file.write('parsecmgmt -a run -p {} -c gcc-hooks -i {} -n {}\n'.format(bench, size, nthreads))

    # sleeping for sometime makes sure
    # that the benchmark's output has been
    # printed to the console
    bench_file.write('sleep 5 \n')
    bench_file.write('m5 exit \n')
    bench_file.close()
    return file_name




if __name__ == "__main__":
    benchmarks = ['blackscholes', 'bodytrack', 'canneal', 'dedup','facesim', 'ferret', 'fluidanimate', 'freqmine', 'raytrace', 'streamcluster', 'swaptions', 'vips', 'x264']
    sizes = ['simsmall', 'simlarge', 'native']
    nthreads = ['1', '4', '8', '16']


    for bench in benchmarks:
        for size in sizes:
            for nth in nthreads:
                writeBenchScript('runscripts', bench, size, nth)
