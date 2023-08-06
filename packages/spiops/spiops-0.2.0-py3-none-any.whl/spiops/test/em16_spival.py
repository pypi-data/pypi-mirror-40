import spiops as spiops


spiops.load('/Users/mcosta/ExoMars2016/kernels/mk/em16_ops_local.tm')

interval = spiops.TimeWindow('2018-03-10T00:00:00', '2018-03-11T23:59:00', resolution=20)

mars = spiops.Target('MARS', time=interval, frame='IAU_MARS')
tgo = spiops.Observer('TGO', time=interval, target=mars)

#tgo.Plot('zaxis_target_angle', notebook=False)

#tgo.Plot('sa_ang', date_format='UTC',notebook=False)
tgo.Plot('saa_sc', date_format='UTC', notebook=False)
tgo.Plot('saa_sa', date_format='UTC', notebook=False)

tgo.Plot('hga_earth', date_format='UTC',  notebook=False)
tgo.Plot('hga_el_az', date_format='UTC', notebook=False)

