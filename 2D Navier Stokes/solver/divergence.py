import numpy as np

def ddy(f,dy):
    result = np.zeros_like(f)
    result[1:-1,1:-1]=(f[2:,1:-1]-f[:-2,1:-1])/2/dy
    return result  

def ddx(f,dx):
    result = np.zeros_like(f)
    result[1:-1,1:-1]=(f[1:-1,2:]-f[1:-1,:-2])/2/dx
    return result

def div(u,v,dx,dy):
    div_uv=np.zeros_like(u)
    div_uv[1:-1,1:-1]= 0.5*(u[1:-1,2:]-u[1:-1,:-2])/dx\
                     + 0.5*(v[2:,1:-1]-v[:-2,1:-1])/dy

    return div_uv   