# @Author: Rui
# @Date: 12/25/20 12:37 AM
# @Description: 
# @File: ReverseOsmosisElement.py

from MCV.Model.Bulk import Bulk
from MCV.Model.Membrane import Membrane
import numpy as np


class ReverseOsmosisElement(object):
    def __init__(self, bulk, membrane):
        self.bulk = bulk
        self.membrane = membrane

    def BsT(self):
        T = self.bulk.temperature
        if T <= 298.15:
            TCFs = 1 + 0.05 * (T - 298.15)
        else:
            TCFs = 1 + 0.08 * (T - 298.15)
        return self.membrane.soluteTransportParameter_25 * TCFs

    def AwT(self):
        T = self.bulk.temperature
        if T >= 298.15:
            TCFp = np.exp(0.0343 * (T - 298.15))
        else:
            TCFp = np.exp(0.0307 * (T - 298.15))
        return self.membrane.waterPermeabilityConstantAw_25 * TCFp * self.membrane.foulingFactor

    def bulkVelocity(self):
        return self.bulk.flowRate / self.membrane.width / self.membrane.thickness / \
               self.membrane.spacerVoidFraction

