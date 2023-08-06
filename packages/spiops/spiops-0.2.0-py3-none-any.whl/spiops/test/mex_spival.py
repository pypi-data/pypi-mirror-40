import spiops as spiops



spiops.load('/Users/mcosta/MARS-EXPRESS/kernels/mk/MEX_OPS_LOCAL.TM')

interval = spiops.TimeWindow('2016-12-01T01:00:00', '2016-12-04T00:00:00', resolution=10)


mars = spiops.Target('MARS', time=interval, frame='IAU_MARS')
mex = spiops.Observer('MEX', time=interval, target=mars)

mex.Plot('sa_ang_p', date_format='UTC',notebook=False)
mex.Plot('saa_sc', date_format='UTC', notebook=False)
mex.Plot('saa_sa_p', date_format='UTC', notebook=False)

mex.Plot('hga_earth', date_format='UTC',  notebook=False)