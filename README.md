## **Anomaly Detection Project: Curriculum Logs**

**Created By:**

Chenchen Feng

[github.com/Chenchen070](https://github.com/Chenchen070)

Mijail Mariano

[github.com/mijailmariano](https://github.com/mijailmariano)

----

### **Project Goal**

* The goal of this analysis was to study trends of online curriculum visits and potential suspicious activity. For this study, we use anomaly detection techniques on a Codeup LLC curriculum log and IP address dataset of ~1mil records. Post analysis, we provide insights for Codeup's strategic lesson planning and make recommendations to mitigate suspicious online behavior.

#### **Project Description**

* We use a scenario-based approach to help inform senior Codeup stakeholders on their online curriculum & platforms strategy. The final report is structured in a question-and-answer format to raise insights on the focal questions asked from the scenario.

----

### **Data Dictionary**

Logs Table:
* Datetime (index): The date and time when the User accessed Codeup’s domain url
* Endpoint: The target or requested Codeup service url where information is accessed
* User_id: The unique Codeup student, alumni, or staff identification number
* Cohort_id: Unique cohort identifier 
* IP: A computer’s unique internet protocol identifier that is used to communicate over a network 
* name (cohort): The cohort name

Cohorts Table:
* Slack: Slack channel the User is a member of
* Start_date: Cohort/User Codeup program start date
* End_date: Cohort/User Codeup program end date
* Program_id: Identifier that links the User to the Codeup program they were enrolled in

----

### **Steps to Reproduce**

1. You will need an env.py file that contains the hostname, Username, and password of Codeup LLC MySQL database which contains the logs & cohort tables. Store that env file locally in the repository.
2. Clone this repo (including the acquire_final.py and prepare_final.py) (confirm .gitignore is hiding your env.py file)
3. Primary libraries include pandas, matplotlib, seaborn, numpy, os.
4. You should be able to run final_report with this environment.

----

### **Scenario:**

--

Email to analyst:

Hello,

I have some questions for you that I need answered before the board meeting Thursday afternoon. My questions are listed below; however, if you discover anything else important that I didn’t think to ask, please include that as well.

1. Which lesson appears to attract the most traffic consistently across cohorts (per program)?
2. Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?
3. Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students?
4. Is there any suspicious activity, such as Users/machines/etc. accessing the curriculum who shouldn’t be? Does it appear that any web-scraping is happening? Are there any suspicious IP addresses?
5. At some point in 2019, the ability for students and alumni to access both curriculums (web dev to ds, ds to web dev) should have been shut off. Do you see any evidence of that happening? Did it happen before?
6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?
7. Which lessons are least accessed?
8. Anything else I should be aware of?

--

----

### **Questions Explored and Answered**

1. Which lesson appears to attract the most traffic consistently across cohorts (per program)?
(Mijail)

``While Attending Codeup:``
* For all programs --  Most Frequent Class/Module Visited: 
  1. javascript-i
  2. html-css
  3. mysql
  4. jquery
  5. spring
  6. java-iii

* FS_JAVA_program -- Most Frequent Class/Module Visited:
  1. javascript-i
  2. html-css
  3. mysql
  4. jquery
  5. java-iii
  6. java-ii

* Data Science Program -- Most Frequent Class/Module Visited:
  1. ds-fundamentals
  2. ds-sql
  3. ds-classification
  4. ds-python
  5. ds-regression
  6. ds-stats

2. Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over? (Chenchen)

* For Data Science program, Darden referred classification lesson a lot more than other cohorts. 
* For Full Stack JAVA program, Ceres referred html-css class the most.

3. Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students? (Chenchen)

* The active student hardly accesses the curriculum is User 704 from Bash cohort, this is a remote student from Full Stack JAVA program. 
* Students may drop the class before program end date: 

      *  User 268 from Xanadu (Full Stack JAVA, in-person)
      
      *  User 663 from Hyperion (Full Stack JAVA, remote)
      
      *  User 663 from Luna (Full Stack JAVA, remote)
      
      *  User 707 from Bash (Full Stack JAVA, remote)
      
      *  User 757 from Jupiter (Full Stack JAVA, remote)

4. Is there any suspicious activity, such as Users/machines/etc. accessing the curriculum who shouldn’t be? Does it appear that any web-scraping is happening? Are there any suspicious IP addresses? (Chenchen)

* ``Suspicious Users and ip:``

    * User 313 with ip 173.173.121.126: web-scarping 225 pages/day 4 years after leaving Codeup. 
    
    * Ip 204.44.112.76: consider as web-scraping machine.
    
    * User 111 with ip 67.11.134.242: cannot identify any information.
    
    * User 354: need to be cleaned out from the system.

5. What topics are grads continuing to reference after graduation and into their jobs (for each program)? (Mijail)

``By Program:``
 
* Codeup Program: FS_PHP_program
Most Frequent Class/Module Revisited:
  1. content
  2. javascript-i
  3. html-css
  4. spring  
  5. mysql       
  6. java-iii    
  7. java-ii      
  8. jquery     
  9. java-i    
  10. javascript-ii 
 
Most Frequent Topics Revisited:

  1. fundamentals 
  2. laravel  
  3. introduction 
  4. html-css
  5. css-i        
  6. javascript 
  7. css-ii
  8. php_ii    
  9. git         
  10. bom-and-dom 

* Codeup Program: FS_JAVA_program
Most Frequent Class/Module Revisited:

  1. javascript-i 
  2. html-css       
  3. mysql           
  4. jquery       
  5. spring        
  6. java-iii        
  7. java-ii          
  8. java-i         
  9. javascript-ii   
  10. appendix        
 
Most Frequent Topics Revisited:

  1. introduction     
  2. fundamentals 
  3. css-i           
  4. css-ii           
  5. search_index.json   
  6. arrays          
  7. bom-and-dom   
  8. ajax          
  9. relationships   
  10. functions     

* Codeup Program: DS_program
Most Frequent Class/Module Revisited:

  1. sql    
  2. fundamentals
  3. classification 
  4. python        
  5. regression         
  6. anomaly-detection
  7. stats
  8. appendix     
  9. timeseries
  10. search

Most Frequent Topics Revisited:

  1. overview              
  2. search_index.json           
  3. AI-ML-DL-timeline.jpg                 
  4. modern-data-scientist.jpg     
  5. mysql-overview   
  6. 1-overview                        
  7. anomaly detection cartoon.jpeg         
  8. explore   
  9. acquire  
  10. intro to data science                     

7. Which lessons are least accessed? (Mijail)

* Codeup Program: FS_JAVA_program

Least Frequent Class/Module Visited:
  1. 3.2-databases                 
  2. 3.4-basic-statements             
  3. 3.6-functions   
  4. 3.9-temporary-tables                     
  5. css   
 
Least Frequent Topic Visited:
  1. twitter.html
  2. 9.3-joins
  3. 120
  4. appendix
  5. PreWork

* Codeup Program: DS_program

Least Frequent Class/Module Visited:
  1. End_to_End_clustering
  2. end_to_end_clustering                           
  3. 4.2-compare-means                        
  4. DataToAction_v2.jpg                        
  5. statistics-assessment       

Least Frequent Topic Visited:
  1. 6.1-parametric-modeling
  2. getUserDetails
  3. 4-navigating-the-filesystem 
  4. cls
  5. explore-old


