from spiops import spiops
import spiops.utils.time as time
import spiops.utils.utils as utils
from spiops.classes.sensor import Sensor
from spiops.classes.observation import TimeWindow
from spiops.classes.body import Target
from spiops.classes.body import Observer

import spiceypy as cspice


#cspice.furnsh('MEX_OPS.TM')
#
#interval = TimeWindow('2017-01-25T00:00:00', '2017-01-26T06:00:00',
#                      resolution=60)
#
#
##print(interval.start)
#
#
#mars = Target('MARS', time=interval, frame='IAU_MARS')
#mex = Observer('MEX', time=interval, target=mars)
#
#vmc = Sensor('MEX_VMC', host=mex, target=mars, time=interval)
##spoint = vmc.getSpoint()
#
#print(vmc.fov_shape)
#
##spoint = vmc.getSpoint()
#
##print(spoint)
#
#mex.Plot('distance')
##mex.Plot('altitude')
#
#
#interval.finish = '2017-01-26T12:00:00'
#
#
##mex.Plot3D()
#
#resolution = 60
#tolerance = 0.1  # deg
#spacecraft_frame = 'ROS_LANDER'
#target_frame = '67P/C-G_CK'
#
#
#mk = 'data/SPICE/ROSETTA/kernels/mk/ROS_CKDIFF_TEST.TM'
#ck1 = 'data/SPICE/ROSETTA/kernels/ck/LATT_EME2LDR_SDL_SONC_V1_0.BC'
#ck2 = 'data/SPICE/ROSETTA/kernels/ck/LATT_EME2LDR_SDL_SONC_V1_1.BC'
#ck3 = 'data/SPICE/ROSETTA/kernels/ck/LATT_ROS2LDR_SDL_ROMAP_V1_0.BC'
#spacecraft_frame = 'MEX_SC_REF'
#target_frame = 'J2000'
#
#
#mk = 'data/SPICE/MARS-EXPRESS/kernels/mk/MEX_CKDIFF_TEST.TM'
#ck1 = 'data/SPICE/MARS-EXPRESS/kernels/ck/ATNM_MEASURED_160101_170101_V03.BC'
#ck2 = 'data/SPICE/MARS-EXPRESS/kernels/ck/ATNM_MEASURED_160101_170101_V02_fix.BC'
#spiops.ckdiff(mk, ck1, ck2, spacecraft_frame, target_frame, resolution, tolerance,
#              plot_style='line')




#spiops.ckplot(mk, ck1, spacecraft_frame, target_frame,
#              resolution)#, utc_start='2014-NOV-12 10:36:42', utc_finish='2014-NOV-12 11:30:00')

#spiops.ckplot(mk, ck2, spacecraft_frame, target_frame,
#              resolution)#, utc_start='2014-NOV-12 10:36:42', utc_finish='2014-NOV-12 11:30:00')

#mk = 'data/SPICE/ROSETTA/kernels/mk/ROS_SPKDIFF_TEST.TM'

#resolution = 1
#pos_tolerance = 0.001  # deg
#vel_tolerance = 0.001
#spacecraft = 'ROS_LANDER'
#target = 'CHURYUMOV-GERASIMENKO'
#target_frame = '67P/C-G_CK'

#spk1 = 'data/SPICE/ROSETTA/kernels/spk/LORB_SUN_J2000_SDL_V1_0.BSP'
#spk2 = 'data/SPICE/ROSETTA/kernels/spk/LORB_DV_145_01___T19_00216.BSP'

#spiops.spkdiff(mk, spk1, spk2, spacecraft, target, resolution,
#               pos_tolerance, vel_tolerance, target_frame=target_frame,
#               plot_format='line')

#print(mex.Orientation())

#cspice.furnsh('juice_crema_3_2_v151.tm')
#
#interval = TimeWindow('2033-02-01T00:00:00', '2033-05-01T01:00:00',
#                      resolution=60*60)
#
#
##print(interval.start)
#
#
#jupiter = Target('JUPITER', time=interval, frame='IAU_JUPITER')
#juice = Observer('JUICE', time=interval, target=jupiter)
#
#
#ganymede = Target('GANYMEDE', time=interval, frame='IAU_GANYMEDE')
#
#juice.target = ganymede
#
#juice.Plot('altitude')


#mk = 'ROS_V06.TM'
#
#
#spiops.load(mk)
#interval = TimeWindow('2014-11-12T08:35:00', '2014-11-14T22:18:01',resolution=30)
#comet = Target('67P/C-G', time=interval, frame='67P/C-G_CK')
#lander = Observer('ROS_LANDER', time=interval, target=comet)
#lander.Plot('altitude')

#spacecraft_frame = 'ROS_LANDER'
#target_frame = '67P/C-G_CK'
#resolution = 60

#ck = '/Users/mcosta/Dropbox/SPICE/SPICE_ROSETTA/processing/lander_ancillary_data/lander_ck_generation/SDL/ROMAP/LATT_ROS2LDR_SDL_ROMAP_V1_0.BC'
#ck = '/Users/mcosta/Dropbox/SPICE/SPICE_ROSETTA/processing/lander_ancillary_data/lander_ck_generation/SDL/SONC/LATT_EME2LDR_SDL_V1_0.BC'
#ck = '/Users/mcosta/Dropbox/SPICE/SPICE_ROSETTA/processing/lander_ancillary_data/lander_ck_generation/FSS/SONC_20170809/LATT_CFF2LDR_FSS_V2_0.BC'



#spiops.ckplot(mk, ck, spacecraft_frame, target_frame, resolution,
#           utc_start='', utc_finish='2014-11-30T00:00:00', notebook=False, plot_style='line')


#ck_path = '/Users/mcosta/kernels_em16/kernels/ck/'
#ck_list = [
#'em16_tgo_sc_sam_20170301_20170331_s20171007_v01.bc',
#'em16_tgo_sc_sam_20170401_20170430_s20171007_v01.bc',
#'em16_tgo_sc_sam_20170501_20170531_s20171007_v01.bc',
#'em16_tgo_sc_sam_20170601_20170630_s20171007_v01.bc',
#'em16_tgo_sc_sam_20170701_20170731_s20171007_v01.bc',
#'em16_tgo_sc_sam_20170801_20170831_s20171007_v01.bc',
#'em16_tgo_sc_sam_20170901_20170930_s20171007_v01.bc',
#'em16_tgo_sc_sam_20171001_20171008_s20171007_v01.bc'
#]
#
#for ck in ck_list:
#    spiops.ckplot(mk, ck_path+ck, spacecraft_frame, target_frame, resolution, plot_style='line')

#spiops.load('/Users/mcosta/Dropbox/SPICE/SPICE_CROSS_MISSION/spiops/spiops/test/juice_crema_3_2_v151.tm')

#bodies = ['CALLIRRHOE',  'THEMISTO',  'MAGACLITE', 'TAYGETE',  'CHALDENE',  'HARPALYKE',  'KALYKE',  'IOCASTE',  'ERINOME',  'ISONOE','PRAXIDIKE',  'AUTONOE', 'THYONE',  'HERMIPPE', 'AITNE', 'EURYDOME', 'EUANTHE',  'EUPORIE',  'ORTHOSIE', 'SPONDE', 'KALE', 'PASITHEE', 'HEGEMONE','MNEME',  'AOEDE', 'THELXINOE', 'ARCHE', 'KALLICHORE', 'HELIKE', 'CARPO',  'EUKELADE', 'CYLLENE',  'KORE',  'HERSE',  '55060',  '55061','55062',  '55063',  '55064',  '55065',  '55066',  '55067',  '55068',  '55069', '55070',  '55071',  '55072',  '55073', 'AMALTHEA', 'THEBE', 'ADRASTEA', 'METIS']
#spiops.pck_body_placeholder(bodies)

#mk = '/Users/mcosta/Dropbox/SPICE/SPICE_CROSS_MISSION/spiops/spiops/test/MEX_OPS.TM'

#spiops.sensor_with_sectors('MEX_ASPERA_IMA', mk)
