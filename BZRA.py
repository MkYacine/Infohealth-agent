from agent import *

notes = """
BZRA Availability
[Table of medications and strengths:]
Alprazolam (Xanax®) T | 0.25 mg, 0.5 mg, 1 mg, 2 mg
Bromazepam (Lectopam®) T | 1.5 mg, 3 mg, 6 mg
Chlordiazepoxide C | 5 mg, 10 mg, 25 mg
Clonazepam (Rivotril®) T | 0.25 mg, 0.5 mg, 1 mg, 2 mg
Clorazepate (Tranxene®) C | 3.75 mg, 7.5 mg, 15 mg
Diazepam (Valium®) T | 2 mg, 5 mg, 10 mg
Flurazepam (Dalmane®) C | 15 mg, 30 mg
Lorazepam (Ativan®) T,S | 0.5 mg, 1 mg, 2 mg
Nitrazepam (Mogadon®) T | 5 mg, 10 mg
Oxazepam (Serax®) T | 10 mg, 15 mg, 30 mg
Temazepam (Restoril®) C | 15 mg, 30 mg
Triazolam (Halcion®) T | 0.125 mg, 0.25 mg
Zopiclone (Imovane®, Rhovane®) T | 5mg, 7.5mg
Zolpidem (Sublinox®) S | 5mg, 10mg
T = tablet, C = capsule, S = sublingual tablet

Using CBT: What is cognitive behavioural therapy (CBT)?
CBT includes 5-6 educational sessions about sleep/insomnia, stimulus control, sleep restriction, sleep hygiene, relaxation training and support
Does it work?
CBT has been shown in trials to improve sleep outcomes with sustained long-term benefits
Who can provide it?
Clinical psychologists usually deliver CBT, however, others can be trained or can provide aspects of CBT education; self-help programs are available
How can providers and patients find out about it?
Some resources can be found here: https://mysleepwell.ca/

Behavioural management: Primary care:
Go to bed only when sleepy
Do not use bed or bedroom for anything but sleep (or intimacy)
If not asleep within about 20-30 min at the beginning of the night or after an awakening, exit the bedroom
If not asleep within 20-30 min on returning to bed, repeat #3
Use alarm to awaken at the same time every morning
Do not nap
Avoid caffeine after noon
Avoid exercise, nicotine, alcohol, and big meals within 2 hrs of bedtime

Institutional care:
Pull up curtains during the day to obtain bright light exposure
Keep alarm noises to a minimum
Increase daytime activity & discourage daytime sleeping
Reduce number of naps (no more than 30 mins and no naps after 2 pm)
Offer warm decaf drink, warm milk at night
Restrict food, caffeine, smoking before bedtime
Have the resident toilet before going to bed
Encourage regular bedtime and rising times
Avoid waking at night to provide direct care
Offer backrub, gentle massage

BZRA Side Effects:
BZRAs have been associated with:
physical dependence, falls, memory disorder, dementia, functional impairment, daytime sedation and motor vehicle accidents
Risks increase in older persons

"""

cont = """
Help the user with continuining their BZRA prescripiton. Advise the user following these instructions:
Since the reason for taking BZRA for non-insomnia related reasons, continuing the treatement is advised.
You should engage patients by discussing potential risks of BZRA, benefits, withdrawal, symptoms, and duration.
Discuss the user's access to emergency care, psychiatric support and support systems.
Some steps the user can take to lessen the effects of the drug are:
- Minimize use of drugs that worsen insomnia (e.g caffeine, alcohol etc...)
- Treat underlying condition
- Consider consulting psychologist or psychiatrist or sleep specialist.

Extra information notes, use when relevant:
""" + notes

deprescribe = """
Help the user with discontinuining their BZRA prescripiton. Advise the user following these instructions:
Since the reason for taking BZRA is insomnia related, discontinuing the treatement is advised.
You should engage patients by discussing potential risks of BZRA, benefits, withdrawal, symptoms, and duration.
- Taper and then stop BZRA: Taper slowly, for example ~25% every two weeks, and if possible, 12.5 reductions near end and planned drug-free days.
For Old patients: strong recommendation from systematic review and GRADE approach
For Young patients:  strong recommendation from systematic review and GRADE approach
Offer Behvaioural sleeping advice; consider CBT if available; minize sleep-disrupting substances; alternativea approaches to manage insomnia.
- Monitor every 1-2 weeks for duration of tapering.
Expected benefits: improved alertness, cognition, daytime sedation, and reduces falls
Withdrawl symptoms: Insomnia, anxiety, irratibility, sweating, gastrointestinal symptoms (all usually mild and last for days for a few weeks)
- Use non-drug appraoches to managed insomnia, Use behavioral approaches and/or CBT
- If symptoms relapse, consider:
Maintining current BZRA dose for 1-2 weeks, then continue to taper at a slow rate.
Or opting for alternate drugs, other medications have been used to manage insomnia. Assessment of their safety and effectiveness is beyond the scope of your work.
Patient can see BZRA deprescribing guideline for details.


Extra information notes, use when relevant:
Tapering doses:
No published evidence exists to suggest switching to long-acting BZRAs reduces incidence of withdrawal symptoms or is more effective than tapering shorter-acting BZRAs
If dosage forms do not allow 25% reduction, consider 50% reduction initially using drug-free days during latter part of tapering, or switch to lorazepam or oxazepam for final taper steps
Engaging patients and caregivers: Patients should understand:
The rationale for deprescribing (associated risks of continued BZRA use, reduced long-term efficacy)
Withdrawal symptoms (insomnia, anxiety) may occur but are usually mild, transient and short-term (days to a few weeks)
They are part of the tapering plan, and can control tapering rate and duration

""" + notes



reason_task = AgentNode(desc = 'Find out the reason for taking BZRA',
                        prerequisites = {'medication': 'BZRA'},
                        success = 'reason',
                        acceptable = {"Insomnia": "Taken BZRA mainly for insomnia ", 
                                      "Not insomnia": "Other sleeping disorders, unmanaged anxiety, depression, physical or mental condition that may be causign or aggravating insomnia, Benzodiazepine effective specifically for anxiety, alcohol withdrawal"
                                     })

comorbidities_task = AgentNode(desc = 'Find out if the user has any underlying mental comorbidities (anxiety, depression, etc...) , AND determine if they are managed or unmanaged',
                              prerequisites= {'medication': 'BZRA', 'reason':'Insomnia'},
                              success = 'comorbidities',
                               acceptable = {"Managed": "The user has no comorbidities, OR has them fully managed",
                                             "Unmanaged": "The user has comorbidities that are not fully managed"})

age_task = AgentNode(desc = 'Find out how old the user is',
                     prerequisites = {'medication': 'BZRA', 'reason':'Insomnia', 'comorbidities': 'Managed'},
                     success = 'age',
                     acceptable = {"Old": "The user is 65 years old or older", 
                                   "Young": "The user is younger than 65 years old"})
duration_task = AgentNode(desc = 'Find out how long the user has been taking BZRA',
                     prerequisites = {'medication': 'BZRA', 'reason':'Insomnia', 'comorbidities': 'Managed', 'age':'Young'},
                     success = 'duration',
                     acceptable = {"Short": "The user has been taking the medication for less than 4 weeks", 
                                   "Long": "The user has been taking the medication for 4 weeks or more"})

deprescribing_task = AgentNode(desc = deprescribe,
                              prerequisites= [
                                  {'medication': 'BZRA', 'reason':'Insomnia', 'comorbidities': 'Managed', 'age': 'Old'},
                                  {'medication': 'BZRA', 'reason':'Insomnia', 'comorbidities': 'Managed', 'age': 'Young', 'duration': 'Long'}
                                   ],
                              success = None,
                              acceptable = None)
continue_task = AgentNode( desc = cont,
                          prerequisites = [
                              {'medication': 'BZRA', 'reason':'Not insomnia'},
                              {'medication': 'BZRA', 'reason':'Insomnia', 'comorbidities': 'Unmanaged'},
                              {'medication': 'BZRA', 'reason':'Insomnia', 'comorbidities': 'Managed', 'age': 'Young', 'duration': 'Short'}
                          ],
                          success = None,
                          acceptable = None)
bzra_tasks = [reason_task, age_task, duration_task, comorbidities_task, deprescribing_task, continue_task]