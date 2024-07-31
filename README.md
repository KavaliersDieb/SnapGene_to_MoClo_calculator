# SnapGene_to_MoClo_calculator
This program reads the latest step of the cloning history in a SnapGene file (Version 6 works. Version 7 does not work!), gets all the plasmid name and sizes and will calculate a optimial molar ratio for Golden Gate / Gibson assembly reactions. It will also consider your DNA concentrations, which can allow for an easier lab workflow.

This code is based on the [SnapGeneFileReader](https://github.com/IsaacLuo/SnapGeneFileReader), developed by [IsaacLuo](https://github.com/IsaacLuo).
I modified it a bit, gave it a GUI and added the molarity calculator. 

[This](https://www.promega.de/en/resources/tools/biomath/) formula was used for the calculations.
