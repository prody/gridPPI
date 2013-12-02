import numpy as np

import grid

"""This module defines a class for scoring docked PPI's."""

class Score(object):
    """Base class for handling grid files and scoring docked poses."""

    # atom selections for each grid type (refine later to select atoms)
    grid_types = {'positive' : 'resname ARG HIS LYS', 
                  'negative' : 'resname ASP GLU', 
                  'polar' : 'resname SER THR ASN GLN',
                  'hydrophobic' : 'resname ALA VAL ILE LEU MET PHE TYR TRP'}

    def __init__(self, **kwargs):
        """Receptor grid files are taken as keyword arguments at instantiation. 
	    
	    Ex: myScore = Score(polar = 'defaults_IPRO.dx')

	    """
        # should check here to make sure keywords match standard grid types
        self.grids = kwargs
        
    def scorePose(self, ligand, selection=None):
        """Method for scoring a docked pose.

        Ligand atom selection should already be aligned to the receptor. 
        Optional input selection string is combined with each grid's default
        selection string.

        The final score of a docking is a sum of values in the voxels that are 
        inhabited by the selected atoms on the ligand.

        """

        score = 0

        for gridfile in self.grids:
            
            # get coordinates of appropriate atoms in ligand
            selstr = Score.grid_types[gridfile]
            lig_atoms = ligand.select(selstr)
            if selection:
                lig_atoms = lig_atoms.select(selection)
            lig_coords = lig_atoms.getCoords()
            
            # sum values in sorresponding voxels
            gridDX = grid.OpenDX(gridfile)
            # * * the following line will throw an IndexError if any coords
            # * * are outside of the grid  
            lig_voxels = gridDX.indices(lig_coords)
            score += sum(gridDX[lig_voxels])

        return score
