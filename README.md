## Index
[Project Brief](#brief)
   * [My Product Solution](#mysolution)
   
[ERD and Diagrams](#erdanddiagrams)
   * [Initial ERD](#erd)
   * [Risk Assessment](#riskassess)
   * [Risk Assessment Table](#risktable)
   * [User Stories](#userstories)

[Sprints & Planning](#spr1)
   * [Trello Board Sprint 1.0](#spr1)
   * [Trello Board Sprint 2.0](#spr2)
   * [Trello Board Sprint 2.1 Continued...](#sprF)
   * [Trello Board Completion Stage](#sprFF)
	
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


<a name="erdanddiagrams"></a>
## ERD and Diagrams

<a name="erd"></a>
### Initial Entity Relationship Diagrams
![Initial ERD](/images/ERD.png)

Shown above is the ERD diagram for the inital database structure of the application. There are a total of 4 tables in which one is a joining table. 

* The tables Restaurants and Destinations were created to store information of specific locations, so that data can only be read from them to display the associated information about each object to the user for their choices.

* The Daytrip Table would be the main table that would store the Users' booking information as well as the ID of the Restaurant that they have selected to visit. 

* The tables Restaurants and Daytrip are linked by a One to Many relationship since the user can select only one restaurant to visit, however there can be multiple daytrips with the same restaurant chosen.

* In my application, a user is able to select 2 destinations to visit, so to account for this many to many relationship between 1 Trip ID from the Daytrip Table, and the many destinations a user can visit from the Destinations table, a bridging table was created between the two which would store the relavent Trip Id and Destination ID combinations which reduces the overall complexity of implementing this application.

* I felt that my application was already simplified enough with the number of tables I had planned to implement it with, and so, no changes were made from the Initial ERD diagram to the Final ERD diagram
