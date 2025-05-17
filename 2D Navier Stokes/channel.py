import numpy as np
import matplotlib.pyplot as plt

from solver.momentum import convection_x_upwind,convection_y_upwind, diffusion
from solver.pressure import poisson_vec_channel
from solver.divergence import ddx,ddy,div
from utils.plot import plot_2d_channel,field_animation
from utils.io import save_data
from utils.val import validation_channel


#-------------------- 2D Navier Stokes ----------------#
#--------------------- Channel Flow -------------------#

#-------------------- Domain ------------------------# 
#define the domain
lx=2.0
ly=2.0
nx=41
ny=41

x=np.linspace(0,lx,nx)
y=np.linspace(0,ly,ny)
xx,yy=np.meshgrid(x,y)

#-- declare variables(2 extra node for dealing with periodic condtion) --#
u=np.zeros([ny,nx+2])
v=np.zeros([ny,nx+2])
p=np.ones([ny,nx+2])
Fx=np.zeros([ny,nx+2])

dx=x[1]-x[0]
dy=y[1]-y[0]

#condition and flow properties
rho=2
nu=0.01
F=1
u[:,:]=0.1


#-------------------- Analytica Soluation ------------------------# 
dpdx=F*rho
u_ana = -dpdx / (2*nu*rho) * y * (y - ly)
dt=0.001



Fx[:,:]=F
#time advance
t=0.0
i=0.0

while True:
    u_old=u.copy()
    v_old=v.copy()


    #Non-convservative of convection term
    ut=u + dt*(-convection_x_upwind(u,v,dx,dy) + diffusion(nu,u,dx,dy) + Fx)
    vt=v + dt*(-convection_y_upwind(u,v,dx,dy) + diffusion(nu,v,dx,dy))

    #periodic Boundary Condition
    ut[:, 0] = ut[:, -2]
    ut[:, -1] = ut[:, 1]

    vt[:, 0] = vt[:, -2]
    vt[:, -1] = vt[:, 1]

    # No-slip at top and bottom walls (u = v = 0)
    ut[0, :]  = 0
    ut[-1, :] = 0
    vt[0, :]  = 0
    vt[-1, :] = 0


    #build pressure poisson equation
    source=rho*(div(ut,vt,dx,dy)/dt) 
    p, error=poisson_vec_channel(p,dx,dy,source)

    #velocity correction
    u=ut-dt*ddx(p,dx)/rho
    v=vt-dt*ddy(p,dy)/rho

    #boundary conditions
    #top wall
    u[-1,1:-1]=0.0
    v[-1,1:-1]=0.0
    #bottom wall
    u[0,1:-1]=0.0
    v[0,1:-1]=0.0

    #periodic condtion
    #left ghost node [0] = right physical node [-2] or [nx]
    v[:,0]=v[:,-2]
    u[:,0]=u[:,-2]
    #right ghost node [-1] = left physical node [1]
    v[:,-1]=v[:,1]
    u[:,-1]=u[:,1]

    u_residual = np.linalg.norm(u - u_old) / np.linalg.norm(u_old)
    v_residual = np.linalg.norm(v - v_old) / np.linalg.norm(v_old)


    ##save Data
    # if u_residual > 1e-3 and u_residual < 1e-4 and i % 100 == 0:
    #     save_data(u[:,1:-1], v[:,1:-1], p[:,1:-1], i)  
    
    # elif u_residual > 1e-4 and u_residual > 1e-5 and i % 1000 == 0:
    #     save_data(u[:,1:-1], v[:,1:-1], p[:,1:-1], i)  
    # elif u_residual > 1e-5 and u_residual > 1e-7 and i % 10000 == 0:
    #     save_data(u[:,1:-1], v[:,1:-1], p[:,1:-1], i)  


    if i % 100 == 0:
        print(f" Step {i}: \n u_residual = {u_residual:.2e}\n v_residual = {v_residual:.2e}\n pressure_error = {error:.2e}\n\n")

    if u_residual < 1e-6 and v_residual < 1e-6 and error < 1e-4 :
        print(" Velocity and pressure converged")
        break

    i+=1
    t+=dt




print(f"final iteration = {i} \n poisson solver error:{error} \n u_residual = {u_residual} \n v_residual ={v_residual}")
plot_2d_channel(xx,yy,u[:,1:-1],v[:,1:-1],p[:,1:-1],dx,dy,x,y)


# validation_channel(u[:,1:-1],v[:,1:-1],x,y,u_ana)
# field_animation(xx,yy,x,y)

