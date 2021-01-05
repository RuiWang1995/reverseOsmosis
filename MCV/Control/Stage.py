# @Author: Rui
# @Date: 12/25/20 5:07 PM
# @Description: 
# @File: Stage.py 

from scipy.optimize import fsolve
import numpy as np
from MCV.Control.MassTransfer import MassTransfer
from MCV.Control.PressureDrop import PressureDrop
from MCV.Model.Bulk import Bulk
from MCV.Model.Feed import Feed
from MCV.Model.Permeate import Permeate
from MCV.Model.Retentate import Retentate
from MCV.Model.ReverseOsmosisElement import ReverseOsmosisElement


class Stage(object):
    def __init__(self, feed, steps):
        self.feed = feed
        self.permeate = feed.toPermeate()
        self.retentate = feed.toRetentate()
        self.bulk = Bulk(feed, self.retentate)
        self.steps = steps

    '''
    A solver for solute concentration in permeate(Cp), kg/m3
    need the value of permeate flow rate, Qp for simplification
    '''

    def findCp(self, Qp):
        Cp_guess = self.feed.soluteConcentration
        Qf = self.feed.flowRate
        Cf = self.feed.soluteConcentration
        Am = self.steps.effectiveAreaOfEachStep()

        def funcDifferenceCp(Cp):
            Cr = (Qf * Cf - Qp * Cp) / (Qf - Qp)
            self.retentate.soluteConcentration = Cr
            self.retentate.flowRate = Qf - Qp
            bulk = Bulk(self.permeate, self.retentate)
            reverseOsmosisElement = ReverseOsmosisElement(bulk, self.steps.membrane)
            massTransfer = MassTransfer(reverseOsmosisElement)
            Cw = Cp + ((Cf + Cr) / 2 - Cp) * np.exp(Qp / Am / massTransfer.massTransferCoefficient())
            Js = reverseOsmosisElement.BsT() * (Cw - Cp)  # kg/m2/s
            Cp_calc = Js * self.steps.effectiveAreaOfEachStep() / Qp  # kg/m3
            return Cp - Cp_calc

        permeateConcentration, = fsolve(funcDifferenceCp, Cp_guess)
        return permeateConcentration

    '''
    A solver for permeate flow rate, Qp in abbreviation
    Basically, the total Qp is initially assumed to be 60% of feed flow rate.
    The fsolve is responsible for solving actual Qp
    Unit: Qp, m3/s
    '''

    def findQp(self):
        Qp_guess = self.feed.flowRate * 0.8 * self.steps.stepCoefficient()

        def funcDifferenceQp(Qp):
            Qf = self.feed.flowRate
            Cf = self.feed.soluteConcentration
            Am = self.steps.effectiveAreaOfEachStep()
            Cp = self.findCp(Qp)
            Cr = (Qf * Cf - Qp * Cp) / (Qf - Qp)
            self.retentate.soluteConcentration = Cr
            self.retentate.flowRate = Qf - Qp
            bulk = Bulk(self.permeate, self.retentate)
            reverseOsmosisElement = ReverseOsmosisElement(bulk, self.steps.membrane)
            pressureDrop = PressureDrop(reverseOsmosisElement)
            self.retentate.pressure = self.feed.pressure - pressureDrop.pressureDrop(self.steps.lengthOfEachStep())
            bulk2 = Bulk(self.permeate, self.retentate)
            NDPfb = bulk2.pressure - self.permeate.pressure - bulk2.osmoticPressure() + self.permeate.osmoticPressure()
            Qp_calc = reverseOsmosisElement.AwT() * Am * NDPfb
            return Qp - Qp_calc

        permeateFlowRate, = fsolve(funcDifferenceQp, Qp_guess)
        return permeateFlowRate

    def showError(self):
        Qp = self.findQp()
        Qf = self.feed.flowRate
        Cf = self.feed.soluteConcentration
        Am = self.steps.effectiveAreaOfEachStep()
        Cp = self.findCp(Qp)
        Cr = (Qf * Cf - Qp * Cp) / (Qf - Qp)
        self.retentate.soluteConcentration = Cr
        self.retentate.flowRate = Qf - Qp
        bulk = Bulk(self.permeate, self.retentate)
        reverseOsmosisElement = ReverseOsmosisElement(bulk, self.steps.membrane)
        pressureDrop = PressureDrop(reverseOsmosisElement)
        self.retentate.pressure = self.feed.pressure - pressureDrop.pressureDrop(self.steps.lengthOfEachStep())
        bulk2 = Bulk(self.permeate, self.retentate)
        NDPfb = bulk2.pressure - self.permeate.pressure - bulk2.osmoticPressure() + self.permeate.osmoticPressure()
        Qp_calc = reverseOsmosisElement.AwT() * self.steps.effectiveAreaOfEachStep() * NDPfb
        massTransfer = MassTransfer(reverseOsmosisElement)
        Cw = Cp + ((Cf + Cr) / 2 - Cp) * np.exp(Qp / Am / massTransfer.massTransferCoefficient())
        Js = reverseOsmosisElement.BsT() * (Cw - Cp)  # kg/m2/s
        Cp_calc = Js * self.steps.effectiveAreaOfEachStep() / Qp  # kg/m3
        return Qp - Qp_calc, Cp - Cp_calc

    def nextStage(self):
        Qp = self.findQp()
        Cp = self.findCp(Qp)
        Qf = self.feed.flowRate
        Cf = self.feed.soluteConcentration
        Qr = Qf - Qp
        Cr = (Qf * Cf - Qp * Cp) / Qr
        self.retentate.soluteConcentration = Cr
        self.retentate.flowRate = Qr
        bulk = Bulk(self.permeate, self.retentate)
        reverseOsmosisElement = ReverseOsmosisElement(bulk, self.steps.membrane)
        pressureDrop = PressureDrop(reverseOsmosisElement)
        Pr = self.feed.pressure - pressureDrop.pressureDrop(self.steps.lengthOfEachStep())
        feedToNextStage = Feed(Cr, self.permeate.temperature, Pr, Qr, 0)
        return feedToNextStage

    def permeateFromThisStage(self):
        Qp = self.findQp()
        Cp = self.findCp(Qp)
        permeateFromStage = Permeate(Cp, self.feed.temperature, 1, Qp, 1)
        return permeateFromStage

    def retentateFromThisStage(self):
        Qp = self.findQp()
        Cp = self.findCp(Qp)
        Qf = self.feed.flowRate
        Cf = self.feed.soluteConcentration
        Qr = Qf - Qp
        Cr = (Qf * Cf - Qp * Cp) / Qr
        self.retentate.soluteConcentration = Cr
        self.retentate.flowRate = Qr
        bulk = Bulk(self.permeate, self.retentate)
        reverseOsmosisElement = ReverseOsmosisElement(bulk, self.steps.membrane)
        pressureDrop = PressureDrop(reverseOsmosisElement)
        Pr = self.feed.pressure - pressureDrop.pressureDrop(self.steps.lengthOfEachStep())
        retentateFromThisStage = Retentate(Cr, self.permeate.temperature, Pr, Qr, 2)
        return retentateFromThisStage
