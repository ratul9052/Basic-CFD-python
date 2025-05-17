import numpy as np
import matplotlib.pyplot as plt

from solver.momentum import convection_x_central, convection_y_central, diffusion
from solver.pressure import poisson,poisson_vec
from solver.divergence import ddx,ddy,div
from utils.plot import plot_2d,field_animation
from utils.io import get_data,save_data
from utils.val import validation

#-------------------- 2D Navier Stokes ----------------#
#------------------- Lid Driven cavity ----------------#

#---------------------- Domain ------------------------# 
lx=1.0
ly=1.0
nx=129
ny=129

x=np.linspace(0,lx,nx)
y=np.linspace(0,ly,ny)

dx=x[1]-x[0]
dy=y[1]-y[0]

xx,yy=np.meshgrid(x,y)

#-------------- condition and flow properties ----------#
Uwall=1.0
Re=100
nu=Uwall*lx/Re
print("reynolds: ", Re)
print("viscosity: ", nu)

#-------------------- stability condition  ---------------#
dt1=0.25/(nu*(1.0/dx/dx + 1.0/dy/dy))
dt2=2*nu/(Uwall*Uwall)
dt=min(dt1,dt2)
print("stable time step: ",dt,"s")

#------------------ declare variable ---------------------#
u=np.zeros([ny,nx])
v=np.zeros([ny,nx])
p=np.zeros([ny,nx])

#------------------- boundary conditions ------------------#
#top wall
u[-1,:]=Uwall
v[-1,:]=0.0
#bottom wall
u[0,:]=0.0
v[0,:]=0.0
#right wall
v[:,-1]=0.0
u[:,-1]=0.0
#left wall
v[:,0]=0.0
u[:,0]=0.0

#time advance
t=0.0
i=0.0

while True:
    u_old=u.copy()
    v_old=v.copy()

    #momentum equations without pressure gradient
    ut=u + dt*(-convection_x_central(u,v,dx,dy) + diffusion(nu,u,dx,dy))
    vt=v + dt*(-convection_y_central(u,v,dx,dy) + diffusion(nu,v,dx,dy)) 

    #build pressure poisson equation
    source=div(ut,vt,dx,dy)/dt 
    error=poisson_vec(p,dx,dy,source)

    #veloctiy correction
    u=ut-dt*ddx(p,dx)
    v=vt-dt*ddy(p,dy)

    #boundary conditions
    #top wall
    u[-1,:]=Uwall
    v[-1,:]=0.0
    #bottom wall
    u[0,:]=0.0
    v[0,:]=0.0
    #right wall
    v[:,-1]=0.0
    u[:,-1]=0.0
    #left wall
    v[:,0]=0.0
    u[:,0]=0.0

    
    u_residual = np.linalg.norm(u - u_old) / np.linalg.norm(u_old)
    v_residual = np.linalg.norm(v - v_old) / np.linalg.norm(v_old)

    ## save data
    # if u_residual > 1e-3 and v_residual > 1e-3 and i % 100 == 0:
    #     save_data(u, v, p, i,output_dir="cavity data")  
    # else:
    #     if i % 1000 == 0:
    #         save_data(u, v, p, i,output_dir="cavity data")  
    

    if i % 50 == 0:
        print(f"Step {i}: \n u_residual = {u_residual:.2e}\n v_residual = {v_residual:.2e}\n pressure_error = {error:.2e}\n\n")

    if u_residual < 1e-6 and v_residual < 1e-6 and error < 1e-6:
        print(" Velocity and pressure converged")
        break



    i+=1
    t+=dt



print(f"final iteration = {i} \n poisson solver error:{error} \n u_residual = {u_residual} \n v_residual ={v_residual}")
plot_2d(xx,yy,u,v,p,int(Re))

# get_data(u,v,x,y)
# validation(int(Re))

# field_animation(xx,yy,x,y,Re,folder="cavity data")