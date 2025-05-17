# Basic CFD Python

This repository contains a collection of small CFD projects, built using Python and finite difference methods. It ranges from 1D convection and diffusion to 2D incompressible Navier–Stokes simulations.

The goal of this work is to learn and understand the basic structure behind numerical simulations — how they are set up from scratch, how the discretization works, and how these abstract equations translate into real, observable behavior. These are not just mathematical formulas, but physical phenomena, and this project is my attempt to feel the physics through the equations.


### 1. 1D Linear Convection

<div align="center">
  <img src="equations/e1.svg"/>
  <br/>
  <img src="gifs/1D_Linear_Convection.gif">
</div>

---
### 2. 1D Diffusion

<div align="center">
  <img src="equations/e2.svg"/>
  <br/>
  <img src="gifs/1D_Diffusion.gif">
</div>

---

### 3. 1D Linear Convection Diffusion

<div align="center">
  <img src="equations/e3.svg"/>
  <br/>
  <img src="gifs/1D_Linear_Convection_Diffusion.gif">
</div>

---

### 4. 1D Nonlinear Convection

<div align="center">
  <img src="equations/e4.svg"/>
  <br/>
  <img src="gifs/1D_Non-Linear_Convection.gif">
</div>
---

### 5. 1D Nonlinear Convection Diffusion (Burgers'    Equation)

<div align="center">
  <img src="equations/e5.svg"/>
  <br/>
  <img src="gifs/1D_Non-Linear_Convection_Diffusion.gif">
</div>
---

### 6. 2D Linear Convection

<div align="center">
  <img src="equations/e6.svg"/>
  <br/>
  <img src="gifs/2D_Linear_Convection.gif">
</div>

---
### 7. 2D Diffusion

<div align="center">
  <img src="equations/e7.svg"/>
  <br/>
  <img src="gifs/2D_Diffusion.gif">
</div>

---

### 8. 2D Linear Convection Diffusion

<div align="center">
  <img src="equations/e8.svg"/>
  <br/>
  <img src="gifs/2D_Linear_Convection_Diffusion.gif">
</div>
---



### 9. 2D Nonlinear Convection Diffusion (Burgers' Equation)


<div align="center">
  <img src="equations/e91.svg"/>
  <br/><br/>
  <img src="equations/e92.svg"/>
  <br/><br/>
  <img src="gifs/2D_Non-Linear_Convection_Diffusion.gif">
</div>


---

### 10. 2D Navier–Stokes

<div align="center">
  <img src="equations/momentum_x.svg"/>
  <br/><br/>
  <img src="equations/momentum_y.svg"/>
  <br/><br/>
  <img src="equations/continuity.svg">
  <br/><br/>
</div>


-  **Cavity Flow**



<div align="center">
  
| Re = 100 | Re = 400 | Re = 1000 |
|---------|----------|-----------|
| <img src="gifs/cavity_Re=100.gif"/> | <img src="gifs/cavity_Re=400.gif"/> | <img src="gifs/cavity_Re=1000.gif"/> |

</div>



- **Channel Flow**

<div align="center">
  <img src="gifs/channel_flow.gif"/>
</div>

---

## Acknowledgments

Much of my understanding came from exploring open resources and excellent online tutorials. I want to thank the following creators whose work helped me build this project:

- [Prof. Saad’s CFD YouTube Playlist](https://youtube.com/playlist?list=PLEaLl6Sf-KICvBLrYFwt5h_LgedJyN59n&si=V7piyexvp5y9BUfY)
- [Zhengtao Gan's Course on CFD](https://drzgan.github.io/Python_CFD/intro.html)
- Various insightful videos and tutorials on finite difference methods and numerical physics

I used their ideas to learn the concepts, then implemented the code myself.

---

## License

This project is licensed under the [MIT License](LICENSE).
