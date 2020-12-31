"""
# @Author: Rui
# @Date: 12/29/20 8:58 PM
# @Description: This is PressureVessel class with fields including membrane element and number of elements in series
# @File: PressureVessel.py
"""


class PressureVessel(object):
    def __init__(self, membrane, numberOfElements):
        self.membrane = membrane
        self.numberOfElements = numberOfElements


