import numpy as np
  
# centers, pairs, spins, num_seeds_per_ring must have same length
x

centers = [(0., 0., 0.), (0., 0., 0.)] # list of 3-tuple centers (x, y, z) 
pairs = [(3.0, 1.), (1., 1.)] # list of 2-tuple pairs(radius, height)
spins = [(0., 0., 1.), (0., 0., 1.)] # list of 3-tuple spins (Jx, Jy, Jz)
num_seeds_per_ring = [8, 8] # list of ints number of seeds per ring
offsets = [0., 0.] # offset in the angles of phi chosen
reflectZ = True
with open("seeds_0.txt","w+") as f:
    for cen, pair, spin, num_steps, offset in zip(centers, pairs, spins, num_seeds_per_ring, offsets):
        r, h = pair
        spin_vec = np.array(spin); cen_vec = np.array(cen)
        spin_vec /= np.linalg.norm(spin_vec)
        u_vec = np.array([51., 50., 49.]) #random vector not parallel to spin
        u_vec -= np.dot(u_vec, spin_vec)    #subtracting off part parallel to spin
        u_vec /= np.linalg.norm(u_vec)
        v_vec = np.cross(spin_vec, u_vec)
        for phi in np.linspace(0 + offset, 2*np.pi + offset, num_steps, endpoint=False):
            c = r*np.cos(phi); s = r*np.sin(phi)
            p1 = cen_vec + c*u_vec + s*v_vec + h*spin_vec
            f.write("{} {} {}\n".format(str(p1[0]), str(p1[1]), str(p1[2])))
            if reflectZ:
                p2 = cen_vec + c*u_vec + s*v_vec - h*spin_vec
                f.write("{} {} {}\n".format(str(p2[0]), str(p2[1]), str(p2[2])))
