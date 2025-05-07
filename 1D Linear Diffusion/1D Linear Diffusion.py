import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#---------1D Diffusion Equation----------#
#         du/dt = nu*d^2u/dx^2           #

#define the grid of spatial and temporal domain 
nx=71 #number of grid points
L=2.0 #length of the domain
x=np.linspace(0,L,nx)
dx=x[1]-x[0]
print(f'dx= {dx}')


nt=151
tend=0.5
dt=tend/(nt-1)



#define initial condition
# u0_gausian=lambda x,a,s: 1*np.exp(-(x-a)**2/(s*s))
# u0=u0_gausian(x,1,0.25)

#u0_sin=lambda x,f: np.sin(f*np.pi*x)
#u0=u0_sin(x,0.5)

# u0=np.zeros_like(x)
# u0[n//2]=1

u0=np.zeros_like(x)
u0[int(nx/4):int(nx/2)]=1

nu=0.125
D=dt*nu/dx/dx
print(f'dt*c/dx^2    (Diffusion Number) = {D}') 

plt.plot(x,u0,'-',color='r')


#declare a container to store the solution at each time step
sol=[]
#declare the soluation array containing ghost points
u=np.zeros(nx)
u=u0
#boundary condition
u[0]=0
u[-1]=0

sol.append(u)
t=0.0

#Generalized Upwind Scheme
while t<tend:
    un=sol[-1]
    unew=np.zeros_like(u)
    #upadating the unew
    unew[1:-1]=un[1:-1] + nu*(dt/dx/dx)*(un[2:] -2*un[1:-1] +un[:-2])   
    sol.append(unew)
    t+=dt


# #plotting
i=0
for solution in sol[1:]:
     # output frequency for frames
    if (i % 5==0):  # output frequency for frames
        plt.plot(x, solution, '-',alpha=0.6)
        plt.ylim(0, 1.5)
    i+=1
plt.text(0.0,1.2,f'nu= {nu:.2f} dx={dx:.2f} dt={dt:.4f} D={D:.2f} \n Forward Time,Center Space(FTCS)', fontsize='12')
plt.xlabel('x')
plt.ylabel('u')

#Animation
#ims=[]
# fig=plt.figure(figsize=[5,4], dpi=200)
# plt.grid()
# i=0
# for solution in sol:
#     if (i % 10==0):  # output frequency for frames
#         im=plt.plot(x, solution, '-', color='b', markersize=2, animated=True)
#         im0=plt.plot(x, u0, '-', color='r', animated=True)
#         plt.ylim(-3, 1.1)
#         ims.append(im + im0)
#     i+=1
# ani=animation.ArtistAnimation(fig, ims, interval=35, blit=True, repeat_delay=1000)
# ani


plt.show()
