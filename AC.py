from agent import *
import random
acb_drugs = {}


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
cont = """
Based on the user's current treatement, there is no need for discontinuing.
However, we also have to look at the user's ACB scoring. Here is the user's ACB report:
{acb}
Make sure to inform the user of their ACB report, including the detailed scores. 

Extra information notes, use when relevant: 
""" + notes
deprescribe = """
Based on the user's current treatment, deprescribin the AC is recommended. Advise the user following these instructions:
Taper then stop AC.
Accompany weaning with commencement of relevant non-pharmacological therapy.
Wean gradually by 25-50 percent of the daily dose every 1-4 weeks.
If reason for deprescribing is due to serious adverse effects, consider weaning faster.
Provide advice to patient/carer on self-monitoring and what to do if symptoms re-occur.
Adjust according to response if no withdrawal symptoms occur, continue to wean then stop.
Inthe presence of worsening confusion, cease outright.
Consider slower weaning (e.g. 12.5%) when reducing to the final lowest dose.
End treatment 2 weeks after administering the lowest dose.
Consider alternate day dosing to aid with weaning if dosage forms are limited.

In the case of recurrent withdrawal symptoms, revert to the previous lowest tolerated dose.
Recommence weaning after 6-12 weeks at the lower weaning rate (e.g. 5-12.5 percent of daily dose each 
month) then stop.

Here is the user's ACB report:
{acb}
Make sure to inform the user of their ACB report, including the detailed scores.

Extra information notes, use when relevant: 
""" + notes

import json

with open('meds_dict.json', 'r') as f:
    meds_map = json.load(f)
    meds_list = [k for k,_ in meds_map.items()]

def calc_acb(state):
    user_meds = state['user_data']['meds'].strip('[]').replace("'", '').split(', ')
    state['user_data']['acb'] = {'total': 0}
    state['user_data']['acb_evaluation'] = 'Low'
    for m in user_meds:
        score = int(meds_map[m])
        if score > 1:
            state['user_data']['acb_evaluation'] = 'High'
        state['user_data']['acb'][m] = score
        state['user_data']['acb']['total'] += score
    if state['user_data']['acb']['total'] > 2:
        state['user_data']['acb_evaluation'] = 'High'

    if state['user_data']['acb_evaluation'] == 'High':
        injec = f"User's ACB score is too high. Tell the user to refer to clinician for an anticholinergic deprescribing assessment. Detailed report: {str(state['user_data']['acb'])}"
    else:
        injec = f"User's ACB score is below the acceptable threshold. Detailed report: {str(state['user_data']['acb'])}"
    state['curr_node']['desc'].format(acb=injec)


reason_task = AgentNode(desc = 'Find out if the user is taking Anticholinergics for urinary incontinence or not',
                        prerequisites = {'medication': 'AC'},
                        success = 'reason',
                        acceptable = {"Urinary incontinence": "The user is taking AC for urinary incontinence", 
                                      "Not urinary incontinence": "The user is not taking AC for urinary incontinence"
                                     })

effective_task = AgentNode(desc = 'Find out the effectiveness of treatement according to patient',
                        prerequisites = {'medication': 'AC', 'reason': 'Urinary incontinence'},
                        success = 'effectiveness',
                        acceptable = {"Effective": "Urinary incontinence has improved and adverse effects are not apparent or not significant to the patient", 
                                      "Ineffective": "No improvement in symptoms, use of multiple medications with anticholinergic effects, concurrent or planned treatement with acetylcholinesterase inhibitiros for dementia, presence or risk of adverse effects, drug interactions, drug-disease interaction, high drug burden index, poor adherence, or patient preference"
                                     })

acb_task = AgentNode(desc = f'Find out all the drugs the user is taking, from this list {meds_list}. The user may give their drugs under their commercial name, in which case you will have to match the medication with its pharmaceutical name from the list above.',
                        prerequisites = [{'medication': 'AC', 'reason':'Not urinary incontinence'},
                                         {'medication': 'AC', 'reason':'Urinary incontinence', 'effectiveness': 'Effective'}],
                        success = 'meds',
                        acceptable = {"[List of the medications the user is taking]": "The user lists all the anticholinergics he is taking. The medications listed match the provided list above. E.g answer: [Trospium, Alprazolam]"
                        })

deprescribe_task = AgentNode(desc = deprescribe,
                             prerequisites={'medication': 'AC', 'reason':'Urinary incontinence', 'effectiveness': 'Ineffective', 'meds': ''},
                             success=None,
                             acceptable=None,
                             preprocess = calc_acb)
continue_task = AgentNode(desc = cont,
                             prerequisites=[{'medication': 'AC', 'reason':'Urinary incontinence', 'effectiveness': 'Effective', 'meds': ''},
                                            {'medication': 'AC', 'reason':'Not urinary incontinence', 'meds': ''}],
                             success=None,
                             acceptable=None,
                             preprocess = calc_acb)

"""clinician_task = AgentNode(desc = "User's ACB score is too high. Refer them to clinician for an anticholinergic deprescribing assessment.",
                           prerequisites={'acb_evaluation': 'High'},
                           success= None,
                           acceptable = None)
pass_task = AgentNode(desc = "User's ACB score is low enough, they can continue taking their anticholinergics.",
                           prerequisites={'acb_evaluation': 'Low'},
                           success= None,
                           acceptable = None)"""


ac_tasks = [reason_task, effective_task, acb_task, deprescribe_task, continue_task]