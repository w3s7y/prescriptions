import cProfile
import pstats
import timeit


def full_load_profile(chunk_size):
    # Profiles the etl pipeline.
    cProfile.run("etl.EtlController({}).run_pipe()".format(chunk_size), 'prescription_stats.profile')
    p = pstats.Stats('prescription_stats.profile')
    p.sort_stats('cumulative').print_stats(50)


def timed_etl_prescriptions_loads(chunk_sizes, iters):
    for chunk_size in chunk_sizes:
        time = timeit.repeat("e.run_pipe()", setup="import etl; e = etl.EtlController({})".format(chunk_size), number=iters)
        print("Runtime ({} iters) for a chunk size of {} was: {}".format(iters, chunk_size, time))


timed_etl_prescriptions_loads([100, 1000, 10000], 1)
