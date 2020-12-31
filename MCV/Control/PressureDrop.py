# @Author: Rui
# @Date: 12/25/20 10:01 AM
# @Description: 
# @File: PressureDrop.py


class PressureDrop(object):
    def __init__(self, reverseOsmosisElement):
        self.reverseOsmosisElement = reverseOsmosisElement

    def reynoldsNumber(self):
        return self.reverseOsmosisElement.bulk.density() * \
               self.reverseOsmosisElement.membrane.hydraulicDiameter * \
               self.reverseOsmosisElement.bulk.flowRate / \
               self.reverseOsmosisElement.membrane.thickness / \
               self.reverseOsmosisElement.membrane.width/self.reverseOsmosisElement.bulk.viscosity()

    def pressureDrop(self, length):
        deltaP = 9.8692e-6*self.reverseOsmosisElement.membrane.charA * \
                 self.reverseOsmosisElement.bulk.density() * self.reverseOsmosisElement.bulkVelocity()**2 * length / 2 \
                 / self.reverseOsmosisElement.membrane.hydraulicDiameter / \
                 self.reynoldsNumber() ** self.reverseOsmosisElement.membrane.charN
        return deltaP



