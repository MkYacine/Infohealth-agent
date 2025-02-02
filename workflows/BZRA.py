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

deprescribing_task = AgentNode(desc = "Positive",
                              prerequisites= [
                                  {'medication': 'BZRA', 'reason':'Insomnia', 'comorbidities': 'Managed', 'age': 'Old'},
                                  {'medication': 'BZRA', 'reason':'Insomnia', 'comorbidities': 'Managed', 'age': 'Young', 'duration': 'Long'}
                                   ],
                              success = None,
                              acceptable = None)
continue_task = AgentNode( desc = "Negative",
                          prerequisites = [
                              {'medication': 'BZRA', 'reason':'Not insomnia'},
                              {'medication': 'BZRA', 'reason':'Insomnia', 'comorbidities': 'Unmanaged'},
                              {'medication': 'BZRA', 'reason':'Insomnia', 'comorbidities': 'Managed', 'age': 'Young', 'duration': 'Short'}
                          ],
                          success = None,
                          acceptable = None)
bzra_tasks = [reason_task, age_task, duration_task, comorbidities_task, deprescribing_task, continue_task]