import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#---------1D Convection Equation----------#
#         du/dt + u*du/dx = 0             #

#define the grid of spatial and temporal domain 
nx=51 #number of grid points
L=2.0 #length of the domain
x=np.linspace(0,L,nx)
dx=x[1]-x[0]
print(f'dx= {dx}')


nt=25
dt=0.04
tend=nt*dt


#define initial condition
u0_gausian=lambda x,a,s: 1*np.exp(-(x-a)**2/(s*s))
u0=u0_gausian(x,1,0.25)

#u0_sin=lambda x,f: np.sin(f*np.pi*x)
#u0=u0_sin(x,0.5)

# u0=np.zeros_like(x)
# u0[n//2]=1

# u0=1*np.ones_like(x)
# u0[int(nx/4):int(nx/2)]=2

c=np.abs(u0).max() #velocity

Co=dt*c/dx
print(f'dt*c/dx    (Courent Number) = {Co}') 

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

#Generalized Upwind Scheme
while t<tend:
    un=sol[-1]
    unew=np.zeros_like(u)
    #upadating the unew
    unew[1:-1]=un[1:-1] -(dt/dx)*( (un[1:-1]-np.abs(un[1:-1]))*(un[2:]-un[1:-1])  + (un[1:-1]+np.abs(un[1:-1]))*(un[1:-1]-un[:-2]) )/2   #(un[1:-1]-np.abs(un[1:-1]))*(un[2:]-un[1:-1]) 
    #apply periodic conditions
    unew[-1]=unew[2]
    unew[0]=unew[-3]
    sol.append(unew)
    t+=dt


# #plotting
i=0
for solution in sol[1:]:
     # output frequency for frames
    if (i % 3==0):  # output frequency for frames
        plt.plot(x, solution[1:-1], '-',alpha=0.6)
        plt.ylim(-1.3, 2.2)
    i+=1
plt.text(0.0,1.6,f'c= {c:.2f} dx={dx:.2f} dt={dt:.2f} Co={Co:.2f} \n Generalized Upwind Scheme', fontsize='12')
plt.xlabel('x')
plt.ylabel('u')

#Animation
#ims=[]
# fig=plt.figure(figsize=[5,4], dpi=200)
# plt.grid()
# i=0
# for solution in sol:
#     if (i % 10==0):  # output frequency for frames
#         im=plt.plot(x, solution[1:-1], '-', color='b', markersize=2, animated=True)
#         im0=plt.plot(x, u0, '-', color='r', animated=True)
#         plt.ylim(-3, 1.1)
#         ims.append(im + im0)
#     i+=1
# ani=animation.ArtistAnimation(fig, ims, interval=35, blit=True, repeat_delay=1000)
# ani


plt.show()
