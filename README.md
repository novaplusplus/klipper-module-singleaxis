# Single-axis kinematics module for Klipper

Exactly what it says. A simple kinematics module for the Klipper 3D printer firmware (https://www.klipper3d.org/) that creates one stepper motor (X) with all the usual parameters. Basically just a cut down and simplified version of the stock cartesian setup.

You don't need to clone this repository - just download `single_axis.py` and place it into the `klippy/kinematics/` directory of your Klipper install. Set the `kinematics:` option in your `[printer]` config section to `single_axis`

Configured exactly like a typical cartesian config, just without the Y or Z steppers defined. See here: https://www.klipper3d.org/Config_Reference.html#cartesian-kinematics

I have only tested this a little so... have fun!
