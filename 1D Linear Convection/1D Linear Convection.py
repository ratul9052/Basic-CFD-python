import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#---------1D Convection Equation----------#
#         du/dt + c*du/dx = 0             #

#define the grid of spatial and temporal domain 
nx=61 #number of grid points
L=2.0 #length of the domain
x=np.linspace(0,L,nx)
dx=x[1]-x[0]
print(f'dx= {dx}')

nt=100
dt=0.0333

c=1.0 #velocity

Co=dt*c/dx
print(f'dt*c/dx    (Courent Number) = {Co}') 

#define initial condition
u0_gausian=lambda x,a,s: np.exp(-(x-a)**2/(s*s))
u0=u0_gausian(x,1,0.25)

#u0_sin=lambda x,f: np.sin(f*np.pi*x)
#u0=u0_sin(x,0.5)

# u0=np.zeros_like(x)
# u0[n//2]=1

# u0=np.ones_like(x)
# u0[int(nx/5):int(2*nx/5)]=2

# plt.plot(x,u0,'-',color='r')


#declare a container to store the solution at each time step
sol=[]
#declare the soluation array containing ghost points
u=np.zeros(nx+2)
u[1:-1]=u0
#apply periodic conditions
u[0]=u[-3]
u[-1]=u[2]

sol.append(u)
t=0.0
tend=nt*dt
#time-stepping loop
scheme=input("enter F:forward, B:backward, C:centrel=")
while t<tend:
    un=sol[-1]
    unew=np.zeros_like(u)
    #upadating the unew
    if scheme=="F":
        s= "Forward"
        unew[1:-1]=un[1:-1] -(c*dt/(dx))*(un[2:]-un[1:-1])
    elif scheme=="B":
        s= "Backward"
        unew[1:-1]=un[1:-1] -(c*dt/(dx))*(un[1:-1]-un[:-2])
    elif scheme=="C":
        s= "Central"
        unew[1:-1]=un[1:-1] -(c*dt/(2*dx))*(un[2:]-un[:-2])
    else:
        s= "Generalized Upwind"
        unew[1:-1]=un[1:-1] -(dt/dx)*( (c-np.abs(c))*(un[2:]-un[1:-1]) + (c+np.abs(c))*(un[1:-1]-un[:-2]) )/2

    #apply periodic conditions
    unew[-1]=unew[2]
    unew[0]=unew[-3]
    sol.append(unew)
    t+=dt



for solution in sol[1:]:
     # output frequency for frames
    plt.plot(x, solution[1:-1], '-',alpha=0.6)
    plt.ylim(0, 2.1)

plt.text(0.0,2,f'c= {c} dx={dx:.2f} dt={dt:.2f} Co={Co:.2f} scheme={s}', fontsize='12')
plt.xlabel('x')
plt.ylabel('u')

# #Animation

# fig, ax = plt.subplots(figsize=(6, 4), dpi=200)

# # Initial plot
# line1, = ax.plot(x, sol[0][1:-1], '-', color='b', markersize=2, label='Time-evolving solution')
# line2, = ax.plot(x, u0, '-', color='r', label='Initial condition')

# ax.set_xlabel("x")
# ax.set_ylabel("u")
# ax.set_title("1D Linear Convection")
# ax.set_ylim(0, 1.5)
# ax.grid(True)
# ax.legend()

# def update(frame):
#     line1.set_ydata(sol[frame][1:-1])
#     return line1,

# ani = animation.FuncAnimation(fig, update,frames=range(0, len(sol), 1), interval=100)

# # Save as GIF
# ani.save("1D_Linear_Convection_final.gif", writer="pillow")



plt.show()

