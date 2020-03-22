## Index
[Project Brief](#brief)
   * [My Product Solution](#mysolution)
   
[ERD and Risk Assessment](#erdrisk)
   * [Initial ERD](#erd)
   * [Risk Assessment](#riskassess)
   * [Risk Assessment Table](#risktable)
   

[Planning and Risk Assessment](#Planning)
   * [User Stories](#userstories)
   * [Trello Board Sprint 1](#spr1)
   * [Trello Board Sprint 1](#spr1)
   * [Trello Board Sprint 2](#spr2)
   * [Trello Board Sprint 3](#spr3)
   * [Trello Board Completion Stage](#sprF)
	
[Testing Methadology](#testingmethod)
   * [Generated Report](#testingreport)
     
[My Deployment Method](#deploymentmethod)
   * [What I used](#techused)

[Visual Representation of my Solution](#visrep)

[Retrospective](#improve)

[Authors](#authorsinv)

[Acknowledgements](#acknowledgements)

<a name="brief"></a>
## The Project Brief

The goal of this First SFIA Project was to produce a solution that:
* Made use of the various methodologies, tools and techniques that were covered in all the modules done during training so far.
* Demonstrated full CRUD (Create, Read, Update, Delete) functionality
* Interacts and manipulates with a minimum of two tables in an SQL Database


<a name="mysolution"></a>
### Solution

The idea that I proposed, to meet the 3 main goals stated in the brief, was to create a simple website that would mimic that of a Holiday Booking website. 
The Website would present a couple of options to pick from, and ask the user fill in a number of fields and select choices for these options using a dropdown list to create a daytrip booking, e.g. First Name, Last Name, Restaurant to eat at, First Destination to visit etc. 
The User would be able to manage their booking to update their saved Daytrip details as well as be able to cancel(delete) their entire trip altogether, using a Unique Trip id number that is assigned to their booking.
The front-end functionality of this application would use Flask, HTML and Bootstrap, whereas the back-end functionality would use a combination of Python, MySQL, GCP (Google Cloud Platform), Jenkins(for Continuous Integration) and Github (as a Version Control Service)


<a name="erdrisk"></a>
## ERD and Risk Assessment

<a name="erd"></a>
### Initial Entity Relationship Diagram
![Initial ERD](/images/ERD.PNG)

Shown above is the ERD diagram for the inital database structure of the application. There are a total of 4 tables in which one is a joining table. 

* The tables Restaurants and Destinations were created to store information of specific locations, so that data can only be read from them to display the associated information about each object to the user for their choices.

* The Daytrip Table would be the main table that would store the Users' booking information as well as the ID of the Restaurant that they have selected to visit. 

* The tables Restaurants and Daytrip are linked by a One to Many relationship since the user can select only one restaurant to visit, however there can be multiple daytrips with the same restaurant chosen.

* In my application, a user is able to select 2 destinations to visit, so to account for this many to many relationship between 1 Trip ID from the Daytrip Table, and the many destinations a user can visit from the Destinations table, a bridging table was created (called DesJoin) between the two tables which would store the relavent Trip Id and Destination ID combinations, which reduces the overall complexity of implementing this application.

* I felt that my application was already simplified enough with the number of tables I had planned to implement it with, and so, no changes were made from the Initial ERD diagram to the Final ERD diagram

<a name="Risk"></a>
## Risk Assessment Table
![Risk Assessment Table](/images/risktable1.jpg)
![Risk Assessment Table Part 2](/images/risktable2.jpg)

<a name="Planning"></a>
## Planning 
# Trello Board

I created a Trello board to plan out my project as it had an easy and intuitive way of creating and managing cards that myself as a developer can assign anything to. I utilised MosCoW Prioritisation to give each requirement of the project an importance, so that I can use this to sort the order I should prioritise completing them in. I used a colour labelling method to do this and you can see an example of this below for my Project Backlog:

![ProjectBacklog](/images/projectbacklog.PNG) ![Labels](/images/MoSCoWLabels.jpg)

<a name="userstories"></a>
## User Stories (Users and Developers)

Using Trello I created a list for all the use-cases of the application from the perspective of a developer and a user as shown below:

![UserStories](/images/Userstories.PNG)

<a name="spr1"></a>
## Trello Board - Sprint 1)

I decided to split my project into 4 sprints. After determining the main requirements of my project, my First Sprint looked like this:

![Sprint 1 Image](/images/sprint1.PNG)

<a name="spr2"></a>
## Trello Board (Sprint 2)

After completing the tasks set out during my first sprint, I moved them them to the things done list. I then moved over cards from my sprint backlog, depending on their importance, to the second sprint, as shown below:

![Sprint 2 Image](/images/sprint2.PNG)

<a name="spr3"></a>
## Final Stages (Sprint 2....)

By the start of this third Sprint, most of the project requirements have been met, so final touches as well as some data entry testing were being introduced in this sprint to ensure the website worked seamlessly with the back-end database hosted on GCP as shown on the board below:

![Sprint 3 Image](/images/sprint3.PNG)

<a name="sprF"></a>
## Final Sprint

My project at this point has now been complete, with all the original requirements having been met. Some of the optional feature have been added, however there were some parts of the project from the third sprint that have been scrapped due to time constraints such as the Google Maps API, and a page that lists all destinations and restaurants. These dropped features could be reconsidered for a future update of the application.

![Completion..](/images/finalsprint.PNG)