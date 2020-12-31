# @Author: Rui
# @Date: 12/25/20 12:38 AM
# @Description: 
# @File: Membrane.py


class Membrane(object):
    def __init__(self, name, length, width, waterPermeabilityConstantAw_25,
                 soluteTransportParameter_25, foulingFactor, thickness, spacerVoidFraction, hydraulicDiameter,
                 lengthOfFilament, charA, charN):
        self.name = name
        self.length = length
        self.width = width
        self.effectiveArea = length*width
        self.waterPermeabilityConstantAw_25 = waterPermeabilityConstantAw_25
        self.soluteTransportParameter_25 = soluteTransportParameter_25
        self.foulingFactor = foulingFactor
        self.spacerVoidFraction = spacerVoidFraction
        self.hydraulicDiameter = hydraulicDiameter
        self.lengthOfFilament = lengthOfFilament
        self.thickness = thickness
        self.charA = charA
        self.charN = charN
        self.kdc = 1.501
