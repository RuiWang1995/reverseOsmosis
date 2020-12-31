"""
# @Author: Rui
# @Date: 12/29/20 8:53 PM
# @Description: I call it column, which is basically one stage.
                I cannot call it stage because its conflict with class Stage.
                column contains fields including number of pressure vessels and pressure vessel
# @File: Column.py
"""


class Column(object):
    def __init__(self, pressureVessel, numberOfPressureVessels):
        self.pressureVessel = pressureVessel
        self.numberOfPressureVessels = numberOfPressureVessels


