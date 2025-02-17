# Simulation of an RBMK Nuclear Fission Reactor
## How to use the program
### Keybindings

| Keybindings | |
| --- | --- |
| Up arrow key | Move control rods up |
| Down arrow key | Move control rods down |
| W | Increase the coolant inflow rate |
| S | Decrease the coolant inflow rate |
| E | Decrease the proportion of U-235 in the core |
| D | Decrease the proportion of Xe-125 in the core |
| A | Sets Xe-135 level to a high number |
| Q | Sets U-235 level to a high number |
| 1 | Sets U-235 level to an even higher number |

Pressing **A** will poison the core with xenon to speed up the actual xenon poisoning process which would happen anyway.
> [!CAUTION]
> Pressing **Q** or **1** will cause a reactor meltdown by flooding the core with fissile U-235

## Methodology
### Fission, Fuel Rods and Neutrons
Fission is modelled at a macroscopic scale in order to represent the reactivity of the reactor as a whole. The coolant grid of squares has a grid of circles overlaid on top of it, with each circle representing a large amount of nuclei all acting together. This circle is coloured differently depending on whether the nuclei are uranium-235, the daughter nuclei of fission or xenon. The daughter nuclei are all coloured the same and for simplicity, the decay heating produced by the decay of daughter nuclei is ignored. This might be added at a later date, as it would allow simulation of the Fukushima and Three Mile Island accidents.

Neutrons are represented as smaller circles that can move continuously across the entire screen. Each neutron represents a group of neutrons, and so when a neutron collides with a uranium circle, it has the possibility of undergoing fission. In order to estimate the number of particles each circle represents, it is necessary to know how many neutrons are undergoing fission in the reactor per second, which is approximately $10^{20}$[^8]. Assuming that in our reactor, roughly 100 neutrons are present per second, the scaling factor $N$ is $10^{18}$.This is dependent on the speed of the neutron: fast neutrons are also be modelled, and are slowed down by the graphite moderators. All neutrons produced from fission begin as fast neutrons and travel in random directions. Fast neutrons also have a greater heating effect on the water, although they can be moderated and slowed down by the water until they become thermal neutrons. Fast neutrons have a much lower chance of inducing fission.

### Delayed Neutrons
Another important part of the stability of nuclear reactors are delayed neutrons. Most neutrons in a reactor are released immediately after induced fission, but some of them are released as a result of the deacy of the neutron-rich fission daughter products, which are usually actinides. Most of these decay by beta decay, but some decay by direct neutron emission. These delayed neutrons contribute to the reactivity of the reactor: most reactors are said to be in a *prompt subcritical, delayed critical* state, where the prompt neutrons emitted from fission alone are not enough to sustain the chain reaction, but the delayed neutrons make up the difference. However, this does make it more difficult to reduce the fission rate, as lowering the control rods will not stop delayed neutron emission.

In this project, the probability of a delayed neutron emission in each daughter nucleus is modelled by an **exponential distribution**. In order to simplify the model, the six energy groups of delayed neutron emission are simplified into one using a weighted average of decay constants based on the fraction of all delayed neutron emissions that each group makes up[^1]. The decay constant used is therefore $\lambda = 0.03073421 s^{-1}$.

The distribution is:
```math
X \sim Exp(\lambda)
```
where X is the waiting time between delayed neutron emissions. In the program, each loop of the main code lasts $60ms$. Therefore, for each daughter nuclei, the fixed chance of a delayed neutron each loop is given using the integral of the probability density function of the distribution:
```math
\int_{0}^{0.060} \lambda e^{-\lambda x} \, dx = 0.1842 \% \, (4.s.f.)
```
As the exponential distribution is memoryless, this probability is the same for each loop. The probability used in the simulation is reduced by a factor of 10 to ensure a more balanced output.

### Cross Sections
The probability of a certain nuclear event occuring is determined by a nuclear cross section. The **microscopic** cross section is measured as an area, where a larger area means a greater probability of occuring. It represents the effective target area presented by a single nucleus to an incident neutron beam[^2]. The unit used is the *barn*, where one barn is $10^{-28}m^2$. The symbol for the barn is $b$, and the symbol for the microscopic cross section is $\sigma$. In order to calculate the probability, the **macroscopic** cross section is used. It represents the effective target area of *all* of the nuclei in a given volume of material. It is first calculated as follows:
```math
\Sigma = N \cdot \sigma,
```
where $\Sigma$ is the macroscopic cross section and $N$ is the number of target nuclei per unit volume (atomic number density). The probability of the event occuring is then determined with the formula:
```math
P = 1 - e^{- \Sigma x}
```
where $x$ is the distance travelled through the material. This formula is based on the **exponential attenuation law** and the fall-off of neutron intensity, $I = I_0 e^{- \Sigma x}$[^2]. Since the simulation models large groups of particles acting together, we can simplify this to comparing the cross sections as follows:
```math
P = \frac{\Sigma}{\Sigma + \Sigma \prime}
```
where $\Sigma$ is the macroscopic cross section of the relevant interaction and $\Sigma \prime$ is the macroscopic cross section of all other competing interactions. The simulation assumes that all movement through the nuclei circles results in a collision; in reality, it is possible for the neutrons to move through the material without colliding, the chance for which is based on the atomic number density of the material and total macroscopic cross section.

The following cross sections are used in this project:
- U-235
  - Fission (thermal neutrons): $585.1 b$[^3]
  - Fission (fast neutrons): $1 b$[^2]
  - Absorption by radiative capture (thermal neutrons): $98 b$[^3]
  - Absorption by radiative capture (fast neutrons): $0.15 b$[^3]
  - Total cross section (thermal neutrons): $698.9 b$
  - Total cross section (fast neutrons): $5.894 b$
- Xe-135
  - Absorption by radiative capture (thermal neutrons): $2,778,000 b$[^4]
  - Absorption by radiative capture (fast neutrons): $40 b$[^4]
- Water (coolant)
  - Absorption by radiative capture (thermal neutrons, primarily due to the hydrogen): $0.665 b$[^5]

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
In this equation, $k$ is the thermal conductivity of the liquid, $\rho$ is the density and $C_p$ is the specific heat capacity. As these values are all constant, $\alpha$ is calculated only once and stored in the constants file. For simulation balance, the value of $\alpha$ has been increased to make the diffusion of heat through the system more noticeable.

Next, the **conduction** between the fuel rods and coolant squares is considered. For this, **Newton's law of cooling** is applied between the fuel rod and the coolant, which can be written as:
```math
\frac{dQ}{dt} \propto (T_{Fuel \ rod} - T_{Coolant})
```
In a discrete form, this becomes:
```math
T(i, j) = T(i, j) + h \cdot [T_{Fuel \ rod} - T(i, j)],
```
where h is the heat transfer coefficient. The value of h is usually experimentally determined, as it is difficult to calculate. The real value for a reactor is $5000W/(m^2 \cdot K)$, but it has been adjusted in this simulation for balance. Several simplifications are made in this system: the fuel rods are of a uniform temperature, internal conduction in the fuel rods is ignored, heat transfer is considered to be instantaneous and the value of h is presumed to remain constant. 

After this, a **forced cooling** system is implemented to simulate the inflow of fresh liquid. The flow rate, $\dot{F}$ is modelled as a fraction between 0 and 1 for how aggressively old fluid is replaced with new fluid: $\dot{F} = 1$ means the entire square's coolant is instantly replaced with new fluid at a temperature of $T_{in}$, and $\dot{F} = 0$ results in no forced replacement. This results in the following equation:
```math
T(i, j) = T(i, j) - \dot{F} (T_{i,j} - T_{in})
```
The value of $\dot{F}$ can be varied by the user.

The last consideration is the heating produced by the **moderation and absorbtion of neutrons**. For this the energies of thermal and fast neutrons are used: $0.025 \ eV$ for a thermal neutron[^6] and $2 \ MeV$ for a fast neutron[^7].In an RBMK reactor, graphite is the primary moderator, but light water also serves to slow down and absorb neutrons. In this simulation, the chance for a thermal neutron to be absorbed is assumed to be fixed, although in reality it is dependent on the speed of the neutron. This chance is calculated based off the water absorption cross section, and assumes that each square of water in the simulation is $1m$ in width. As thermal neutron collisions result in a minimal energy transfer to the coolant, they are ignored, and all of the energy of the thermal neutron is transferred to the square that it is absorbed by. The energy of the neutron is then converted to heat by choosing a value for simulation balance. This is in realistic proportion to the energy released by fission.

A larger portion of the energy released by neutron capture is the gamma emission which results from the de-excitation of the nuclues after capturing a neutron. For light water, the hydrogen becomes deuterium and releases a $2.2 \ MeV$ gamma ray. The energy of this gamma ray is transferred to the water through three processes: the ejection of electrons from water molecules (the photoelectric effect), Compton scattering - in which the gamma ray transfers part of its energy to electrons in the water, which further ionize and excite other molecules - and pair production. In the simulation, the energy is simply all transferred as heat energy to the water.

The energy transferred by **moderation of fast neutrons** follows a different process. The number of collisions required to moderate a neutron at $2 MeV$ energy can be estimated using the **logarithmic energy decrement**. To do this we define a parameter $\xi$, which is equal to the average decrease in the neutron's $ln(E)$ per collision. For hydrogen, $\xi \approx 1$, so the number of collisions is:
```math
N \approx \frac{ln(E_{fast}/E_{thermal})}{\xi}
```
which gives $N \approx 18$ using the energy values above. For balance, this is decreased to SOME NUMBER of collisions in the simulation (this hasn't been added yet).

As a final addition, logic is added to make the water evaporate once it reaches $295^oC$. RBMK reactors used water at a very high pressure and at $260^oC$[^9], as it was more thermally efficient at removing heat from the reactor. This also increased the boiling point of the water, allowing the reactor as a whole to operate at a higher temperature. For the coolant, this means it can no longer absorb or moderate neutrons, as it is now much less dense, and so the absorption cross-section is effectively zero. Its temperature is still recorded, as it could cool down with the addition of new water from the pumps.

### References
[^1]: https://www.oecd-nea.org/upload/docs/application/pdf/2019-12/volume6.pdf
[^2]: https://www.nuclear-power.com/nuclear-power/reactor-physics/nuclear-engineering-fundamentals/neutron-nuclear-reactions/microscopic-cross-section/
[^3]: https://wwwndc.jaea.go.jp/cgi-bin/Tab80WWW.cgi?iso=U235&lib=J40
[^4]: https://wwwndc.jaea.go.jp/cgi-bin/Tab80WWW.cgi?iso=Xe135&lib=J40
[^5]: https://www.ncnr.nist.gov/resources/n-lengths/
[^6]: https://www.nrc.gov/reading-rm/basic-ref/glossary/neutron-thermal.html
[^7]: https://www.nuclear-power.com/nuclear-power/reactor-physics/atomic-nuclear-physics/fundamental-particles/neutron/neutron-energy/
[^8]: https://www.nuclear-power.com/nuclear-power/reactor-physics/nuclear-engineering-fundamentals/neutron-nuclear-reactions/reaction-rate/
[^9]: https://www-pub.iaea.org/MTCD/publications/PDF/Pub1211_web.pdf
