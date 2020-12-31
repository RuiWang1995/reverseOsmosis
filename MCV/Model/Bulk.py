# @Author: Rui
# @Date: 12/25/20 10:03 AM
# @Description: 
# @File: Bulk.py

from MCV.Model.Stream import Stream
import numpy as np


class Bulk(Stream):
    def __init__(self, feed, retentate):
        self.feed = feed
        self.retentate = retentate
        self.location = 3
        self.soluteConcentration = (self.feed.soluteConcentration + self.retentate.soluteConcentration) / 2
        self.temperature = self.feed.temperature
        self.pressure = (self.feed.pressure + self.retentate.pressure) / 2
        self.flowRate = (self.feed.flowRate + self.retentate.flowRate) / 2

    '''
    return viscosity of brine, kg/m s
    density in kg/m3
    diffusivity in m2/s
    temperature in Kelvin
    concentration in kg/m3
    '''
    def viscosity(self):
        return 1.234e-6 * np.exp(0.0212 * self.soluteConcentration + 1965/self.temperature)

    def mf(self):
        return 1.0069 - 2.757e-4 * (self.temperature-273.15)

    def density(self):
        return 498.4 * self.mf() + np.sqrt(248400 * self.mf()**2 + 752.4 * self.mf() * self.soluteConcentration)

    def diffusivity(self):
        return 6.72510e-6 * np.exp(0.154610e-3*self.soluteConcentration - 2513/self.temperature)
