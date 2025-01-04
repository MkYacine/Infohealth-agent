from agent import *

notes = """
PPI Availability
[Table contents:]
PPI | Standard dose (healing) (once daily)* | Low dose (maintenance) (once daily)
Omeprazole (Losec®) - Capsule | 20 mg+ | 10 mg+
Esomeprazole (Nexium®) - Tablet | 20ᵃ or 40ᵇ mg | 20 mg
Lansoprazole (Prevacid®) - Capsule | 30 mg+ | 15 mg+
Dexlansoprazole (Dexilant®) - Tablet | 30ᶜ or 60ᵈ mg | 30 mg
Pantoprazole (Tecta®, Pantoloc®) - Tablet | 40 mg | 20 mg
Rabeprazole (Pariet®) - Tablet | 20 mg | 10 mg
Legend:
a Non-erosive reflux disease
b Reflux esophagitis
c Symptomatic non-erosive gastroesophageal reflux disease
d Healing of erosive esophagitis

Can be sprinkled on food


Standard dose PPI taken BID only indicated in treatment of peptic ulcer caused by H. pylori; PPI should generally be stopped once eradication therapy is complete unless risk factors warrant continuing PPI (see guideline for details)

Key:
GERD = gastroesophageal reflux disease
NSAID = nonsteroidal anti-inflammatory drugs
H2RA = H2 receptor antagonist
SR = systematic review
GRADE = Grading of Recommendations Assessment, Development and Evaluation

PPI side effects:
When an ongoing indication is unclear, the risk of side effects may outweigh the chance of benefit
PPIs are associated with higher risk of fractures, C. difficile infections and diarrhea, community-acquired pneumonia, vitamin B12 deficiency and hypomagnesemia
Common side effects include headache, nausea, diarrhea and rash


On-demand definition:
Daily intake of a PPI for a period sufficient to achieve resolution of the individual's reflux-related symptoms; following symptom resolution, the medication is discontinued until the individual's symptoms recur, at which point, medication is again taken daily until the symptoms resolve
"""

cont = """
Help the user with PPI prescripiton. Advise the user following these instructions:
Based on this user's answers, continuing the treatement is advised.
Continue PPI or consult gastroenterologist if considering deprescribing.

Extra information notes, use when relevant:
""" + notes

deprescribe1 = """
Help the user with their PPI prescripiton. Advise the user following these instructions:
Based on this user's answers, discontinuing the treatement is advised.
Strong Recommendation (from Systematic Review and GRADE approach)
Decrease to lower dose (evidence suggests no increased risk in return of symptoms compared to continuing higher dose), or
Stop and use on-demand (daily until symptoms stop) (1/10 patients may have return of symptoms).

Monitor at 4 and 12 weeks
If verbal: Heartburn, Dyspepsia, Regurgitation, Epigastric pain
If non-verbal: Loss of appetite, Weight loss, Agitation

Use non-drug approaches
Avoid meals 2-3 hours before bedtime; elevate head of bed; address if need for weight loss and avoid dietary triggers
Manage occasional symptoms
Over-the-counter antacid, H2RA, PPI, alginate prn (ie. Tums®, Rolaids®, Zantac®, Olex®, Gaviscon®)
H2RA daily (weak recommendation – GRADE; 1/5 patients may have symptoms return)

If symptoms relapse: If symptoms persist x 3 – 7 days and interfere with normal activity:
Test and treat for H. pylori
Consider return to previous dose


Extra information notes, use when relevant:
Engaging patients and caregivers:
Patients and/or caregivers may be more likely to engage if they understand the rationale for deprescribing (risks of continued PPI use; long-term therapy may not be necessary), and the deprescribing process

Tapering doses:
No evidence that one tapering approach is better than another
Lowering the PPI dose (for example, from twice daily to once daily, or halving the dose, or taking every second day) OR stopping the PPI and using it on-demand are equally recommended strong options
Choose what is most convenient and acceptable to the patient

""" + notes

deprescribe2 = """
Help the user with their PPI prescripiton. Advise the user following these instructions:
Based on this user's answers, discontinuing the treatement is advised.
Stop PPI.

Monitor at 4 and 12 weeks
If verbal: Heartburn, Dyspepsia, Regurgitation, Epigastric pain
If non-verbal: Loss of appetite, Weight loss, Agitation

Use non-drug approaches
Avoid meals 2-3 hours before bedtime; elevate head of bed; address if need for weight loss and avoid dietary triggers
Manage occasional symptoms
Over-the-counter antacid, H2RA, PPI, alginate prn (ie. Tums®, Rolaids®, Zantac®, Olex®, Gaviscon®)
H2RA daily (weak recommendation – GRADE; 1/5 patients may have symptoms return)

If symptoms relapse: If symptoms persist x 3 – 7 days and interfere with normal activity:
Test and treat for H. pylori
Consider return to previous dose


Extra information notes, use when relevant:
Engaging patients and caregivers:
Patients and/or caregivers may be more likely to engage if they understand the rationale for deprescribing (risks of continued PPI use; long-term therapy may not be necessary), and the deprescribing process

Tapering doses:
No evidence that one tapering approach is better than another
Lowering the PPI dose (for example, from twice daily to once daily, or halving the dose, or taking every second day) OR stopping the PPI and using it on-demand are equally recommended strong options
Choose what is most convenient and acceptable to the patient

""" + notes



reason_task = AgentNode(desc = 'Find out the reason for taking the medication. If unsure, find out if history of endoscopy, if ever hospitalized for bleeding ulcer or if taking because of chronic NSAID use in past, if ever had heartburn or dyspepsia',
                        prerequisites = {'medication': 'PPI'},
                        success = 'reason',
                        acceptable = {"Conditions A": "Barretts esophagus, Chronic NSAID users with bleeding risk, Severe esophagitis, Documented history of bleeding GI ulcer",
                                      "Conditions B": "Peptic Ulcer Disease treated x 2-12 weeks (from NSAID; H. pylori), Upper Gl symptoms without endoscopy; asymptomatic for 3 consecutive days, ICU stress ulcer prophylaxis treated beyond ICU admission, Uncomplicated H. pylori treated x 2 weeks and asymptomatic",
                                      "Conditions C": "Mild to moderate esophagitis, or GERD treated x 4-8 weeks (esophagitis healed, symptoms controlled)",
                                      "Unknown": "The user explicity states they do not know why."
                                     })

deprescribing1_task = AgentNode(desc = deprescribe1,
                              prerequisites= [
                                  {'medication': 'PPI', 'reason':'Conditions C'},
                                  {'medication': 'PPI', 'reason':'Unknown'}
                                   ],
                              success = None,
                              acceptable = None)
deprescribing2_task = AgentNode(desc = deprescribe2,
                              prerequisites= {'medication': 'PPI', 'reason':'Conditions B'},
                              success = None,
                              acceptable = None)

continue_task = AgentNode( desc = cont,
                          prerequisites = {'medication': 'PPI', 'reason':'Conditions A'},
                          success = None,
                          acceptable = None)

ppi_tasks = [reason_task, deprescribing1_task, deprescribing2_task, continue_task]