from agent import *


notes = """
AC availability 
Oxybutynin (Ditropan) 2.5mg, 3meg, Smeg 
Solifenacin 5mg, 10mg 
Tolterodine (Detrusitol) Img, 2mg, 4mg 
Darifenacin (Emselex) 7.5mg, 15 mg 
Propantheline (Pro-banthine) 15mg

AC side effects: 
Falls, urinary retention, blurred vision, dry eyes, dry mouth, constipation, increased QT interval, dizziness, confusion, delirium and even cognitive impairment, drowsiness, agitation.
Older patients (over 65) with existing cognitive impairment and those with early stage dementia, age associated memory impairment, or mild cognitive impairment, can be especially vulnerable to cognitive side effects.
ACB rating for anticholinergic risk scale (MARS) is dose dependent.
Avoid anticholinergics with acetylcholine sterase inhibitors.

Altemative management 
Non-pharmacological support: 
Symptom diary, attention to fluid intake, avoiding constipation, bladder training, timed toileting and incontinence aids, pelvic floor exercises, toileting assistance.

Switching within drug class or consider alternative therapy: 
Consider changing formulation or switching to another antimuscarinic medication if anticholinergic medication is effective but cannot be tolerated due to adverse drug reactions.

"""


reason_task = AgentNode(desc = 'Find out if the user is taking Anticholinergics for a listed condition or not',
                        prerequisites = {'medication': 'AC'},
                        success = 'reason',
                        acceptable = {"Listed condition": "The user is taking AC for any of the following conditions: Urinary incontinence, history of urinary frequency, urinary urgency, neurogenic bladder instability, adult enuresis, gastrointestinal disorders characterised by smooth muscle spam", 
                                      "Non listed condition": "The user is not taking AC for urinary incontinence"
                                     })

effective_task = AgentNode(desc = 'Find out the effectiveness of treatement according to patient',
                        prerequisites = {'medication': 'AC', 'reason': 'Listed condition'},
                        success = 'effectiveness',
                        acceptable = {"Effective": "Urinary incontinence has improved and adverse effects are not apparent or not significant to the patient", 
                                      "Ineffective": "No improvement in symptoms, use of multiple medications with anticholinergic effects, concurrent or planned treatement with acetylcholinesterase inhibitiros for dementia, innapropriate indication or no current indication, presence or risk of adverse effects, drug interactions, drug-disease interaction, high drug burden index, poor adherence, or patient preference"
                                     })

acb_task = AgentNode(desc = f'Find out all the drugs the user is taking that belong to this list {meds_list}. The user may give their drugs under their commercial name, in which case you will have to match the medication with its pharmaceutical name from the list above.',
                        prerequisites = {'medication': 'AC', 'reason':'Listed condition', 'effectiveness': 'Effective'},
                        success = 'meds',
                        acceptable = {"[List of the medications the user is taking]": "The user lists all the drugs he is taking. The medications listed match the provided list above. Example answer: [Trospium, Alprazolam]",
                                      "None": "The user lists all of the drugs he is taking. None of which match with the medications listed"
                        })

deprescribe_task = AgentNode(desc = "Positive",
                             prerequisites=[{'medication': 'AC', 'reason':'Listed condition', 'effectiveness': 'Effective', 'meds': '['},
                                            {'medication': 'AC', 'reason':'Listed condition', 'effectiveness': 'Ineffective'}],
                             success=None,
                             acceptable=None,
                             preprocess = calc_acb)
continue_task = AgentNode(desc = "Negative",
                             prerequisites={'medication': 'AC', 'reason':'Listed condition', 'effectiveness': 'Effective', 'meds': 'None'},
                             success=None,
                             acceptable=None,
                             preprocess = None)



ac_tasks = [reason_task, effective_task, acb_task, deprescribe_task, continue_task]