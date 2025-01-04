from agent import *

notes = """
Commonly Prescribed Antipsychotics
[Table contents:]
Antipsychotic | Form | Strength
Chlorpromazine | T, IM, IV | 25, 50, 100 mg; 125 mg/mL
Haloperidol (Haldol®) | T, L, IR, IM, IV, LA IM | 0.5, 1, 2, 5, 10, 20 mg; 2 mg/mL; 5 mg/mL; 50, 100 mg/mL
Loxapine (Xylac®, Loxapac®) | T, L, IM | 2.5, 5, 10, 25, 50 mg; 25 mg/L; 25, 50 mg/mL
Aripiprazole (Abilify®) | T, IM | 2, 5, 10, 15, 20, 30 mg; 300, 400 mg
Clozapine (Clozaril®) | T | 25, 100 mg
Olanzapine (Zyprexa®) | T, D, IM | 2.5, 5, 7.5, 10, 15, 20 mg; 5, 10, 15, 20 mg; 10mg per vial
Paliperidone (Invega®) | ER T, PR IM | 3, 6, 9 mg; 50mg/0.5mL, 75mg/0.75mL, 100mg/1mL, 150mg/1.5mL
Quetiapine (Seroquel®) | IR T, ER T | 25, 100, 200, 300 mg; 50, 150, 200, 300, 400 mg
Risperidone (Risperdal®) | T, S, D, PR IM | 0.25, 0.5, 1, 2, 3, 4 mg; 1 mg/mL; 0.5, 1, 2, 3, 4 mg; 12.5, 25, 37.5, 50 mg
IM = intramuscular, IV = intravenous, L = liquid, S = suppository, SL = sublingual, T = tablet, D = disintegrating tablet, ER = extended release, IR = immediate release, LA = long-acting, PR = prolonged release

Sleep management:
Primary care:
Go to bed only when sleepy
Do not use your bed or bedroom for anything but sleep (or intimacy)
If you do not fall asleep within about 20-30 min at the beginning of the night or after an awakening, exit the bedroom
If you do not fall asleep within 20-30 min on returning to bed, repeat #3
Use your alarm to awaken at the same time every morning
Do not nap
Avoid caffeine after noon
Avoid exercise, nicotine, alcohol, and big meals within 2 hrs of bedtime

Institutional care:
Pull up curtains during the day to obtain bright light exposure
Keep alarm noises to a minimum
Increase daytime activity and discourage daytime sleeping
Reduce number of naps (no more than 30 mins and no naps after 2pm)
Offer warm decaf drink, warm milk at night
Restrict food, caffeine, smoking before bedtime
Have the resident toilet before going to bed
Encourage regular bedtime and rising times
Avoid waking at night to provide direct care
Offer backrub, gentle massage

BPSD management:
Consider interventions such as: relaxation, social contact, sensory (music or aroma-therapy), structured activities and behavioural therapy
Address physical and other disease factors: e.g. pain, infection, constipation, depression
Consider environment: e.g. light, noise
Review medications that might be worsening symptoms

Antipsychotic side effects:
APs associated with increased risk of:
Metabolic disturbances, weight gain, dry mouth, dizziness
Somnolence, drowsiness, injury or falls, hip fractures, EPS, abnormal gait, urinary tract infections, cardiovascular adverse events, death
Risk factors: higher dose, older age, Parkinsons', Lewy Body Dementia
"""

cont = """
Help the user with discontinuining their AP prescripiton. Advise the user following these instructions:
Since the user is taking AP for untreated mental disorder, continuing the treatement is advised.
Continue AP or consult psychiatrist if considering deprescribing

Extra information notes, use when relevant:
""" + notes

deprescribe1 = """
Help the user with discontinuining their AP prescripiton. Advise the user following these instructions:
Since the user is taking AP for insomnia, discontinuing the treatement is advised.
Stop AP, Good practice recommendation.
If insomnia relapses:
Consider: Minimize use of substances that worsen insomnia (e.g. caffeine, alcohol), or Non-drug behavioural approaches.
Alternate drugs
Other medications have been used to manage insomnia. Assessment of their safety and effectiveness is beyond the scope of this deprescribing algorithm. See notes for details.

Extra information notes, use when relevant:
Engaging patients and caregivers:
Patients and caregivers should understand:
The rationale for deprescribing (risk of side effects of continued AP use)
Withdrawal symptoms, including BPSD symptom relapse, may occur
They are part of the tapering plan, and can control tapering rate and duration

Tapering doses:
No evidence that one tapering approach is better than another
Consider:
Reduce to 75%, 50%, 25% of original dose on a weekly or bi-weekly basis and then stop; or
Consider slower tapering and frequent monitoring in those with severe baseline BPSD
Tapering may not be needed if low dose for insomnia only
""" + notes

deprescribe2 = """
Help the user with discontinuining their AP prescripiton. Advise the user following these instructions:
Since the user is taking AP for a controlled mental disorder, discontinuing the treatement is advised.
Strong Recommendation (from Systematic Review and GRADE approach)
Taper and stop AP (slowly in collaboration with patient and/or caregiver; e.g. 25%-50% dose reduction every 1-2 weeks)
Monitor every 1-2 weeks for duration of tapering
Expected benefits:
May improve alertness, gait, reduce falls, or extrapyramidal symptoms
Adverse drug withdrawal events (closer monitoring for those with more severe baseline symptoms):
Psychosis, aggression, agitation, delusions, hallucinations

If BPSD relapses:
Consider:
Non-drug approaches (e.g. music therapy, behavioural management strategies)
Restart AP drug:
Restart AP at lowest dose possible if resurgence of BPSD with re-trial of deprescribing in 3 months
At least 2 attempts to stop should be made
Alternate drugs:
Consider change to risperidone, olanzapine, or aripiprazole

Extra information notes, use when relevant:
Engaging patients and caregivers:
Patients and caregivers should understand:
The rationale for deprescribing (risk of side effects of continued AP use)
Withdrawal symptoms, including BPSD symptom relapse, may occur
They are part of the tapering plan, and can control tapering rate and duration

Tapering doses:
No evidence that one tapering approach is better than another
Consider:
Reduce to 75%, 50%, 25% of original dose on a weekly or bi-weekly basis and then stop; or
Consider slower tapering and frequent monitoring in those with severe baseline BPSD
Tapering may not be needed if low dose for insomnia only
""" + notes

reason_task = AgentNode(desc = 'Find out the reason for taking AP',
                        prerequisites = {'medication': 'AP'},
                        success = 'reason',
                        acceptable = {"Insomnia": " Primary insomnia treated for any duration or secondary insomnia where underlying comorbidities are managed",
                                      "Treated mental disorder":" Psychosis, aggression, agitation (behavioural and psychological symptoms of dementia - BPSD) treated ≥ 3 months (symptoms controlled, or no response to therapy).",
                                      "Untreated mental disorder": "Schizophrenia, Schizo-affective disorder, Bipolar disorder, Acute delirium, Tourette’s syndrome, Tic disorders, Autism, Less than 3 months duration of psychosis in dementia, Intellectual disability, Developmental delay, Obsessive-compulsive disorder, Alcoholism, Cocaine abuse, Parkinson’s disease psychosis, Adjunct for treatment of Major Depressive Disorder"
                                     })


deprescribing1_task = AgentNode(desc = deprescribe1,
                              prerequisites={'medication': 'AP', 'reason':'Insomnia'},
                              success = None,
                              acceptable = None)

deprescribing2_task = AgentNode(desc = deprescribe2,
                              prerequisites={'medication': 'AP', 'reason':'Treated mental disorder'},
                              success = None,
                              acceptable = None)
continue_task = AgentNode( desc = cont,
                          prerequisites = {'medication': 'AP', 'reason':'Untreated mental disorder'},
                          success = None,
                          acceptable = None)

ap_tasks = [reason_task, deprescribing1_task, deprescribing2_task, continue_task]