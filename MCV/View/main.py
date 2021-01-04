from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from MCV.Control.Main import MainBody
from MCV.Control.Steps import Steps
from MCV.Model.Column import Column
from MCV.Model.Feed import Feed
from MCV.Model.Membrane import Membrane
from MCV.Model.PressureVessel import PressureVessel
from MCV.Model.SetOfColumns import SetOfColumns

Builder.load_file('design.kv')


class CalScreen(Screen):
    def run(self, membraneName, membraneLength, membraneWidth, Aw_25, Bs_25, foulingFactor, feedSpacerThickness,
            spacerVoidFraction, hydraulicDiameter, lengthOfFilament, charA, charN, steps, feedSoluteConcentration,
            feedTemperature, feedPressure, feedFlowRate, pvInFirstStage, pvInSecondStage, pvInThirdStage,
            elementsInOnePV):
        feed = Feed(float(feedSoluteConcentration), float(feedTemperature), float(feedPressure), float(feedFlowRate) /
                    3600, 0)
        membrane = Membrane(membraneName, float(membraneLength), float(membraneWidth), float(Aw_25), float(Bs_25),
                            float(foulingFactor), float(feedSpacerThickness), float(spacerVoidFraction),
                            float(hydraulicDiameter), float(lengthOfFilament), float(charA), float(charN))
        pressureVessel = PressureVessel(membrane, int(elementsInOnePV))
        step = Steps(int(steps), membrane, pressureVessel)
        self.displayStepSize.text = str(step.lengthOfEachStep())
        if pvInFirstStage == '0':
            column1 = None
        else:
            column1 = Column(pressureVessel, int(pvInFirstStage))
        if pvInSecondStage == '0':
            column2 = None
        else:
            column2 = Column(pressureVessel, int(pvInSecondStage))
        if pvInThirdStage == '0':
            column3 = None
        else:
            column3 = Column(pressureVessel, int(pvInThirdStage))
        setOfColumns = SetOfColumns(column1, column2, column3)
        arrayGenerator = MainBody(feed, step, setOfColumns)
        List = arrayGenerator.severalColumnCalculation()
        self.displayPermeateSoluteConcentrationFromStage1.text = str(int(List[0][4] * 1000) / 1000)
        self.displayPermeateFlowRateFromStage1.text = str(int(List[0][3]*3600 * column1.numberOfPressureVessels * 1000) / 1000)
        self.displayRetentateSoluteConcentrationFromStage1.text = str(int(List[0][6] * 1000) / 1000)
        self.displayRetentateFlowRateFromStage1.text = str(int(List[0][5]*3600 * column1.numberOfPressureVessels * 1000) / 1000)
        self.displayRetentatePressureFromStage1.text = str(int(List[0][2][int(steps)].pressure * 1000) / 1000)
        if column2 is not None:
            self.displayPermeateSoluteConcentrationFromStage2.text = str(int(List[1][4] * 1000) / 1000)
            self.displayPermeateFlowRateFromStage2.text = str(int(List[1][3]*3600 * column2.numberOfPressureVessels * 1000) / 1000)
            self.displayRetentateSoluteConcentrationFromStage2.text = str(int(List[1][6] * 1000) / 1000)
            self.displayRetentateFlowRateFromStage2.text = str(int(List[1][5]*3600* column2.numberOfPressureVessels *1000) / 1000)
            self.displayRetentatePressureFromStage2.text = str(int(List[1][2][int(steps)].pressure * 1000) / 1000)
        else:
            self.displayPermeateSoluteConcentrationFromStage2.text = str(0)
            self.displayPermeateFlowRateFromStage2.text = str(0)
            self.displayRetentateSoluteConcentrationFromStage2.text = str(0)
            self.displayRetentateFlowRateFromStage2.text = str(0)
            self.displayRetentatePressureFromStage2.text = str(0)
        if column3 is not None:
            self.displayPermeateSoluteConcentrationFromStage3.text = str(int(List[2][4] * 1000) / 1000)
            self.displayPermeateFlowRateFromStage3.text = str(int(List[2][3] * 3600 * column3.numberOfPressureVessels * 1000) / 1000)
            self.displayRetentateSoluteConcentrationFromStage3.text = str(int(List[2][6] * 1000) / 1000)
            self.displayRetentateFlowRateFromStage3.text = str(int(List[2][5]*3600* column3.numberOfPressureVessels *1000) / 1000)
            self.displayRetentatePressureFromStage3.text = str(int(List[2][2][int(steps)].pressure * 1000) / 1000)
        else:
            self.displayPermeateSoluteConcentrationFromStage3.text = str(0)
            self.displayPermeateFlowRateFromStage3.text = str(0)
            self.displayRetentateSoluteConcentrationFromStage3.text = str(0)
            self.displayRetentateFlowRateFromStage3.text = str(0)
            self.displayRetentatePressureFromStage3.text = str(0)




class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
