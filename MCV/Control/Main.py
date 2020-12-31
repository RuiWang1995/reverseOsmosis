# @Author: Rui
# @Date: 12/26/20 8:46 PM
# @Description: Main body of the model
# @File: Main.py 
import numpy as np

from MCV.Control.Stage import Stage


def finalArrays(feed, steps):
    Nx = steps.numberOfStages
    feedArray = [feed]
    permeateArray = []
    retentateArray = []
    permeateFlowRate = 0
    totalPermeateSoluteAmount = 0
    for i in range(0, Nx + 1):
        stage = Stage(feedArray[i], steps)
        permeateArray.append(stage.permeateFromThisStage())
        permeateFlowRate += stage.permeateFromThisStage().flowRate
        totalPermeateSoluteAmount += stage.permeateFromThisStage().flowRate * stage.permeateFromThisStage(). \
            soluteConcentration
        retentateArray.append(stage.retentateFromThisStage())
        retentateFlowRate = stage.retentateFromThisStage().flowRate
        retentateSoluteConcentration = stage.retentateFromThisStage().soluteConcentration
        if i < Nx:
            feedArray.append(stage.nextStage())
        permeateSoluteConcentration = totalPermeateSoluteAmount / permeateFlowRate
    return [feedArray, permeateArray, retentateArray, permeateFlowRate, permeateSoluteConcentration,
            retentateFlowRate, retentateSoluteConcentration
            ]


class MainBody(object):
    def __init__(self, feed, steps, setOfColumns):
        self.feed = feed
        self.steps = steps
        self.setOfColumns = setOfColumns

    '''
    return feed array (feed class)
    return permeate array (permeate class)
    return retentate array (retentate class)
    return final permeate flow rate
    return final permeate solute concentration
    return final retentate flow rate
    return final retentate solute concentration
    '''

    def severalColumnCalculation(self):
        if self.setOfColumns.column1 is None:
            return None
        else:
            feed = self.feed
            feed.flowRate = feed.flowRate / self.setOfColumns.column1.numberOfPressureVessels
            listFromColumn1 = finalArrays(feed, self.steps)
            if self.setOfColumns.column2 is None:
                return [listFromColumn1]
            else:
                feed2 = listFromColumn1[0][self.steps.numberOfStages]
                feed2.flowRate = feed2.flowRate * self.setOfColumns.column1.numberOfPressureVessels / self.setOfColumns.column2.numberOfPressureVessels
                listFromColumn2 = finalArrays(feed2, self.steps)
                if self.setOfColumns.column3 is None:
                    return [listFromColumn1, listFromColumn2]
                else:
                    feed3 = listFromColumn2[0][self.steps.numberOfStages]
                    feed3.flowRate = feed3.flowRate * self.setOfColumns.column2.numberOfPressureVessels/ self.setOfColumns.column3.numberOfPressureVessels
                    listFromColumn3 = finalArrays(feed3, self.steps)
                    return [listFromColumn1, listFromColumn2, listFromColumn3]


