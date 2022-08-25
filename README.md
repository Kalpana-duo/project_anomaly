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

* for all programs:

                Count	     Percentage
 -------------------------------------------------------               
javascript-i	 118723	      0.13
html-css	      84935	      0.09
mysql	      82848	      0.09
jquery	      60869	      0.07
spring	      58603	      0.07
java-iii     	 56733	      0.06


* FS_JAVA_program

Most Frequent Class/Module Visited:
-----------
                 Count	Percentage
javascript-i	  94676	0.18
html-css	       66968	0.13
mysql	       65629	0.12
jquery	       48477	0.09
java-iii	       43094	0.08
java-ii	       41966	0.08
 
* Data Science Program

Most Frequent Class/Module Visited:
-----------
                    Count	Percentage
ds-fundamentals	15171	0.18
ds-sql	          12116	0.14
ds-classification	10524	0.12
ds-python      	9610	     0.11
ds-regression	     6797	     0.08
ds-stats	          6133	     0.07

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

By Program:
 
* Codeup Program: FS_PHP_program
Most Frequent Class/Module Revisited:
-----------
content          0.22
javascript-i     0.13
html-css         0.09
spring           0.08
mysql            0.07
java-iii         0.07
java-ii          0.05
jquery           0.05
java-i           0.05
javascript-ii    0.05
 
Most Frequent Topics Explored:
-----------
fundamentals    0.06
laravel         0.05
introduction    0.05
html-css        0.04
css-i           0.03
javascript      0.03
css-ii          0.03
php_ii          0.03
git             0.03
bom-and-dom     0.02

* Codeup Program: FS_JAVA_program
Most Frequent Class/Module Revisited:
-----------
javascript-i     0.16
html-css         0.12
mysql            0.11
jquery           0.08
spring           0.08
java-iii         0.08
java-ii          0.08
java-i           0.06
javascript-ii    0.05
appendix         0.05
 
Most Frequent Topics Explored:
-----------
introduction         0.07
fundamentals         0.06
css-i                0.06
css-ii               0.04
search_index.json    0.03
arrays               0.03
bom-and-dom          0.03
ajax                 0.02
relationships        0.02
functions            0.02

* Codeup Program: DS_program
Most Frequent Class/Module Revisited:
-----------
fundamentals      0.09
classification    0.09
1-fundamentals    0.08
sql               0.08
3-sql             0.06
python            0.06
4-python          0.05
6-regression      0.05
appendix          0.04
5-stats           0.04

Most Frequent Topics Explored:
-----------
overview                     0.04
1-overview                   0.04
project                      0.03
AI-ML-DL-timeline.jpg        0.03
modern-data-scientist.jpg    0.03
cli                          0.03
search_index.json            0.02
1.1-intro-to-data-science    0.02
scale_features_or_not.svg    0.02
explore                      0.02


7. Which lessons are least accessed? (Mijail)

* Codeup Program: FS_PHP_program
Least Frequent Class/Module Revisited:
-----------
2.00.02_Navigating_Excel                
2.00.05_Charts_PivotTables_Sparklines   
2.02.00_Inferential_Stats               
Exercises                               
ajax-api-request.html  

* Codeup Program: FS_JAVA_program
Least Frequent Class/Module Revisited:
-----------
Correlation.md                 
Clustering_Explore             
5.04.04_LeastAngleRegression   
6.00_Intro                     
curie-python-assessment    

* Codeup Program: DS_program
Least Frequent Class/Module Revisited:
-----------
modern-data-scientist.jpg   
git                         
spring                      
login                       
individual-project     
