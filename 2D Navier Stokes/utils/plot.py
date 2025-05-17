import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
import os
from glob import glob
from natsort import natsorted 



def plot_2d(xx,yy,u,v,p,Re):
    #plotting 
    vel=np.sqrt(u**2+v**2)
    step=2
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))


    contour1 = axes[0].contourf(xx, yy, vel, cmap=cm.jet, levels=255)
    axes[0].streamplot(xx,yy,u,v,linewidth=0.7,color='black',density=[2, 2])
    # axes[0].quiver(xx[::step, ::step], yy[::step, ::step], u[::step, ::step], v[::step, ::step], scale=None)
    axes[0].set_title(f'velocity contour(Re={Re})')
    axes[0].set_xlabel('X')
    axes[0].set_ylabel('Y')
    axes[0].set_xlim(0,xx.max())
    axes[0].set_ylim(0,yy.max())

    fig.colorbar(contour1, ax=axes[0])

    contour2 = axes[1].contourf(xx, yy, p, cmap='plasma')
    axes[1].set_title(f'pressure(Re={Re})')
    axes[1].set_xlabel('X')
    axes[1].set_ylabel('Y')
    axes[1].set_xlim(0,xx.max())
    axes[1].set_ylim(0,yy.max())
    fig.colorbar(contour2, ax=axes[1])

    plt.tight_layout()
    plt.savefig(f"my_plots/Re_{Re}_Contour.png")
    plt.show()
    plt.close(fig)

def plot_2d_channel(xx,yy,u,v,p,dx,dy,x,y):

    vel=np.sqrt(u**2+v**2)
    step=2

    fig, axes = plt.subplots(1, 1, figsize=(15, 5))

    contour1 = axes.contourf(xx, yy, vel, cmap='viridis')
    axes.quiver(xx[::step, ::step], yy[::step, ::step], u[::step, ::step], v[::step, ::step], scale=None)
    axes.plot( u[:,int(len(x)/2)+1]/u.max(), y,'-', c='red', label=r'$u/u_{max}$')
    axes.set_title(f'velocity contour')
    axes.set_xlabel('X')
    axes.set_ylabel('Y')
    axes.legend()

    plt.tight_layout()
    plt.savefig(f"channel_plots/channel_Final_Contour({u.shape[1]}X{u.shape[0]})_c.png")
    plt.show()
    plt.close(fig)


def field_animation(xx,yy,x,y,Re,folder="output"):

    files = natsorted(glob(os.path.join(folder, "*.npz")))
    if not files:
        print("No .npz files found.")
        return

    print("data length=",len(files))

    #animation
    fig, axes = plt.subplots(1, 1, figsize=(5, 5))
    step=2

    def update(index):
        axes.clear()

        data=np.load(files[index])
        u=data['u']
        v=data['v']
        vel=np.sqrt(u**2+v**2)

        # Plot the first contour plot
        contour1 = axes.contourf(xx, yy, vel, cmap=cm.jet,levels=255)
        axes.streamplot(xx,yy,u,v,linewidth=0.7,color='black',density=[2, 2])
        # axes.quiver(xx[::step, ::step], yy[::step, ::step], u[::step, ::step], v[::step, ::step], scale=None)
        # axes.plot( u[:,int(len(x)/2)+1]/u.max(), y,'-', c='black', label=r'$u/u_{max}$')
        axes.set_title(f'velocity contour(Re={Re})',fontsize=16)
        axes.set_xlabel('X')
        axes.set_ylabel('Y')
        axes.set_xlim(0,x.max())
        axes.set_ylim(0,y.max())
        # axes.legend()

        return contour1

    ani = animation.FuncAnimation(fig, update, frames=len(files), interval=100)
    ani.save(f"Animation/cavity_final_Re={Re}.gif", writer="pillow")
    print("animation saved")


