# Simulation of an RBMK Nuclear Fission Reactor
## How to use the program
WIP
## Methodology
### Heat Transfer
When modelling heat transfer in this project, several things are taken into account. In the coolant system, it is necessary to firstly consider
heat transfer by **conduction** between adjacent squares of coolant on the grid. This is achieved by **Fourier's law of heat conduction**:
```math
\frac{\partial T}{\partial t} = \alpha \nabla^2 T
```
In a disrete form, used in our grid of sqaures simplification, this becomes:
```math
\text{Conduction} = \alpha \cdot \Delta t \cdot [T(i+1, j)+T(i, j+1)+T(i, j-1) - 4 \cdot T(i, j)],
```
where $\alpha$ is the thermal diffusivity of the fluid, which is calculated by:
```math
\alpha = \frac{k}{\rho C_p}
```
In this equation, $k$ is the thermal conductivity of the liquid, $\rho$ is the density and $C_p$ is the specific heat capacity. As these values are all constant, $\alpha$ is calculated only once and stored in the constants file.

Next, the heat transfer around the grid of squares by **convection** is considered. This is calculated using the **Advection-Diffusion Equation**:
```math
\frac{\partial T}{\partial t} + \mathbf{v} \cdot \nabla T = \alpha \nabla^2 T
```
For the discrete form, it is assumed that the fluid velocity $\mathbf{v}$ is constant throughout the time step, and that the fluid is homogeneous (uniform density and specific heat capacity). Therefore, the final discrete term becomes:
```math
\text{Convection} = (1 - F) T(i, j) + \frac{F}{4} \left( T(i+1, j) + T(i-1, j) + T(i, j+1) + T(i, j-1) \right)
```
Here, $F$ is a user defined flow rate. This allows the program to simulate what would happen if, for example, the coolant pumps of the reactor were turned off.

After this, the **conduction** between the fuel rods and coolant squares is considered. For this, **Newton's law of cooling** is applied between the fuel rod and the coolant, which can be written as:
```math
\frac{dQ}{dt} \propto (T_{Fuel rod} - T_{Coolant})
```
In a discrete form, this becomes:
```math
T(i, j) = T(i, j) + k \cdot [T_{Fuel rod} - T(i, j)],
```
where k is the heat transfer coefficient. The value of k is usually experimentally determined, as it is difficult to calculate. In this program, it is taken as $5000W/(m^2 \cdot K)$. Several simplifications are made in this system: the fuel rods are of a uniform temperature, internal conduction in the fuel rods is ignored, heat transfer is considered to be instantaneous and the value of k is presumed to remain constant.

The last consideration is the heating produced by the moderation and absorbtion of neutrons. In an RBMK reactor, graphite is the primary moderator, but light water also served to slow down and absorb neutrons. While in the rest of the program, the neutrons represent only 1 neutron, in the specific case of heating water, they are considered to represent multiple, in order to maintain a more accurate effect. This calculation is based on the energy of the neutron:
```math
T(i, j) += N \cdot \frac{E_{neutron}}{m_{coolant} \cdot C_p},
```
where N is the number of neutrons represented, functioning as a scaling factor for the heating.

As a final addition, logic is added to make the water evaporate once it reaches $100^oC$. This means it can no longer absorb or moderate neutrons, as it is now much less dense, and so the absorption cross-section is effectively zero. Its temperature is still recorded, as it could cool down with the addition of new water from the pumps.
