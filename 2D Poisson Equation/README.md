## 2D Poisson Equation

<p align="center">
  <img src="e.svg" alt="Equation"><br>
</p>

The following results present simulations of the 2D Poisson equation solved using iterative methods. Three different numerical approaches were employed: Jacobi, Gauss-Seidel, and Successive Over-Relaxation (SOR). Each method was implemented using finite difference discretization and the results were compared against the analytical solution. Among the three, the SOR method demonstrated the most efficient convergence, completing the calculation in approximately 300 iterations. The Gauss-Seidel method followed with convergence around 2,000 iterations, while the Jacobi method was the least efficient, requiring nearly 3,000 iterations to reach a similar level of accuracy. The corresponding solution plots for each method are given below. 


*2D Poisson - Jacobi (iteration=3141)*
![2D Poisson - Jacobi](plots/2D_Poisson_j.png)


---
*2D Poisson - Gauss-Seidel (iteration=1747)*
![2D Poisson - Gauss-Seidel](plots/2D_Poisson_gs.png)


---
**2D Poisson - SOR (iteration=310)**
![2D Poisson - SOR](plots/2D_Poisson_sor.png)





