# @Author: Rui
# @Date: 12/25/20 12:36 AM
# @Description: 
# @File: Stream.py 


class Stream(object):
    def __init__(self, soluteConcentration, temperature, pressure, flowRate, location):
        self.soluteConcentration = soluteConcentration
        self.temperature = temperature
        self.pressure = pressure
        self.flowRate = flowRate
        self.location = location

    '''
    function for osmotic pressure, atm
    concentration in unit of kg/m3
    '''

    def osmoticPressure(self):
        return 0.7994 * self.soluteConcentration * (1 + 0.003 * (self.temperature - 298.15))
