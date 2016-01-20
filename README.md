#Genesis

##What is Genesis

Genesis is acronym for **G**enetically **E**volved **N**euralnetwork **E**nvironment **S**ystem **I**n **S**imualtion. Or something like that.
This is a project where I learn Neural Networks, Physics Simulation and 3D Rendering of the simulated world.
The code is in python3, which was chosen because of the ease of development and to maximize the speed of progress and writing code.

##Goal
Besides learning, this project has some ambitious goals:

- Simulation of a 3D world, with all neccessary physics involved
  - Real simulation of movement of bodies on ground or in water
  - Movements of a body capable of controlling its bodyparts
- Creatures using Neural Network to survive and reproduce
  - Natural Selection is not part of the system, it happens naturally when a creature cannot pass it's genes.
  - The creatures vitality is not determined by the simulation, there is no fittness, only survival or death.
  - The environment changes over time, first provides more food and movement is cheaper, later it can become harder to staying alive.
  - Everithing is edible, including you.
  - The genom describes not only the Neural Network but also the body structure itself.
  - The creature has random chance to get special predefined mutations (like eye, proximity sensor ...)
- Rendering the world in real time in 3D

##Getting Started
###Requirements

- python 3.x - I wrote in 3.5, tested on 3.4, latest python3 recommended
- works on Linux (Ubuntu) and Windows
- developed on x86_64 platform, it may need 64bit python to get enough memory
- additional dependencies may change over time
  - **necessary:**
    - numpy
    - scipy
  - **planned:**
    - pygame or pyopengl
    - pybrain
- I use PyCharm IDE

###Development

It is a personal hobby project, feel free to fork or even send pull requests, but the **ONE and ONLY** goal of this project for me is to learn these things, others solving the problems and giving me the answers misses the point entirely.
