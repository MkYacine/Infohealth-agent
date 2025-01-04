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

cont = """
Help the user with discontinuining their CHEI prescripiton. Advise the user following these instructions:
Based on this user's answers, continuing the treatement is advised.
Consult geriatrician, psychiatrist or other healthcare professional if considering other reason for deprescribing. 

Extra information notes, use when relevant:
""" + notes

deprescribe = """
Help the user with discontinuining their CHEI prescripiton. Advise the user following these instructions:
Based on this user's answers, discontinuing the treatement is advised.

Engage individuals and caregivers determine their values and preferences and 
discuss potential risks and benefits of continuation and discontinuation.
Taper and then stop: Halve dose (or step down through available dose forms) every 4 weeks to lowest available dose, followed by discontinuation. Plan this in collaboration with the individual/carer and relevant healthcare professionals.
Conduct close periodic monitoring (e.g. every 4 weeks) cognition, function and neuropsychiatric symptoms. Consider other causes of changes (e.g. delirium).

Extra information notes, use when relevant:
Monitoring during tapering and after discontinuation
[Table with columns: Timing of symptoms after dose reduction/discontinuation | Types of symptoms | Action to be taken by family/nurses/care staff | Possible cause*]
Less than 1 week | Severe symptoms, including agitation, aggression, hallucinations or reduced consciousness | Restart previous dose immediately and contact responsible healthcare professional as soon as possible | Adverse drug withdrawal reaction
2 to 6 weeks | Worsening of cognition, behavioural or psychological symptoms or function | Contact responsible healthcare professional and consider restarting previous dose and/or make an appointment to see responsible healthcare professional at the next available time | Re-emergence of symptoms that were being treated by ChEI/memantine
6 weeks to 3 months | Worsening of cognition, behavioural or psychological symptoms or function | Contact responsible healthcare professional at the next available time to make an appointment | Likely progression of condition or possible re-emergence of symptoms that were being treated by ChEI/memantine

3 months | Any | As per usual care | Progression of condition

*Exclude other causes of change in condition (e.g. infection or dehydration) first.

Discuss monitoring plan with the individual/family/carer and write it down for them (e.g. frequency and type of follow-up). Ensure they have a way to contact a clinician if needed.

Engaging individuals and family/carers:
Determining suitability for deprescribing:

Discuss treatment goals – what do they value the most (cognition, quality of life, remaining independent)?
Ask about experience with dementia symptoms when treatment started and over last 6 months.
Ask about side effects.

Helping the individual and family/carers to make an informed decision:

Deprescribing is a trial — medication can be restarted if appropriate.
There are uncertain benefits and harms to both continuing and discontinuing the medication.
Tailor discussion about benefits and harms to the individual.
Explore fears and concerns about deprescribing.
Consider medication costs and local reimbursement/subsidisation criteria.
If the recommendation to deprescribe is being made due to progression of dementia, remind family/carers that the person with dementia may continue to decline after deprescribing, and explain why.
""" + notes



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

deprescribing_task = AgentNode(desc = deprescribe,
                              prerequisites= [
                                  {'medication': 'CHEI', 'reason':'Other'},
                                  {'medication': 'CHEI', 'reason':'Dementia', 'duration': 'Long', 'conditions1': 'Yes'},
                                  {'medication': 'CHEI', 'reason':'Dementia', 'duration': 'Short', 'conditions2': 'Yes'},
                                  {'medication': 'CHEI', 'reason':'Dementia', 'duration': 'Long', 'conditions1': 'No', 'conditions2': 'Yes'}
                                   ],
                              success = None,
                              acceptable = None)
continue_task = AgentNode( desc = cont,
                          prerequisites = [
                              {'medication': 'CHEI', 'reason':'Dementia', 'duration': 'Short', 'conditions2': 'No'},
                              {'medication': 'CHEI', 'reason':'Dementia', 'duration': 'Long', 'conditions1': 'No', 'conditions2': 'No'}
                          ],
                          success = None,
                          acceptable = None)

chei_tasks = [reason_task, duration_task, conditions1_task, conditions2_task, deprescribing_task, continue_task]