# import os, sys
# pid_file_path = os.path.join(os.environ.get('userprofile'), 'AppData', 'Local', 'Temp', 'raystation.pid')
#
# with open(pid_file_path) as f:
#     os.environ['RAYSTATION_PID'] = f.read()
#
# script_client_path = r'C:\Program Files\RaySearch Laboratories\RayStation 12A-SP1\ScriptClient'
# sys.path.append(script_client_path)

from connect import *
from contraintes_OARs import *
from tkinter import ttk
import tkinter as tk
from tkinter import *
from collections import defaultdict


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        plan = get_current("Plan")
        # try:
        #     while len(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions) != 0:
        #         plan.TreatmentCourse.EvaluationSetup.DeleteClinicalGoal(
        #             FunctionToRemove=plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[0])
        # except:
        #     print('tous les clinical goals sont supprimés')

        ### définition des frames
        self.frameComboboxLocation = Frame(self, highlightbackground="gray", highlightthickness=1)
        self.frameComboboxLocation.grid(row=0, column=0)

        self.frameOarEnDoublon = Frame(self, highlightbackground="gray", highlightthickness=1)
        self.frameOarEnDoublon.grid(row=0, column=2, sticky='n', padx = 10)

        self.comboboxLocalisations = ttk.Combobox(self.frameComboboxLocation, values='')
        locations = get_locations()
        self.locationsName = [locations[i]['name'] for i,j in enumerate(locations)]

        self.lblLocalisation = tk.Label(self.frameComboboxLocation, text='Sélectionner la localisation',
                                        font=("Arial", 13))
        self.lblLocalisation.grid(row=1, column=0)

        self.lblEnfantOuAdulte = tk.Label(self.frameComboboxLocation, text='Sélectionner la catégorie',
                                          font=("Arial", 13))
        self.lblEnfantOuAdulte.grid(row=0, column=0)

        self.radioValueAdulteEnfant=tk.StringVar(value = ' ')
        self.radioValueAdulte = tk.Radiobutton(self.frameComboboxLocation,
                                               text='Adulte',
                                               font=("Arial", 13),
                                               variable = self.radioValueAdulteEnfant,
                                               value='Adulte')
        self.radioValueAdulte.grid(row=0, column=1)


        self.radioValueEnfant = tk.Radiobutton(self.frameComboboxLocation,
                                               text='Enfant',
                                               font=("Arial", 13),
                                               variable = self.radioValueAdulteEnfant,
                                               value='Enfant')
        self.radioValueEnfant.grid(row=0, column=2)


        self.obj = GetClinicalGoal()
        self.numberOfFractions = self.obj.getNumberOfFractions()
        prescriptionValue = self.obj.getDosePrescription()
        self.fractionationValue = (prescriptionValue / self.numberOfFractions)/100
        self.oarList = self.obj.getOarList()

        self.fractionation = self.setFractionation(self.fractionationValue)

        self.creationWidgets()


    def tata(self):
        print('aaa  : ', self.radioValueAdulteEnfant.get())

    def creationWidgets(self):
        self.comboboxLocalisations = ttk.Combobox(self.frameComboboxLocation,
                                                  values=self.locationsName,
                                                  state='readonly',
                                                  width=25)
        self.comboboxLocalisations.grid(row=1, column=1, columnspan=2, padx=10)
        self.comboboxLocalisations.bind('<<ComboboxSelected>>', self.getOARsFromLocalisation)


    def setFractionation(self, fractionation):
        if fractionation < 2.2:
            return 'dose séance < 2.2 Gy'
        else:
            return self.numberOfFractions

    def getIdemOar(self, organs):
        listeOarEnDoublon = []
        organs.sort()
        for i in range(len(organs) - 1):
            if organs[i + 1].startswith(organs[i]):
                print(organs[i])
                listeOarEnDoublon.append(organs[i])
            if organs[i].startswith(organs[i + 1]):
                print(organs[i + 1])
                listeOarEnDoublon.append(organs[i + 1])



            # listeOarEnDoublon.append(' '.join(listeOarEnDoublonTemp))
        if len(listeOarEnDoublon) !=0:
            print("listeOarEnDoublonnnnnnnnnnn : ", listeOarEnDoublon)

            ### Définition des labels pour afficher quels fichiers ont été ouverts
            self.lblOarEnDoublon = ttk.Label(self.frameOarEnDoublon, text='OAR en doublon : ',
                                             font=("Arial", 13))
            self.lblOarEnDoublon.grid(row=0, column=0)

            ### Définition du champs qui affiche le chemin du rtplan
            self.afficherOarEnDoublon = tk.Label(self.frameOarEnDoublon, text=listeOarEnDoublon[0],
                                                 font=("Arial", 13))
            self.afficherOarEnDoublon.grid(row=0, column=1)


            self.listeOarEnDoublonLast = []
            for i in organs:
                if listeOarEnDoublon[0] in i:
                    self.listeOarEnDoublonLast.append(i)

            print('ça me gonfle : ', self.listeOarEnDoublonLast)

            ### Définition de la combobox pour selection du doublon
            self.lblOarEnDoublon = ttk.Label(self.frameOarEnDoublon, text='Selectionner l\'organe à inclure: ',
                                             font=("Arial", 13))
            self.lblOarEnDoublon.grid(row=1, column=0)

            self.comboboxLocalisationsEnDoublon = ttk.Combobox(self.frameOarEnDoublon,
                                                      values= self.listeOarEnDoublonLast,
                                                      state='readonly',
                                                      width=25,
                                                               font=("Arial", 13))
            self.comboboxLocalisationsEnDoublon.grid(row=1, column=1)
            # self.comboboxLocalisationsEnDoublon.bind('<<ComboboxSelected>>', self.toto,organs)
            # self.comboboxLocalisationsEnDoublon.bind('<<ComboboxSelected>>', lambda event:self.toto(organs, event))
            self.comboboxLocalisationsEnDoublon.bind('<<ComboboxSelected>>', lambda event: self.toto(organs, self.listeOarEnDoublonLast, event))

        else:
            self.getConstraintsAndObjectives(organs)

    def toto(self, organs, organsDoublon, event):
        print("organDoublonDansToto : ", organsDoublon)
        listeTemp = [i for i in organsDoublon if i != self.comboboxLocalisationsEnDoublon.get()]
        print("aaaaa : ", listeTemp)
        for i in listeTemp:
            organs.remove(i)
        print('organsfffffffffff : ', organs)

        self.getConstraintsAndObjectives(organs)

        print(" ")
        # self.getConstraintsAndObjectives(listeTemp)

    def getOARsFromLocalisation(self, event):
        organs = get_organs(location=self.comboboxLocalisations.get(), patient=self.radioValueAdulteEnfant.get(), fraction=self.fractionation)
        organs = [organs[i]['name'] for i, j in enumerate(organs)]
        print("liste des OARs pour cette localisation : ", organs)
        print('ENFANT OU ADULTE : ', self.radioValueAdulteEnfant.get())

        self.getIdemOar(organs)

        # self.getConstraintsAndObjectives(organs)

    def setGoalCriteria(self, comparison):
        if comparison == '<':
            return "AtMost"
        else:
            return "AtLeast"

    def setGoalType(self, volumeValue):
        if volumeValue == "Dose (Gy)":
            return "AverageDose"
        elif volumeValue == 'Volume (%)':
            return "VolumeAtDose"
        else:
            return "DoseAtAbsoluteVolume"



    def getConstraintsAndObjectives(self, organs):
        print('organes : ', organs)
        plan = get_current("Plan")
        case = get_current("Case")
        vari = self.comboboxLocalisations.get()
        for organ in organs:
            for oar in self.oarList:
                if organ in oar or oar in organ:
                    doseOrgan = get_indication(location=vari,
                                               organ=organ,
                                               fraction=self.fractionation,
                                               patient=self.radioValueAdulteEnfant.get())
                    print("doseOrgan : ", doseOrgan)


                    if len(doseOrgan[0]['organs'][0]['constraints'])!=0:
                        for i in range(len(doseOrgan[0]['organs'][0]['constraints'])):
                            comparisonSign = self.setGoalCriteria(doseOrgan[0]['organs'][0]['constraints'][i]['comparison_sym'])
                            volumeValue = self.setGoalType(doseOrgan[0]['organs'][0]['constraints'][i]['unit'])
                            if volumeValue == "AverageDose":
                                try:
                                    self.obj.addClinicalGoal(RoiName=oar,
                                                             GoalCriteria=comparisonSign,
                                                             GoalType=volumeValue,
                                                             AcceptanceLevel=doseOrgan[0]['organs'][0]['constraints'][i]['value']*100,
                                                             IsComparativeGoal=False,
                                                             BeamSet=None,
                                                             Priority=1,
                                                             ParameterValue=0,
                                                             AssociateToPlan=True
                                                             )
                                except:
                                    print('No ROI or POI named ', oar , ' exists')
                            elif volumeValue == "VolumeAtDose":
                                # try:
                                self.obj.addClinicalGoal(RoiName=oar,
                                                         GoalCriteria=comparisonSign,
                                                         GoalType=volumeValue,
                                                         AcceptanceLevel=doseOrgan[0]['organs'][0]['constraints'][i]['value']/100,
                                                         IsComparativeGoal=False,
                                                         BeamSet=None,
                                                         Priority=1,
                                                         ParameterValue=doseOrgan[0]['organs'][0]['constraints'][i]['volume']*100,
                                                         AssociateToPlan=True
                                                         )
                                # except:
                                #     print('No ROI or POI named ', organ, ' exists')
                            else:
                                # try:
                                self.obj.addClinicalGoal(RoiName=oar,
                                                         GoalCriteria=comparisonSign,
                                                         GoalType=volumeValue,
                                                         AcceptanceLevel=doseOrgan[0]['organs'][0]['constraints'][i]['volume']*100,
                                                         IsComparativeGoal=False,
                                                         BeamSet=None,
                                                         Priority=1,
                                                         ParameterValue=doseOrgan[0]['organs'][0]['constraints'][i]['value'],
                                                         AssociateToPlan=True
                                                         )
                                # except:
                                #     print('No ROI or POI named ', organ, ' exists')

                    if len(doseOrgan[0]['organs'][0]['objectives'])!=0:
                        for j in range(len(doseOrgan[0]['organs'][0]['objectives'])):
                            comparisonSign = self.setGoalCriteria(doseOrgan[0]['organs'][0]['objectives'][j]['comparison_sym'])
                            volumeValue = self.setGoalType(doseOrgan[0]['organs'][0]['objectives'][j]['unit'])
                            if volumeValue == "AverageDose":
                                try:
                                    self.obj.addClinicalGoal(RoiName=oar,
                                                             GoalCriteria=comparisonSign,
                                                             GoalType=volumeValue,
                                                             AcceptanceLevel=doseOrgan[0]['organs'][0]['objectives'][j]['value']*100,
                                                             IsComparativeGoal=False,
                                                             BeamSet=None,
                                                             Priority=2147483647,
                                                             ParameterValue=0,
                                                             AssociateToPlan=True
                                                             )
                                except:
                                    print('No ROI or POI named ', organ, ' exists')
                            elif volumeValue == "VolumeAtDose":
                                # try:
                                self.obj.addClinicalGoal(RoiName=oar,
                                                         GoalCriteria=comparisonSign,
                                                         GoalType=volumeValue,
                                                         AcceptanceLevel=doseOrgan[0]['organs'][0]['objectives'][j]['value']/100,
                                                         IsComparativeGoal=False,
                                                         BeamSet=None,
                                                         Priority=2147483647,
                                                         ParameterValue=doseOrgan[0]['organs'][0]['objectives'][j]['volume']*100,
                                                         AssociateToPlan=True
                                                         )
                                # except:
                                #     print('No ROI or POI named ', organ, ' exists')
                            else:
                                # try:
                                self.obj.addClinicalGoal(RoiName=oar,
                                                         GoalCriteria=comparisonSign,
                                                         GoalType=volumeValue,
                                                         AcceptanceLevel=doseOrgan[0]['organs'][0]['objectives'][j]['volume']*100,
                                                         IsComparativeGoal=False,
                                                         BeamSet=None,
                                                         Priority=2147483647,
                                                         ParameterValue=doseOrgan[0]['organs'][0]['objectives'][j]['value'],
                                                         AssociateToPlan=True
                                                         )
                                # except:
                                #     print('No ROI or POI named ', organ, ' exists')

        try:
            for i in range(len(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions)):
                RoiName = plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[i].ForRegionOfInterest.Name
                if not case.PatientModel.RegionsOfInterest[RoiName].Type == 'Ptv':
                    while ('ptv' in plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[
                        i].ForRegionOfInterest.Name.lower()) or ('opt' in plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[
                        i].ForRegionOfInterest.Name.lower()):
                        plan.TreatmentCourse.EvaluationSetup.DeleteClinicalGoal(
                            FunctionToRemove=plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[i])
        except:
            print('tous les clinical goals sont supprimés')

        sys.exit()
class GetClinicalGoal():
    def __init__(self):
        self.listeOAR = []
        self.examination = get_current("Examination")
        self.case = get_current("Case")
        self.beamset = get_current("BeamSet")
        self.plan = get_current("Plan")

    def getOarList(self):
        listeOAR = [i.Name for i in self.case.PatientModel.RegionsOfInterest if i.Type == 'Organ']

        return listeOAR

    def getNumberOfFractions(self):
        numberOfFractions = self.beamset.FractionationPattern.NumberOfFractions

        return numberOfFractions

    def getDosePrescription(self):
        prescriptionValue = self.beamset.Prescription.PrimaryPrescriptionDoseReference.DoseValue

        return prescriptionValue

    def addClinicalGoal(self, RoiName, GoalCriteria, GoalType, AcceptanceLevel, IsComparativeGoal,
                        Priority,AssociateToPlan=True, BeamSet=None,ParameterValue=0):
        self.plan.TreatmentCourse.EvaluationSetup.AddClinicalGoal(RoiName=RoiName,
                                                                  GoalCriteria=GoalCriteria,
                                                                  GoalType=GoalType,
                                                                  AcceptanceLevel=AcceptanceLevel,
                                                                  ParameterValue=ParameterValue,
                                                                  IsComparativeGoal=IsComparativeGoal,
                                                                  BeamSet=BeamSet,
                                                                  Priority=Priority,
                                                                  AssociateToPlan=AssociateToPlan)


# obj = GetClinicalGoal()
app = Application()
app.mainloop()
