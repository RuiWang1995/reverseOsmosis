"""
# @Author: Rui
# @Date: 12/25/20 1:11 AM
# @Description: Testing for functions
# @File: test.py
"""

from MCV.Control.Main import MainBody
from MCV.Control.MassTransfer import MassTransfer
from MCV.Control.PressureDrop import PressureDrop
from MCV.Control.Stage import Stage
from MCV.Control.Steps import Steps
from MCV.Model.Bulk import Bulk
from MCV.Model.Column import Column
from MCV.Model.Feed import Feed
from MCV.Model.Permeate import Permeate
from MCV.Model.PressureVessel import PressureVessel
from MCV.Model.Retentate import Retentate
from MCV.Model.ReverseOsmosisElement import ReverseOsmosisElement
from MCV.Model.Membrane import Membrane
from MCV.Model.SetOfColumns import SetOfColumns

feed1 = Feed(0.997, 298.15, 9.22, 42 / 3600, 0)
permeate1 = Permeate(0.997, 298.15, 9.22, 42/3600, 1)
bulk = Bulk(feed1, permeate1)
print(bulk.density())
print(bulk.diffusivity())
print(bulk.viscosity())
membrane1 = Membrane('TMG20D-400', 1, 37.2, 9.6203e-7, 1.61277e-7, 1, 8.6e-4, 0.9058, 8.126e-4, 2.77e-3, 7.38, 0.34)
pressureVessel1 = PressureVessel(membrane1, 6)
step1 = Steps(24, membrane1, pressureVessel1)
column1 = Column(pressureVessel1, 8)
column2 = Column(pressureVessel1, 4)
column3 = Column(pressureVessel1, 0)
setOfColumns = SetOfColumns(column1, column2, column3)
main1 = MainBody(feed1, step1, setOfColumns)

#print(main1.severalColumnCalculation()[1][0][0].flowRate*3600)

