import numpy as np
import lsst.sims.featureScheduler as fs
from lsst.sims.speedObservatory import Speed_observatory

# Run a single-filter r-band survey.
# 5-sigma depth percentile
# standard target map (WFD, NES, SCP, GP)
# Slewtime
# mask lots of off-meridian space
# No pairs
# Greedy selection of opsim fields

if __name__ == "__main__":

    survey_length = 365.25  # days
    # Define what we want the final visit ratio map to look like
    target_map = fs.standard_goals()['r']
    filtername = 'r'

    bfs = []
    bfs.append(fs.Depth_percentile_basis_function(filtername=filtername))
    bfs.append(fs.Target_map_basis_function(target_map=target_map, filtername=filtername))
    bfs.append(fs.North_south_patch_basis_function(zenith_min_alt=50.))
    bfs.append(fs.Slewtime_basis_function(filtername=filtername))

    weights_list = [[.5, 1., 1., 1.],
                    [1., 1., 1., 1.],
                    [0.5, 1., 1., 1.5],
                    [0.5, 1.5, 1., 1.]]
    for i, weights in enumerate(weights_list):
        
        survey = fs.Simple_greedy_survey_fields(bfs, weights, block_size=1, filtername=filtername)
        scheduler = fs.Core_scheduler([survey])

        observatory = Speed_observatory()
        observatory, scheduler, observations = fs.sim_runner(observatory, scheduler,
                                                             survey_length=survey_length,
                                                             filename='one_filter_%i.db' % i,
                                                             delete_past=True)

