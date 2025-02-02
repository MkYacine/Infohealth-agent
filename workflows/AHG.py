from agent import *

notes = """
Drug | Causes hypoglycemia?
Alpha-glucosidase inhibitor | No
Dipeptidyl peptidase-4 (DPP-4) inhibitors | No
Glucagon-like peptide-1 (GLP-1) agonists | No
Insulin | Yes (highest risk with regular insulin and NPH insulin)
Meglitinides | Yes (low risk)
Metformin | No
Sodium-glucose linked transporter 2 (SGLT2) inhibitors | No
Sulfonylureas | Yes (highest risk with glyburide and lower risk with gliclazide)
Thiazolidinediones (TZDs) | No
Engaging patients and caregivers:

Some older adults prefer less intensive therapy, especially if burdensome or increases risk of hypoglycemia
Patients and/or caregivers may be more likely to engage in discussion about changing targets or considering deprescribing if they understand the rationale:

Risks of hypoglycemia and other side effects
Risks of tight glucose control (no benefit and possible harm with A1C < 6%)
Time to benefit of tight glucose control
Reduced certainty about benefit of treatment with frailty, dementia or at end-of-life


Goals of care: avoid hyperglycemic symptoms (thirst, dehydration, frequency, falls, fatigue, renal insufficiency) and prevent complications (5-10 years of treatment needed)
Many countries agree on less aggressive treatment of diabetes in older persons
Reviewing options for deprescribing, as well as the planned process for monitoring and thresholds for returning to previous doses will help engage patients and caregivers

Drugs affecting glycemic control:

Drugs reported to cause hyperglycemia (when these drugs stopped, can result in hypoglycemia from antihyperglycemic drugs) e.g. quinolones (especially gatifloxacin), beta-blockers (except carvedilol), thiazides, atypical antipsychotics (especially olanzapine and clozapine), corticosteroids, calcineurin inhibitors (such as cyclosporine, sirolimus, tacrolimus), protease inhibitors
Drugs that interact with antihyperglycemics (e.g. trimethoprim/sulfamethoxazole with sulfonylureas)
Drugs reported to cause hypoglycemia (e.g. alcohol, MAOIs, salicylates, quinolones, quinine, beta-blockers, ACEIs, pentamidine)

Hypoglycemia information for patients and caregivers:

Older frail adults are at higher risk of hypoglycemia
There is a greater risk of hypoglycemia with tight control
Symptoms of hypoglycemia include: sweating, tachycardia, tremor BUT older patients may not typically have these
Cognitive or physical impairments may limit older patient's ability to respond to hypoglycemia symptoms
Some drugs can mask the symptoms of hypoglycemia (e.g. beta blockers)
Harms of hypoglycemia may be severe and include: impaired cognitive and physical function, falls and fractures, seizures, emergency room visits and hospitalizations
"""

patient_task = AgentNode(desc = 'Find if the user is a 65 years old (or older) patient with type 2 diabetes.',
                     prerequisites = {'medication': 'AHG'},
                     success = 'patient',
                     acceptable = {"Yes": "The user is 65 years old or older type 2 diabetes patient", 
                                   "No": "The user is NOT 65 years old or older type 2 diabetes patient"})

criteria_task = AgentNode(desc = """Find out if the user meets one or more of the following criteria:
-At risk of hypoglycemia due to advancing age, overly intense glycemic control, multiple comorbidities, drug interactions, hypoglycemia history or unawareness, impaired renal function, or on sulfonylurea or insulin.
-Experiencing, or at risk of, adverse effects from antihyperglycemic
-Uncertain of clinical benefit due to frailty, dementia or limited life-expectancy
""",
                              prerequisites = {'medication': 'AHG', 'patient': 'Yes'},
                              success = 'criteria',
                              acceptable = {"Yes": "The user meets one or more of the listed criteria.",
                                       "No": "The user does not meet any one of the listed criteria."})

at_risk_task = AgentNode(desc = """Address potential contributors to hypoglycemia (e.g. not eating, drug interactions such as trimethoprim/sulfamethoxazole and sulfonylurea, recent cessation of drugs causing hyperglycemia), and find out if user thinks they're still at risk after addressing these.
""",
                        prerequisites = {'medication': 'AHG', 'patient': 'Yes', 'criteria': 'Yes'},
                        success = 'risk',
                        acceptable = {"Yes": "The user confirms they are at risk.",
                                       "No": "The user is not at risk."})

deprescribing_task = AgentNode(desc = "Positive",
                              prerequisites= {'medication': 'AHG', 'patient':'Yes', 'criteria': 'Yes', 'risk': 'Yes'},
                              success = None,
                              acceptable = None)
continue_task = AgentNode( desc = "Negative",
                          prerequisites = [
                              {'medication': 'AHG', 'patient':'No'},
                              {'medication': 'AHG', 'patient':'Yes', 'criteria': 'No'},
                              {'medication': 'AHG', 'patient':'Yes', 'criteria': 'Yes', 'risk': 'Yes'},
                                          ],
                          success = None,
                          acceptable = None)

ahg_tasks = [patient_task, criteria_task, at_risk_task, deprescribing_task, continue_task]