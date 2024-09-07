# GeneticAlgorithm-CS461
Implementation of a genetic algorithm in Python to find ideal schedules for a list of activities. Made for Intro to AI course at UMKC. schedule.txt shows an example elite schedule and its fitness score.

Uses Python Anaconda distribution and scipy library for specialized statistical functions. 

## Fitness function criteria
*	For each activity, fitness starts at 0.
*	Activity is scheduled at the same time in the same room as another of the activities: -0.5
*	Room size:
    * Activities is in a room too small for its expected enrollment: -0.5
    *	Activities is in a room with capacity > 3 times expected enrollment: -0.2
    *	Activities is in a room with capacity > 6 times expected enrollment: -0.4
    * Otherwise + 0.3
*	Activities is overseen by a preferred facilitator: + 0.5
*	Activities is overseen by another facilitator listed for that activity: +0.2
*	Activities is overseen by some other facilitator: -0.1
*	Facilitator load:
    *	Activity facilitator is scheduled for only 1 activity in this time slot: + 0.2
    *	Activity facilitator is scheduled for more than one activity at the same time: - 0.2
    *	Facilitator is scheduled to oversee more than 4 activities total: -0.5
 
*	Facilitator is scheduled to oversee 1 or 2 activities*: -0.4
    *	Exception: Dr. Tyler is committee chair and has other demands on his time. 
    \*No penalty if he’s only required to oversee < 2 activities.
*	If any facilitator scheduled for consecutive time slots: Same rules as for SLA 191 and SLA 101 in consecutive time slots—see below.

Activity-specific adjustments:
*	The 2 sections of SLA 101 are more than 4 hours apart: + 0.5
*	Both sections of SLA 101 are in the same time slot: -0.5
*	The 2 sections of SLA 191 are more than 4 hours apart: + 0.5
*	Both sections of SLA 191 are in the same time slot: -0.5
*	A section of SLA 191 and a section of SLA 101 are overseen in consecutive time slots (e.g., 10 AM & 11 AM): +0.5
    *	In this case only (consecutive time slots), one of the activities is in Roman or Beach, and the other isn’t: -0.4
*	It’s fine if neither is in one of those buildings, of activity; we just want to avoid having consecutive activities being widely separated. 	
*	A section of SLA 191 and a section of SLA 101 are taught separated by 1 hour (e.g., 10 AM & 12:00 Noon): + 0.25
*	A section of SLA 191 and a section of SLA 101 are taught in the same time slot: -0.25
