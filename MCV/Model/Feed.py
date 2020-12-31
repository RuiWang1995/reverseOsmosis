# @Author: Rui
# @Date: 12/25/20 12:39 AM
# @Description: 
# @File: Feed.py
from MCV.Model.Retentate import Retentate
from MCV.Model.Stream import Stream
from MCV.Model.Permeate import Permeate


class Feed(Stream):
    location = 0

    def toPermeate(self):
        permeate = Permeate(self.soluteConcentration, self.temperature, 1, self.flowRate, 1)
        return permeate

    def toRetentate(self):
        retentate = Retentate(self.soluteConcentration, self.temperature, self.pressure, self.flowRate, 2)
        return retentate

