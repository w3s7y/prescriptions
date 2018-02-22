import cProfile
import etl
import pstats

# Profile the csv load & transform.
cProfile.run("etl.etl_controller().run_pipe()", 'prescription_stats.profile')
p = pstats.Stats('prescription_stats.profile')
p.sort_stats('cumulative').print_stats(50)

