import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D 


#-----------------------2D Non-Linear Convection Diffusion Equation-----------------------#
#             du/dt + u*du/dx + v*du/dy= nu*( d^2v/dx^2 +d^2v/dy^2)                       #
#             dv/dt + u*dv/dx + v*dv/dy= nu*( d^2v/dx^2 +d^2v/dy^2)                       #

#define the grid of spatial and temporal domain 
nx=51
ny=51
Lx=1.0
Ly=1.0
#create coordinates
x=np.linspace(0,Lx,nx)
dx=x[1]-x[0]
y=np.linspace(0,Ly,ny)
dy=y[1]-y[0]
#create 2D mesh
X,Y=np.meshgrid(x,y)

#--------------------initial condition------------------#
u0_gaussian_2d = lambda x, y, ax, ay, sx, sy: 2*np.exp(-((x-ax)**2 /sx**2 + (y-ay)**2 /sy**2))
u0=u0_gaussian_2d(X,Y,0.5,0.5,0.2,0.2)
v0=u0_gaussian_2d(X,Y,0.5,0.5,0.2,0.2)


# u0_sin=lambda x,y: 2*np.sin(2*np.pi*x)*np.sin(2*np.pi*y)
# u0=u0_sin(X,Y)
# v0=u0_sin(X,Y)

# u0_hat = lambda x, y: np.where((0.2 < x) & (x < 0.4) & (0.4 < y) & (y < 0.6), 2, 0)
# u0=u0_hat(X,Y)
# v0=u0_hat(X,Y)



# plt.contourf(X,Y,u0)
# plt.show()

#physical condition
cx=abs(u0).max()
cy=abs(v0).max()
nu=0.01


#stability condition:
# sum(courant number) <= 1
Cr=1
Cdt=Cr/(abs(cx)/dx +abs(cy)/dy)
# D(Diffusion Number) <= 0.5
D=0.5
Ddt=D/(nu/dx/dx +nu/dy/dy)

dt=min(Cdt,Ddt)

t=0.0
tend=0.5

#setup the solution arrays
u_sol=[]
v_sol=[]

u=np.zeros([ny+2,nx+2])
v=np.zeros([ny+2,nx+2])

u[1:-1,1:-1]=u0
v[1:-1,1:-1]=v0

u_sol.append(u)
v_sol.append(v)



#periodic conditions on the initial condition
#in 1D:
#u[0]=u[-3]
#u[-1]=u[2]

#periodic conditions on the initial condition for u field
#left face or x-minus face
u[:,0]=u[:,-3]
#right face or x-plus face
u[:,-1]=u[:,2]

#y-minus face(bottom)
u[0,:]=u[-3,:]
#y-pluse face(top)
u[-1,:]=u[2,:]

#periodic conditions on the initial condition for v field
#left face or x-minus face
v[:,0]=v[:,-3]
#right face or x-plus face
v[:,-1]=v[:,2]

#y-minus face(bottom)
v[0,:]=v[-3,:]
#y-pluse face(top)
v[-1,:]=v[2,:]


#time advance loop
while t<tend:
    un=u_sol[-1]
    vn=v_sol[-1]

    unew=un.copy()
    vnew=vn.copy()
    #update the solution at the interior points of u field
    unew[1:-1,1:-1]=un[1:-1,1:-1] - 0.5*(un[1:-1,1:-1]+abs(un[1:-1,1:-1]))*(dt/dx)*(un[1:-1,1:-1] - un[1:-1,0:-2]) - 0.5*(vn[1:-1,1:-1]+abs(vn[1:-1,1:-1]))*(dt/dy)*(un[1:-1,1:-1] - un[0:-2,1:-1])\
                                  - 0.5*(un[1:-1,1:-1]-abs(un[1:-1,1:-1]))*(dt/dx)*(un[1:-1,2:] - un[1:-1,1:-1]) - 0.5*(vn[1:-1,1:-1]-abs(vn[1:-1,1:-1]))*(dt/dy)*(un[2:,1:-1] - un[1:-1,1:-1])\
                                  + nu*(dt/dx/dx)*(un[1:-1,0:-2] - 2*un[1:-1,1:-1] + un[1:-1,2:])\
                                  + nu*(dt/dy/dy)*(un[0:-2,1:-1] - 2*un[1:-1,1:-1] + un[2:,1:-1])


    #update the solution at the interior points of v field
    vnew[1:-1,1:-1]=vn[1:-1,1:-1] - 0.5*(un[1:-1,1:-1]+abs(un[1:-1,1:-1]))*(dt/dx)*(vn[1:-1,1:-1] - vn[1:-1,0:-2]) - 0.5*(vn[1:-1,1:-1]+abs(vn[1:-1,1:-1]))*(dt/dy)*(vn[1:-1,1:-1] - vn[0:-2,1:-1])\
                                  - 0.5*(un[1:-1,1:-1]-abs(un[1:-1,1:-1]))*(dt/dx)*(vn[1:-1,2:] - vn[1:-1,1:-1]) - 0.5*(vn[1:-1,1:-1]-abs(vn[1:-1,1:-1]))*(dt/dy)*(vn[2:,1:-1] - vn[1:-1,1:-1])\
                                  + nu*(dt/dx/dx)*(vn[1:-1,0:-2] - 2*vn[1:-1,1:-1] + vn[1:-1,2:])\
                                  + nu*(dt/dy/dy)*(vn[0:-2,1:-1] - 2*vn[1:-1,1:-1] + vn[2:,1:-1])

    #periodic conditions on the initial condition for u field
    #left face or x-minus face
    unew[:,0]=unew[:,-3]
    #right face or x-plus face
    unew[:,-1]=unew[:,2]

    #y-minus face(bottom)
    unew[0,:]=unew[-3,:]
    #y-pluse face(top)
    unew[-1,:]=unew[2,:]

    #periodic conditions on the initial condition for v field
    #left face or x-minus face
    vnew[:,0]=vnew[:,-3]
    #right face or x-plus face
    vnew[:,-1]=vnew[:,2]

    #y-minus face(bottom)
    vnew[0,:]=vnew[-3,:]
    #y-pluse face(top)
    vnew[-1,:]=vnew[2,:]

    u_sol.append(unew)
    v_sol.append(vnew)
    t+=dt

#animation
fig = plt.figure(figsize=(16, 12),constrained_layout=True) 


ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2, projection='3d')
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4, projection='3d')


def update(frame):
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()

    # Contour plot
    cont1 = ax1.contourf(X, Y, u_sol[frame][1:-1, 1:-1], cmap=cm.jet, levels=20, vmin=-1, vmax=1)
    ax1.text(0.3, 0.9, "u field",fontsize=10, transform=ax1.transAxes)
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")

    # 3D surface plot
    surf1 = ax2.plot_surface(X, Y, u_sol[frame][1:-1, 1:-1], cmap=cm.jet, vmin=-1, vmax=1, rstride=1, cstride=1)
                            
    ax2.set_zlim(-2, 2)
    ax2.view_init(elev=40, azim=315)
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.set_zlabel("u")

    # Contour plot
    cont2 = ax3.contourf(X, Y, v_sol[frame][1:-1, 1:-1], cmap='plasma', levels=20, vmin=-1, vmax=1)
    ax3.text(0.3, 0.9, " v field ",fontsize=10, transform=ax3.transAxes)
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")

    # 3D surface plot
    surf2 = ax4.plot_surface(X, Y, v_sol[frame][1:-1, 1:-1], cmap='plasma', vmin=-1, vmax=1, rstride=1, cstride=1)
                            
    ax4.set_zlim(-2, 2)
    ax4.view_init(elev=30, azim=-45)
    ax4.set_xlabel("x")
    ax4.set_ylabel("y")
    ax4.set_zlabel("v")    

    return cont1, surf1, cont2, surf2

ani = animation.FuncAnimation(fig, update, frames=len(u_sol), interval=0.1)
#fig.tight_layout()
ani.save(f"2D Non-Linear Convection Diffusion (2D Burgers's Equation)/plots/2D_NLCD_ug_vg.gif", writer="pillow")
#plt.show()
print("done")

