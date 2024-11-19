# Simulation of an RBMK Nuclear Fission Reactor
## How to use the program
WIP
## Methodology
### Fission, Fuel Rods and Neutrons
Fission is modelled at a macroscopic scale in order to represent the reactivity of the reactor as a whole. The coolant grid of squares has a grid of circles overlaid on top of it, with each circle representing a large amount of nuclei all acting together. This circle is coloured differently depending on whether the nuclei are uranium, the daughter nuclei of fission or xenon. The daughter nuclei are all coloured the same and for simplicity, the decay heating produced by the decay of daughter nuclei is ignored. This might be added at a later date, as it would allow simulation of the Fukushima and Three Mile Island accidents.

Neutrons are represented as smaller circles that can move continuously across the entire screen. Each neutron represents a group of neutrons, and so when a neutron collides with a uranium circle, it has the possibility of undergoing fission. This is dependent on the speed of the neutron: fast neutrons will also be modelled, and can be slowed down by the graphite moderators. All neutrons produced from fission will begin as fast neutrons and will travel in random directions. Fast neutrons will also have a greater heating effect on the water, although they can be moderated and slowed down by the water until they become thermal neutrons. Fast neutrons have a much lower chance of inducing fission.

The probability of a certain nuclear event occuring is determined by a nuclear cross section. The **microscopic** cross section is measured as an area, where a larger area means a greater probability of occuring. The unit used is the *barn*, where one barn is $10^{-28}m^2$. The symbol for the barn is $b$ or $\sigma$. In order to calculate the probability, the **macroscopic** cross section is first calculated as follows:
```math
\Sigma = N \cdot \sigma,
```
where $\Sigma$ is the macroscopic cross section and $N$ is the number of target nuclei per unit volume. The probability is then determined with the formula:
```math
P = 1 - e^{- \Sigma x}
```
where $x$ is the distance travelled through the material. This formula is based on the **exponential attenuation law** and the fall-off of neutron intensity, $I = I_0 e^{- \Sigma x}$[^1].

The following cross sections were used in this project:
- U-235
  - Fission (thermal neutrons): $585.1 b$[^2]
  - Fission (fast neutrons): $1 b$[^1]
  - Absorption by radiative capture (thermal neutrons): $98 b$[^2]
  - Absorption by radiative capture (fast neutrons): $0.15 b$[^2]
- Xe-135
  - Absorption by radiative capture (thermal neutrons): $2,778,000 b$[^3]
  - Absorption by radiative capture (fast neutrons): $40 b$[^3]
- Water (coolant)
  - Absorption by radiative capture (thermal neutrons, primarily due to the hydrogen): $0.665 b$[^4]

### Heat Transfer
When modelling heat transfer in this project, several things are taken into account. In the coolant system, it is necessary to firstly consider
heat transfer by **conduction** between adjacent squares of coolant on the grid. This is achieved by **Fourier's law of heat conduction**:
```math
\frac{\partial T}{\partial t} = \alpha \nabla^2 T
```
In a discrete form, used in our grid of sqaures simplification, this becomes:
```math
\text{Conduction} = \alpha \cdot \Delta t \cdot [T(i+1, j) + T(i-1, j) + T(i, j+1) +T (i, j-1) - 4 \cdot T(i, j)],
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

The last consideration is the heating produced by the moderation and absorbtion of neutrons. In an RBMK reactor, graphite is the primary moderator, but light water also serves to slow down and absorb neutrons. While in the rest of the program, the neutrons represent only 1 neutron, in the specific case of heating water, they are considered to represent multiple, in order to maintain a more accurate effect. This calculation is based on the energy of the neutron:
```math
T(i, j) = T(i, j) + N \cdot \frac{E_{neutron}}{m_{coolant} \cdot C_p},
```
where N is the number of neutrons represented, functioning as a scaling factor for the heating. In order to estimate this, it is necessary to know how many neutrons are undergoing fission in the reactor per second, which is approximately $10^{20}$[^5]. Assuming that in our reactor, roughly 100 neutrons are present per second, the scaling factor N is $10^{18}$. This equation assumes 100% efficient energy transfer from kinetic energy of the neutron to thermal energy in the coolant.

As a final addition, logic is added to make the water evaporate once it reaches $100^oC$. This means it can no longer absorb or moderate neutrons, as it is now much less dense, and so the absorption cross-section is effectively zero. Its temperature is still recorded, as it could cool down with the addition of new water from the pumps.

### References
[^1]: https://www.nuclear-power.com/nuclear-power/reactor-physics/nuclear-engineering-fundamentals/neutron-nuclear-reactions/microscopic-cross-section/
[^2]: https://wwwndc.jaea.go.jp/cgi-bin/Tab80WWW.cgi?iso=U235&lib=J40
[^3]: https://wwwndc.jaea.go.jp/cgi-bin/Tab80WWW.cgi?iso=Xe135&lib=J40
[^4]: https://www.ncnr.nist.gov/resources/n-lengths/
[^5]: https://www.nuclear-power.com/nuclear-power/reactor-physics/nuclear-engineering-fundamentals/neutron-nuclear-reactions/reaction-rate/
