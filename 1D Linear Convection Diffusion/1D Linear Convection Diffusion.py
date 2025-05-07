import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#---------1D Convection Diffusion Equation----------#
#         du/dt + c*du/dx = nu*d^2u/dx^2            #

#define the grid of spatial and temporal domain 
nx=61 #number of grid points
L=2.0 #length of the domain
x=np.linspace(0,L,nx)
dx=x[1]-x[0]
print(f'dx= {dx}')

nt=70
dt=0.01

c=3.0 #velocity
nu=0.05

Co=c*dt/dx
D=nu*dt/dx/dx
print(f'c*dt/dx    (Courent Number) = {Co}') 
print(f'nu*dt/dx^2    (Diffusion Number) = {D}') 

#define initial condition
u0_gausian=lambda x,a,s: np.exp(-(x-a)**2/(s*s))
u0=u0_gausian(x,1,0.25)

#u0_sin=lambda x,f: np.sin(f*np.pi*x)
#u0=u0_sin(x,0.5)

# u0=np.zeros_like(x)
# u0[n//2]=1

# u0=np.ones_like(x)
# u0[int(nx/5):int(2*nx/5)]=2

plt.plot(x,u0,'-',color='r')


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
        unew[1:-1]=un[1:-1] -(c*dt/(dx))*(un[2:]-un[1:-1]) + nu*(dt/dx/dx)*(un[2:] -2*un[1:-1] +un[:-2])  
    elif scheme=="B":
        s= "Backward"
        unew[1:-1]=un[1:-1] -(c*dt/(dx))*(un[1:-1]-un[:-2]) + nu*(dt/dx/dx)*(un[2:] -2*un[1:-1] +un[:-2]) 
    elif scheme=="C":
        s= "Central"
        unew[1:-1]=un[1:-1] -(c*dt/(2*dx))*(un[2:]-un[:-2]) + nu*(dt/dx/dx)*(un[2:] -2*un[1:-1] +un[:-2]) 
    else:
        s= "Generalized Upwind"
        unew[1:-1]=un[1:-1] -(dt/dx)*( (c-np.abs(c))*(un[2:]-un[1:-1]) + (c+np.abs(c))*(un[1:-1]-un[:-2]) )/2 + nu*(dt/dx/dx)*(un[2:] -2*un[1:-1] +un[:-2]) 

    #apply periodic conditions
    unew[-1]=unew[2]
    unew[0]=unew[-3]
    sol.append(unew)
    t+=dt

##plotting
i=0
for solution in sol[1:]:
     # output frequency for frames
    if (i % 5==0):  # output frequency for frames
        plt.plot(x, solution[1:-1], '-',alpha=0.6)
        plt.ylim(0, 1.5)
    i+=1

plt.text(0.0,1.2,f'c= {c} dx={dx:.2f} dt={dt:.2f} Co={Co:.2f} D={D:.4f} \nConvection terms = {s} scheme \nDiffusion terms = Central scheme', fontsize='12')
plt.xlabel('x')
plt.ylabel('u')

# #Animation
# ims=[]
# fig=plt.figure(figsize=[5,4], dpi=200)
# plt.grid()
# i=0
# for solution in sol:
#     if (i % 10==0):  # output frequency for frames
#         im=plt.plot(x, solution[1:-1], '-o', color='b', markersize=2, animated=True)
#         im0=plt.plot(x, u0, '-', color='r', animated=True)
#         plt.ylim(0, 2.1)
#         ims.append(im + im0)
#     i+=1
# ani=animation.ArtistAnimation(fig, ims, interval=35, blit=True, repeat_delay=1000)
# ani


plt.show()
