# @Author: Rui
# @Date: 12/25/20 12:39 AM
# @Description: 
# @File: MassTransfer.py


class MassTransfer(object):
    def __init__(self, reverseOsmosisElement):
        self.reverseOsmosisElement = reverseOsmosisElement

    def schmidtNumber(self):
        return self.reverseOsmosisElement.bulk.viscosity() / self.reverseOsmosisElement.bulk.density() / \
               self.reverseOsmosisElement.bulk.diffusivity()

    def reynoldsNumber(self):
        return self.reverseOsmosisElement.bulk.density() * \
               self.reverseOsmosisElement.membrane.hydraulicDiameter * \
               self.reverseOsmosisElement.bulk.flowRate / \
               self.reverseOsmosisElement.membrane.thickness / \
               self.reverseOsmosisElement.membrane.width/self.reverseOsmosisElement.bulk.viscosity()
    '''
    return mass transfer coefficient, m/s
    '''
    def massTransferCoefficient(self):
        return 0.664 * self.reverseOsmosisElement.membrane.kdc * self.reynoldsNumber()**0.5 * \
               self.schmidtNumber()**0.33 * self.reverseOsmosisElement.bulk.diffusivity() / \
               self.reverseOsmosisElement.membrane.hydraulicDiameter * \
               (2*self.reverseOsmosisElement.membrane.hydraulicDiameter /
                self.reverseOsmosisElement.membrane.lengthOfFilament)**0.5
