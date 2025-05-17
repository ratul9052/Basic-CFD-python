import numpy as np
import os



def get_data(u,v,x,y):

    ny,nx=u.shape

    #exporting data
    data_u_alongY = np.column_stack(( y, u[:, nx//2]))
    data_v_alongX = np.column_stack(( x, v[ny//2 ,:]))

    np.savetxt('data/u_alongY.csv', data_u_alongY, delimiter=',', header='   y    u', comments='', fmt='  %.4f,  %.5f')
    np.savetxt('data/v_alongX.csv', data_v_alongX, delimiter=',', header='   x,   v', comments='', fmt='  %.4f,  %.5f')




def save_data(u, v, p, t, output_dir="output"):
    """
    Save velocity fields u, v and pressure p to a compressed .npz file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = os.path.join(output_dir, f"data_{int(t)}.npz")
    np.savez_compressed(filename, u=u, v=v, p=p)

