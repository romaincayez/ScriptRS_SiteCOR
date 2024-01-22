import os, sys
pid_file_path = os.path.join(os.environ.get('userprofile'), 'AppData', 'Local', 'Temp', 'raystation.pid')

with open(pid_file_path) as f:
    os.environ['RAYSTATION_PID'] = f.read()

script_client_path = r'C:\Program Files\RaySearch Laboratories\RayStation 12A-SP1\ScriptClient'
sys.path.append(script_client_path)

from connect import *

plan = get_current("Plan")
case = get_current("Case")
print('toto')
# print('toto : ', plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[0])


for i in range(len(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions)):
    roiName = plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[i].ForRegionOfInterest.Name
    if not case.PatientModel.RegionsOfInterest[roiName].Type == 'Ptv':
        while 'ptv' in plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[i].ForRegionOfInterest.Name.lower():
            plan.TreatmentCourse.EvaluationSetup.DeleteClinicalGoal(FunctionToRemove=plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[i])



# try:
#     while len(plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions) != 0:
#         plan.TreatmentCourse.EvaluationSetup.DeleteClinicalGoal(
#             FunctionToRemove=plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[0])
# except:
#     print('tous les clinical goals sont supprimés')