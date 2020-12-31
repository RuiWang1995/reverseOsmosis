# @Author: Rui
# @Date: 12/25/20 4:09 PM
# @Description: 
# @File: Steps.py


class Steps(object):
    def __init__(self, numberOfStages, membrane, pressureVessel):
        self.numberOfStages = numberOfStages
        self.membrane = membrane
        self.pressureVessel = pressureVessel

    def lengthOfEachStep(self):
        return self.membrane.length * self.pressureVessel.numberOfElements / self.numberOfStages

    def effectiveAreaOfEachStep(self):
        return self.membrane.effectiveArea * self.pressureVessel.numberOfElements / self.numberOfStages

    def stepCoefficient(self):
        return 1 / self.numberOfStages


