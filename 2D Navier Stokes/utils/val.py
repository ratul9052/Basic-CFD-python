import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def validation(Re):

    gU_df = pd.read_csv('ghia/ghiaU.csv')
    gV_df = pd.read_csv('ghia/ghiaV.csv')

    Re_target = f"{Re}"  
    u_profile = gU_df[Re_target]
    v_profile = gV_df[Re_target]


    y = gU_df.iloc[:, 0]  
    x = gV_df.iloc[:, 0] 



    myU = np.loadtxt('data/u_alongY.csv', delimiter=',', skiprows=1)  
    myV = np.loadtxt('data/v_alongX.csv', delimiter=',', skiprows=1)

    fig, axes = plt.subplots(1,2, figsize=(12, 6))

    # Plot U-velocity data on the first subplot
    axes[0].plot(u_profile,y,'-X', c='blue', label='GHIA U')
    axes[0].plot(myU[:,1], myU[:,0],'-', c='red', label='Present U')
    axes[0].set_title('Y_Position vs U_velocity [GHIA vs Present]')
    axes[0].set_xlabel('U')
    axes[0].set_ylabel('Y')
    axes[0].legend()  # Add a legend
    axes[0].text(0.45, 0.95, f"Re={Re}", fontsize=12,transform=axes[0].transAxes)

    # Plot V-velocity data on the second subplot
    axes[1].plot(x, v_profile,'-X', c='blue', label='GHIA V')
    axes[1].plot(myV[:,0], myV[:,1],'-', c='red', label='Present V')
    axes[1].set_title('V_velocity vs X_Position [GHIA vs Present]')
    axes[1].set_xlabel('X')
    axes[1].set_ylabel('V')
    axes[1].legend()  
    axes[1].text(0.45, 0.95, f"Re={Re}", fontsize=12, transform=axes[1].transAxes)

    plt.tight_layout() 
    plt.savefig(f"my_plots/Re_{Re}_validation.png") 
    plt.show()
    plt.close(fig)

def validation_channel(u,v,x,y,u_a):

    fig, axes = plt.subplots(1,1, figsize=(12, 6))

    # Plot U-velocity profile data on the plot
    axes.plot(u_a,y,'-X', c='blue', label='Analytical')
    axes.plot(u[:,int(len(x)/2)+1],y,'-', c='red', label='Numerical')
    axes.set_title('Y_Position vs U_velocity_profile')
    axes.set_xlabel('U')
    axes.set_ylabel('Y')
    axes.legend()  
   

    plt.tight_layout()  
    plt.savefig(f"channel_plots/channel_Final_validation({len(x)}X{len(y)}).png") 
    plt.show()
    plt.close(fig)
