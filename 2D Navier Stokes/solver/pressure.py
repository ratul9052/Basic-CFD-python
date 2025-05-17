import numpy as np

def poisson_vec(p, dx, dy, b):
    pn = np.empty_like(p)
    pn = p.copy()
    it = 0
    err = 1e5
    tol = 1e-5
    maxit = 100
    while it < maxit and err > tol:
        pn = p.copy()
        p[1:-1, 1:-1] = (((pn[1:-1, 2:] + pn[1:-1, 0:-2]) * dy**2 +
                          (pn[2:, 1:-1] + pn[0:-2, 1:-1]) * dx**2) /
                         (2 * (dx**2 + dy**2)) -
                         dx**2 * dy**2 / (2 * (dx**2 + dy**2)) *
                         b[1:-1, 1:-1])

        p[:, -1] = p[:, -2]  # dp/dy = 0 at x = 2
        p[0, :] = p[1, :]    # dp/dy = 0 at y = 0
        p[:, 0] = p[:, 1]    # dp/dx = 0 at x = 0
        p[-1, :] = 0         # p = 0 at the top wall
        err = np.linalg.norm(p.ravel() - pn.ravel(), 2)
        it += 1

    return err

def poisson_vec_channel(p, dx, dy, b):
    pn = p.copy()
    it = 0
    err = 1e5
    tol = 1e-5
    maxit = 100
    while it < maxit and err > tol:
        pn = p.copy()
        p[1:-1, 1:-1] = (((pn[1:-1, 2:] + pn[1:-1, 0:-2]) * dy**2 +
                          (pn[2:, 1:-1] + pn[0:-2, 1:-1]) * dx**2) /
                         (2 * (dx**2 + dy**2)) -
                         dx**2 * dy**2 / (2 * (dx**2 + dy**2)) *
                         b[1:-1, 1:-1])

        #top wall
        p[-1, 1:-1] = p[-2,1:-1]       # dp/dy = 0 at y = 2
        #bottom wall
        p[0, 1:-1] = p[1, 1:-1]        # dp/dy = 0 at y = 0

        #periodic condtion
        #left ghost node [0] = right physical node [-2] or [nx]
        p[:, 0] = p[:, -2]      # dp/dy = 0 at x = 2
        #right ghost node [-1] = left physical node [1]
        p[:, -1] = p[:, 1]        # dp/dx = 0 at x = 0

        # Apply reference pressure in the physical domain
        p[0, 1] = 0.0

        err = np.linalg.norm(p.ravel() - pn.ravel(), 2)
        it += 1

    return p , err