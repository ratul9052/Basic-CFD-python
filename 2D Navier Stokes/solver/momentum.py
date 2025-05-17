import numpy as np

#----------------------UPwind Convective terms-----------------------#
epsilon= 2e-7
def convection_x_upwind(u,v,dx,dy):
    u_conv=np.zeros_like(u)
    
    u_conv[1:-1,1:-1]= 0.5*(u[1:-1,1:-1]+abs(u[1:-1,1:-1]))*(1/dx)*(u[1:-1,1:-1] - u[1:-1,0:-2]) - 0.5*(v[1:-1,1:-1]+abs(v[1:-1,1:-1]))*(1/dy)*(u[1:-1,1:-1] - u[0:-2,1:-1])\
                     + 0.5*(u[1:-1,1:-1]-abs(u[1:-1,1:-1]))*(1/dx)*(u[1:-1,2:] - u[1:-1,1:-1]) - 0.5*(v[1:-1,1:-1]-abs(v[1:-1,1:-1]))*(1/dy)*(u[2:,1:-1] - u[1:-1,1:-1])      # backwar scheme and forward scheme or Generalized Upwind Scheme
    u_conv = np.where(np.abs(u_conv) < epsilon, 0.0, u_conv)
    return u_conv

def convection_y_upwind(u,v,dx,dy):
    v_conv=np.zeros_like(v)

    v_conv[1:-1,1:-1]= 0.5*(u[1:-1,1:-1]+abs(u[1:-1,1:-1]))*(1/dx)*(v[1:-1,1:-1] - v[1:-1,0:-2]) - 0.5*(v[1:-1,1:-1]+abs(v[1:-1,1:-1]))*(1/dy)*(v[1:-1,1:-1] - v[0:-2,1:-1])\
                     + 0.5*(u[1:-1,1:-1]-abs(u[1:-1,1:-1]))*(1/dx)*(v[1:-1,2:] - v[1:-1,1:-1]) - 0.5*(v[1:-1,1:-1]-abs(v[1:-1,1:-1]))*(1/dy)*(v[2:,1:-1] - v[1:-1,1:-1])      # backwar scheme and forward scheme or Generalized Upwind Scheme
    v_conv = np.where(np.abs(v_conv) < epsilon, 0.0, v_conv)
    return v_conv

#----------------------Diffusion-----------------------#
def diffusion(nu,vel,dx,dy):
    vel_diff=np.zeros_like(vel)
    vel_diff[1:-1,1:-1]= (nu/dx/dx)*(vel[1:-1,0:-2] - 2*vel[1:-1,1:-1] + vel[1:-1,2:])\
                       + (nu/dy/dy)*(vel[0:-2,1:-1] - 2*vel[1:-1,1:-1] + vel[2:,1:-1])
    vel = np.where(np.abs(vel) < epsilon, 0.0, vel)
    return vel_diff


#----------------------Central Convective terms-----------------------#
def convection_x_central(u, v, dx, dy):
    u_conv = np.zeros_like(u)
    u_conv[1:-1,1:-1] = (
        u[1:-1,1:-1] * (u[1:-1,2:] - u[1:-1,0:-2]) / (2*dx) +
        v[1:-1,1:-1] * (u[2:,1:-1] - u[0:-2,1:-1]) / (2*dy)
    )
    u_conv = np.where(np.abs(u_conv) < epsilon, 0.0, u_conv)
    return u_conv

def convection_y_central(u, v, dx, dy):
    v_conv = np.zeros_like(v)

    v_conv[1:-1, 1:-1] = (
        u[1:-1, 1:-1] * (v[1:-1, 2:] - v[1:-1, 0:-2]) / (2 * dx) +  # du * dv/dx
        v[1:-1, 1:-1] * (v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy)    # dv * dv/dy
    )

    v_conv = np.where(np.abs(v_conv) < epsilon, 0.0, v_conv)

    return v_conv