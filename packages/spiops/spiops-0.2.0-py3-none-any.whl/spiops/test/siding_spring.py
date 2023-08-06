import spiops as spiops
import spiceypy as cspice

spiops.load('/Users/mcosta/Dropbox/SPICE/SPICE_CROSS_MISSION/cosmographia/missions/MEX_SIDING_SPRING/kernels/mk/mex_siding_spring_v002.tm')


time = spiops.TimeWindow('2014-10-18T00:00:00', '2014-10-22T00:00:00', resolution=5)
timeset = time.window

plane_distance = []
real_distance = []
angles = []
bool = 0

#  The predicted time tpeak of peak dust flux [Tricarico et al., 2014; Kelley et al., 2014] was approximately 20 UT on 19 October 2014 or
#  approximately 90 min after the close approach of the comet

with open('siding_spring_data', 'w') as f:

    f.write('Time[UTC], Mars-SidingSpingPlane Distance[km], Mars-SidingSpring Distance[km], SidingSpring Orbital Inclination[degrees]\n')
    for et in timeset:
        (plane, real) = spiops.body_distance_to_plane('MARS', 'SIDING SPRING', et)
        angle = spiops.angle_between_planes('SIDING SPRING', 'EARTH', et)

        #id = cspice.bodn2c('SIDING SPRING')
        #state = cspice.spkgeo(0, et, 'J2000', id)[0]
        #mu = cspice.bodvrd('SUN', 'GM', 1)
        #elts = cspice.oscelt(state, et, mu[0])

        plane_distance.append(plane)
        real_distance.append(real)
        #angles.append(elts[2]*cspice.dpr())
        angles.append(angle)

        if bool == 0:
            bool = spiops.plane_ellipsoid('SIDING SPRING', 'MARS', et)

        if bool !=0 and bool !=1:
            print(cspice.et2utc(et, 'ISOC', 3))
            print(real)
            print(plane)
            bool = 1

        f.write('{},{},{},{}\n'.format(cspice.et2utc(et, 'ISOC', 3),plane, real, angle))


spiops.plot(timeset, [plane_distance,real_distance],
            yaxis_name=['Plane Distance [km]','Distance [km]'],
            title='Mars distance to Comet Siding Spring Plane',
            plot_height=500, plot_width=1000)


spiops.plot(timeset, [angles],
            yaxis_name=['Inclination [deg]'],
            title='Comet Siding Spring Orbital Plane Inclination Angle',
            plot_height=500, plot_width=1000)


def body_distance_to_plane(body_distance, body_plane, time):

    body_1 = body_plane
    body_2 = body_distance

    if isinstance(time, str):
        time = cspice.utc2et(time)

    id_1 = cspice.bodn2c(body_1)
    id_2 = cspice.bodn2c(body_2)


    mat = cspice.pxform('MEX_SIDING_SPRING_PLANE','IAU_MARS', time)
    vec1_1 = cspice.mxv(mat, [1,0,0])
    vec2_1 = cspice.mxv(mat, [0,1,0])

    state_1 = cspice.spkgeo(id_2, time, 'IAU_MARS', id_1)[0]

    pos_1 = state_1[0:3]
    vel_1 = state_1[2:5]

    pos_2 = [0,0,0]

    norm_1 = np.cross(vec1_1,vec2_1)
    norm_1 = norm_1/np.linalg.norm(norm_1)

    # https://mathinsight.org/distance_point_plane

    a1, b1, c1 = norm_1[0], norm_1[1], norm_1[2]
    d1 = -1*norm_1[0]*pos_1[0] - norm_1[1]*pos_1[1] - norm_1[2]*pos_1[2]

    dist_1 = abs(a1 * pos_2[0] + b1 * pos_2[1] + c1 * pos_2[2] + d1) / np.sqrt(
        np.square(a1) + np.square(b1) + np.square(c1))

    dist_real = np.linalg.norm(pos_1)

    return dist_1, dist_real


def angle_between_planes(body_1, body_2, time):

    if isinstance(time, str):
        time = cspice.utc2et(time)

    mat = cspice.pxform('MEX_SIDING_SPRING_PLANE', 'HEE', time)
    norm_1 = cspice.mxv(mat, [0,0,1])

    norm_1 = norm_1 / np.linalg.norm(norm_1)

    angle = 180 - cspice.dpr()*cspice.vsep(norm_1,[0,0,1])

    return angle


def plane_ellipsoid(body_1, body_2, time):


    id_1 = cspice.bodn2c(body_1)
    id_2 = cspice.bodn2c(body_2)

    mat = cspice.pxform('MEX_SIDING_SPRING_PLANE','IAU_MARS', time)
    vec1 = cspice.mxv(mat, [1,0,0])
    vec2 = cspice.mxv(mat, [0,1,0])

    state1 = cspice.spkgeo(id_2, time, 'IAU_'+body_2, id_1)[0]
    pos1 = state1[0:3]

    plane = cspice.psv2pl(pos1, vec1, vec2)

    # Get the body semi-axis lenght
    (num, semi_axis) = cspice.bodvcd(id_2, "RADII", 3)

    a = semi_axis[0]
    b = semi_axis[1]
    c = semi_axis[2]

    try:
        ellipse = cspice.inedpl(a, b, c, plane)
    except:
        ellipse = 0

    return ellipse
