# Project - Anomaly Detection

By: Chenchen Feng and Mijail Mariano
23AUGUST2022

## Project Goal
* The goal is by analyzing Codeup curriculum access data, identify suspicious activities and ip address. Also get some insights from this data for future use.

## Project Description 
* In this report, we used Codeup curriculum access data with anomaly detection method to answer the questions list in the scenario email.

## Data Dictionary

“Logs” Table:
* Datetime (index): The date and time when the user accessed Codeup’s domain url
* Endpoint: The target or requested Codeup service url where information is accessed
* User_id: The unique Codeup student, alumni, or staff identification number
* Cohort_id: Unique cohort identifier 
* IP: A computer’s unique internet protocol identifier that is used to communicate over a network 
* name (cohort): The cohort name

“Cohorts” Table:
* Slack: Slack channel the user is a member of
* Start_date: Cohort/user Codeup program start date
* End_date: Cohort/user Codeup program end date
* Program_id: Identifier that links the user to the Codeup program they were enrolled in

## Steps to Reproduce

1. You will need an env.py file that contains the hostname, username and password of the mySQL database that contains the Zillow table. Store that env file locally in the repository.
2. Clone my repo (including the acquire_final.py and prepare_final.py) (confirm .gitignore is hiding your env.py file)
3. Libraries used are pandas, matplotlib, seaborn, numpy, os.
4. You should be able to run final_report.

## Scenario:

Email to analyst:


Hello,


I have some questions for you that I need answered before the board meeting Thursday afternoon. My questions are listed below; however, if you discover anything else important that I didn’t think to ask, please include that as well.

1. Which lesson appears to attract the most traffic consistently across cohorts (per program)?
2. Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?
3. Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students?
4. Is there any suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be? Does it appear that any web-scraping is happening? Are there any suspicious IP addresses?
5. At some point in 2019, the ability for students and alumni to access both curriculums (web dev to ds, ds to web dev) should have been shut off. Do you see any evidence of that happening? Did it happen before?
6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?
7. Which lessons are least accessed?
8. Anything else I should be aware of?

Thank you,

## Initial Questions We Picked and Answers

1. Which lesson appears to attract the most traffic consistently across cohorts (per program)?
(Mijail)

2. Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over? (Chenchen)
* For Data Sience program, Darden referred classification lesson a lot more than other cohorts. 
* For Full Stack JAVA program, Ceres referred html-css class tha most.

3. Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students? (Chenchen)
* The active student hardly access the curriculum is user 704 from Bash cohort, this is a remote student from Full Stack JAVA program. 
* Students might dropped the class before program end date: 
      *  user 268 from Xanadu (Full Stack JAVA, in-person),
      *  user 663 from Hyperion (Full Stack JAVA, remote),
      *  user 663 from Luna (Full Stack JAVA, remote),
      *  user 707 from Bash (Full Stack JAVA, remote),
      *  user 757 from Jupiter (Full Stack JAVA, remote).

4. Is there any suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be? Does it appear that any web-scraping is happening? Are there any suspicious IP addresses? (Chenchen)
* Suspicious users and ip:
    * User 313 with ip 173.173.121.126 : web-scarping 225 pages/day 4 years after leaving codeup. 
    * Ip 204.44.112.76 : consider as web-scraping machine.
    * User 111 with ip 67.11.134.242 : can not identify any information.
    * User 354 : need to be cleaned out from the system.

5. What topics are grads continuing to reference after graduation and into their jobs (for each program)? (Mijail)

7. Which lessons are least accessed? (Mijail)