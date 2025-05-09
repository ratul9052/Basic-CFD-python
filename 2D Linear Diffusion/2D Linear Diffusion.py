import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D 


#----------------2D Linear Diffusion Equation-----------------#
#             du/dt = nu*( d^2u/dx^2 +d^2u/dy^2)              #

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
# u0_gaussian_2d = lambda x, y, ax, ay, sx, sy: 2*np.exp(-((x-ax)**2 /sx**2 + (y-ay)**2 /sy**2))
# u0=u0_gaussian_2d(X,Y,0.5,0.5,0.2,0.2)

u0_sin=lambda x,y: np.sin(2*np.pi*x)*np.sin(2*np.pi*y)
u0=u0_sin(X,Y)

# u0_hat = lambda x, y: np.where((0.3 < x) & (x < 0.7) & (0.3 < y) & (y < 0.7), 2, 0)
# u0=u0_hat(X,Y)



plt.contourf(X,Y,u0)
plt.show()

#physical condition
nu=0.1

#stability condition:
# D(Diffusion Number) <= 0.5
D=0.5
dt=D/(nu/dx/dx +nu/dy/dy)

t=0.0
tend=0.5

#setup the solution arrays
sol=[]
u=np.zeros([ny,nx])
u=u0
sol.append(u)


#periodic conditions on the initial condition
u[:,0]=0
u[:,-1]=0
u[0,:]=0
u[-1,:]=0

#time advance loop
while t<tend:
    un=sol[-1]
    unew=un.copy()
    #update the solution at the interior points
    unew[1:-1,1:-1]=un[1:-1,1:-1] + nu*(dt/dx/dx)*(un[1:-1,0:-2] - 2*un[1:-1,1:-1] + un[1:-1,2:])\
                                  + nu*(dt/dy/dy)*(un[0:-2,1:-1] - 2*un[1:-1,1:-1] + un[2:,1:-1])
                                     
    unew[:,0]=0
    unew[:,-1]=0
    unew[0,:]=0
    unew[-1,:]=0

    sol.append(unew)
    t+=dt

#animation
fig=plt.figure(figsize=(12, 4)) 


ax1=fig.add_subplot(1, 2, 1)
ax2=fig.add_subplot(1, 2, 2, projection='3d')


def update(frame):
    ax1.clear()
    ax2.clear()

    # Contour plot
    cont=ax1.contourf(X, Y, sol[frame], cmap=cm.jet, levels=20, vmin=-1, vmax=1)
    ax1.text(0.3, 0.9, rf"2D Diffusion $\nu$={nu:.3f}",fontsize=10, transform=ax1.transAxes)
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")

    # 3D surface plot
    surf=ax2.plot_surface(X, Y, sol[frame], cmap=cm.jet, vmin=-1, vmax=1, rstride=1, cstride=1)
                            
    ax2.set_zlim(-2, 2)
    ax2.view_init(elev=20, azim=315)
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.set_zlabel("u")

    return cont, surf

ani = animation.FuncAnimation(fig, update, frames=range(0,len(sol),10) ,interval=1)
plt.show()
#ani.save(f"2D Linear Diffusion/plots/2D_D_h_nu={nu:.3f}.gif", writer="pillow")



