import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#---------1D Non-Linear Convection Diffusion (Buregers' Equation)----------#
#                  du/dt + u*du/dx = nu*d^2u/dx^2                          #


#define the grid of spatial and temporal domain 
nx=401 #number of grid points
L=2.0 #length of the domain
x=np.linspace(0,L,nx)
dx=x[1]-x[0]
print(f'dx= {dx}')

nt=1000
tend=1
dt=tend/(nt-1)

nu=0.01


#----------------------------initial condtion----------------------------#
#                       u(x,0)= -2*nu* dphi/dx /phi + 4                  #

phi = lambda x: np.exp((-x**2)/(4*nu)) + np.exp((-(x-2*np.pi)**2)/(4*nu))
dphi_dx = lambda x: -2*x/(4*nu)*np.exp((-x**2)/(4*nu)) - (2*(x-2*np.pi))/(4*nu)*np.exp((-(x-2*np.pi)**2)/(4*nu))

u0= -2*nu*dphi_dx(x)/phi(x) + 4

#----------------------------Analytical soluation------------------------#
#                    u(x,t)= -2*nu* dphi/dx /phi + 4                     #

phi = lambda x,t: np.exp((-(x-4*t)**2)/(4*nu*(t+1))) + np.exp((-(x-4*t-2*np.pi)**2)/(4*nu*(t+1)))
dphi_dx = lambda x,t: -2*(x-4*t)/(4*nu*(t+1))*np.exp((-(x-4*t)**2)/(4*nu*(t+1))) - 2*(x-4*t-2*np.pi)/(4*nu*(t+1))*np.exp((-(x-4*t-2*np.pi)**2)/(4*nu*(t+1)))
u_t = lambda x,t: -2*nu*dphi_dx(x,t)/phi(x,t) + 4


# plt.plot(x,u0,'-',color='r')

Co=u0.max()*dt/dx
D=nu*dt/dx/dx
print(f'c*dt/dx    (Courent Number) = {Co}') 
print(f'nu*dt/dx^2    (Diffusion Number) = {D}') 

#declare a container to store the analytical and numerical solution at each time step
a_sol=[]
n_sol=[]
#declare the soluation array containing ghost points
u=np.zeros(nx+2)
u[1:-1]=u0
#apply periodic conditions
u[0]=u[-3]
u[-1]=u[2]

n_sol.append(u)
a_sol.append(u0)

t=0.0
#time-stepping loop
scheme='o' #input("enter F:forward, B:backward, C:centrel=")
while t<tend:
    un=n_sol[-1]
    unew=np.zeros_like(u)
    #upadating the unew
    if scheme=="F":
        s= "Forward"
        unew[1:-1]=un[1:-1] -(un[1:-1]*dt/(dx))*(un[2:]-un[1:-1]) + nu*(dt/dx/dx)*(un[2:] -2*un[1:-1] +un[:-2])  
    elif scheme=="B":
        s= "Backward"
        unew[1:-1]=un[1:-1] -(un[1:-1]*dt/(dx))*(un[1:-1]-un[:-2]) + nu*(dt/dx/dx)*(un[2:] -2*un[1:-1] +un[:-2]) 
    elif scheme=="C":
        s= "Central"
        unew[1:-1]=un[1:-1] -(un[1:-1]*dt/(2*dx))*(un[2:]-un[:-2]) + nu*(dt/dx/dx)*(un[2:] -2*un[1:-1] +un[:-2]) 
    else:
        s= "Generalized Upwind"
        unew[1:-1]=un[1:-1] -(dt/dx)*( (un[1:-1]-np.abs(un[1:-1]))*(un[2:]-un[1:-1]) + (un[1:-1]+np.abs(un[1:-1]))*(un[1:-1]-un[:-2]) )/2 + nu*(dt/dx/dx)*(un[2:] -2*un[1:-1] +un[:-2]) 

    #apply periodic conditions
    unew[-1]=unew[2]
    unew[0]=unew[-3]
    n_sol.append(unew)
    # a_sol.append(u_t(x,t))
    t+=dt





##plotting
# print(len(a_sol),len(n_sol))

for i in range(len(n_sol)):
     # output frequency for frames
    if i==0:
        continue

    elif (i % 30==0):  # output frequency for frames
        color = f"C{i//30}"  # uses matplotlib's default cycle, safely
        plt.plot(x, a_sol[i], '-', alpha=0.8, color=color, label="Analytical Soluation")
        plt.plot(x, n_sol[i][1:-1], '-o', alpha=0.4, color=color,label="Numerical Soulation")


plt.text(0.0,8,f'nu={nu:.3f} dx={dx:.2f} dt={dt:.4f} Co={Co:.2f} D={D:.3f} \nConvection terms = {s} scheme \nDiffusion terms = Central scheme', fontsize='12')
plt.xlabel('x')
plt.ylabel('u')
plt.ylim(0.0,10)
plt.ylim(0.0,10)
plt.legend()


#Animation

# fig, ax = plt.subplots(figsize=(6, 4), dpi=200)

# # Initial plot
# line1, = ax.plot(x, n_sol[0][1:-1], '-', color='b', markersize=2, label='Time-evolving solution')
# line2, = ax.plot(x, u0, '-', color='r', label='Initial condition')

# ax.set_xlabel("x")
# ax.set_ylabel("u")
# ax.set_title("1D Non-Linear Convection Diffusion")
# ax.set_ylim(0, 1.5)
# ax.grid(True)
# ax.legend()

# def update(frame):
#     line1.set_ydata(n_sol[frame][1:-1])
#     return line1,

# ani = animation.FuncAnimation(fig, update,frames=range(0, len(n_sol), 30), interval=1)

# # Save as GIF
# ani.save("1D_Non-Linear_Convection_Diffusion.gif", writer="pillow")

plt.show()
