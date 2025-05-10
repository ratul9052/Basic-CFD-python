import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm


#----------------2D Laplace Equation-----------------#
#              d^2p/dx^2 +d^2u/dy^2 = 0              #

#define domain
Lx=2
Ly=1
nx=51
ny=51
x=np.linspace(0,Lx,nx)
dx=x[1]-x[0]
y=np.linspace(0,Ly,ny)
dy=y[1]-y[0]

X,Y=np.meshgrid(x,y)

#set up
p=np.zeros([ny,nx])
p_a=np.zeros([ny,nx])
su=np.zeros([ny,nx])

#--------------------------analytical soluation---------------------------#
sc=lambda x,y,n: (np.sinh(n*np.pi*x)*np.cos(n*np.pi*y))/(np.sinh(2*np.pi*n)*(n*np.pi)**2)
for n in range(1,100,2):
    su+=sc(X,Y,n)
p_a=X/4.0 - 4.0*su


#tolerance
beta=1.75
tol=1e-4
error=1e10
max_it=10000
it=0
while error>tol and it<max_it:
    p_k=p.copy()
    #Boundary condtion
    p[:,-1]=y #right wall
    p[:,0]=0.0 #left wall
    p[0,:]=p[1,:]#bottom wall
    p[-1,:]=p[-2,:]#top wall

    for i in range(1, nx-1):
        for j in range(1, ny-1):
            #jacobi iterative method
            #p[j, i] = 1.0 / 2.0 / (dx * dx + dy * dy) * (dy * dy * (p_k[j, i+1] + p_k[j, i-1])+ dx * dx * (p_k[j+1, i] + p_k[j-1, i]))
 
            #gauss-seidel iterative method
            #p[j, i] = 1.0 / 2.0 / (dx * dx + dy * dy) * (dy * dy * (p[j, i+1] + p[j, i-1])+ dx * dx * (p[j+1, i] + p[j-1, i]))

            #SOR
            p[j, i] = beta*1.0 / 2.0 / (dx * dx + dy * dy) * (dy * dy * (p[j, i+1] + p[j, i-1])+ dx * dx * (p[j+1, i] + p[j-1, i])) +(1-beta)*p_k[j,i]

    diff = p - p_k #difference between current and previous iteration
    error = np.linalg.norm(diff, 2) #l2 norm of the difference
    it+=1

if it==max_it:
    m=f"tolerance = {tol} \nsoluation did not converge in:{it} iterations \nerror={error}"
else:
    m=f"tolerance = {tol} \nsolution converged in: {it} iterations"


#plotting 
fig=plt.figure("2D Laplace", figsize=(20,15),constrained_layout=True)
ax1=fig.add_subplot(2,2,1)
ax2=fig.add_subplot(2,2,2)
ax3=fig.add_subplot(2,2,3,projection='3d')
ax4=fig.add_subplot(2,2,4,projection='3d')

ax1.contourf(X,Y,p,levels=50,cmap="jet")
ax1.text(0.0, 0.7,m,fontsize=12,color='w', transform=ax1.transAxes)
ax1.set_title(f"Numerical(SOR) iteration={it}")
ax1.set_xlabel("x")
ax1.set_ylabel("y")

ax3.plot_surface(X,Y,p,cmap="jet")
ax3.view_init(elev=20, azim=300)
ax3.set_xlabel("x")
ax3.set_ylabel("y")
ax3.set_zlabel("p")
ax3.set_title("Numerical")

ax4.plot_surface(X,Y,p_a,cmap="jet")
ax4.view_init(elev=20, azim=300)
ax4.set_xlabel("x")
ax4.set_ylabel("y")
ax4.set_zlabel("p")
ax4.set_title("Analytical")



for i in range(0,len(y),15):
    # output frequency for frames
    color = f"C{i//30}"  # uses matplotlib's default cycle, safely
    ax2.plot(x, p[i], '-', alpha=0.8, color=color, label=f"y={y[i]:.2f} Analytical")
    ax2.plot(x, p_a[i], 'o', alpha=0.4, color=color,label=f"y={y[i]:.2f} Numerical")
    ax2.set_xlabel("x")
    ax2.set_ylabel("p")
    ax2.set_title("Analytical vs Numerical")
    ax2.legend()
plt.show()
