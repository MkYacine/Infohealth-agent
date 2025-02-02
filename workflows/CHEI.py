from agent import *

notes = """
Non-pharmacological management and ongoing care after deprescribing:
See (http://sydney.edu.au/medicine/cdpc/resources/dementia-guidelines.php) for Australian guidelines on care of people with dementia, including behavioural and psychological symptoms.
ChEI and memantine availability (Australia):
[Table of medications:]
Drug | Strength
Donepezil (Aricept®, Aridon®, Arazil®) | Tablet – 5mg, 10mg
Galantamine (Galantal®, Gamine XR®, Reminyl®) | Controlled release capsule – 8mg, 16mg, 24mg
Rivastigmine (Exelon®) | Capsule – 1.5mg, 3mg, 4.5mg, 6mg; Patch – 4.6mg/24 hours, 9.5mg/24 hours, 13.3mg/24 hours
Memantine (Ebixa®, Memanxa®) | Tablet – 10mg, 20mg
ChEI and memantine side effects:

Common: include gastrointestinal effects, dizziness, confusion, headache, insomnia, agitation, weight loss and falls.
Rare (ChEI): may include urinary, cardiovascular (e.g. bradycardia), pulmonary and dermatological (e.g. Stevens-Johnson syndrome) complications, Pisa syndrome, seizures, gastrointestinal haemorrhage and rhabdomyolysis.
Lack of evidence of potential harms in complex older adults.
"""


reason_task = AgentNode(desc = 'Find out the reason for taking the medication',
                        prerequisites = {'medication': 'CHEI'},
                        success = 'reason',
                        acceptable = {"Dementia": "Alzheimer’s disease, dementia of Parkinson’s disease, Lewy body dementia or vascular dementia.",
                                      "Other": "Any other reason that doens't fit into the other category."
                                     })

duration_task = AgentNode(desc = 'Find out how long the user has been taking their medication',
                     prerequisites = {'medication': 'CHEI', 'reason': 'Dementia'},
                     success = 'duration',
                     acceptable = {"Short": "The user has been taking the medication for less than 1 year", 
                                   "Long": "The user has been taking the medication for 1 year or more"})

conditions1_task = AgentNode(desc = """Find out if the user fulfills one of the following conditions:
-Cognition +/- function significantly worsened over past 6 months (or less, as per individual).
-Sustained decline (in cognition, function +/- behaviour), at a greater rate than previous (after exclusion of other causes).
-Severe/end-stage dementia (dependence in most activities of daily living, inability to respond to their environment +/- limited life expectancy).
-No benefit (i.e., no improvement, stabilisation or decreased rate of decline) seen during treatment.
""",
                     prerequisites = {'medication': 'CHEI', 'reason': 'Dementia', 'duration': 'Long'},
                     success = 'conditions1',
                     acceptable = {"Yes": "The user fulfills one of the listed conditions.", 
                                   "No": "The user does not fulfill any of the listed conditions"})

conditions2_task = AgentNode(desc = """Find out if the user fulfills one of the following conditions:
-Decision by a person with dementia/family/carer to discontinue.
-Non-adherence that cannot be resolved.
-Severe agitation/psychomotor restlessness.
-Non-dementia terminal illness.
-Drug–drug or drug–disease interactions that make treatment risky.
-Refusal or inability to take the medication
""",
                     prerequisites = [
                         {'medication': 'CHEI', 'reason':'Dementia', 'duration': 'Long', 'conditions1': 'No'},
                         {'medication': 'CHEI', 'reason':'Dementia', 'duration': 'Short'},
                                     ],
                     success = 'conditions2',
                     acceptable = {"Yes": "The user fulfills one of the listed conditions.", 
                                   "No": "The user does not fulfill any of the listed conditions"})

deprescribing_task = AgentNode(desc = "Positive",
                              prerequisites= [
                                  {'medication': 'CHEI', 'reason':'Other'},
                                  {'medication': 'CHEI', 'reason':'Dementia', 'duration': 'Long', 'conditions1': 'Yes'},
                                  {'medication': 'CHEI', 'reason':'Dementia', 'duration': 'Short', 'conditions2': 'Yes'},
                                  {'medication': 'CHEI', 'reason':'Dementia', 'duration': 'Long', 'conditions1': 'No', 'conditions2': 'Yes'}
                                   ],
                              success = None,
                              acceptable = None)
continue_task = AgentNode( desc = "Negative",
                          prerequisites = [
                              {'medication': 'CHEI', 'reason':'Dementia', 'duration': 'Short', 'conditions2': 'No'},
                              {'medication': 'CHEI', 'reason':'Dementia', 'duration': 'Long', 'conditions1': 'No', 'conditions2': 'No'}
                          ],
                          success = None,
                          acceptable = None)

chei_tasks = [reason_task, duration_task, conditions1_task, conditions2_task, deprescribing_task, continue_task]