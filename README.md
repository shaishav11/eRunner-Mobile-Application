# eRunner-Mobile-Application

The primary objective of this study was to design and implement a relational database that is industry ready for a mobile application. Due to the recent pandemic, the world has come to a stop and slowly reopening. Many sports related events have been either postponed or cancelled due to social distancing. Since people are staying home, this is affecting their fitness and this led us to the idea to build a real time platform for runners to compete with one or more players located anywhere in the world! The goal was to create, alter tables and maintain data of multiple entities to support different functionalities of the mobile application in the live environment. Also, manage insertion, update, and delete of the data for storage and efficient retrieval of the data of the mobile application. Additionally, integrate GPS coordinates and user profile pictures with User Interface to track time, speed and distance and finally develop an interactive and user friendly user interface for easy utilization of mobile applications. 

Before diving into the requirements, let us talk about the functionality of the application. The application provides three important features to the users. 
<br>Quick Race: The user can go for a quick 1 on 1 race with an opponent who wishes to run the same distance and the same time from anywhere across the globe
<br>Marathon: The user can register for all the upcoming marathons happening anywhere in the world and participate in it without actually having to
<br>Training Run: The user can set a distance and schedule a time to run for fun and maintain their fitness

The database was modelled taking requirements of data fields required for building an application which can hold user information and their attributes, login information, user selections, and storing all the results to create a dashboard for user’s achievements. The EER and UML diagrams were modelled, followed by the mapping of the conceptual model to a relational model with the required primary and foreign keys. This database was then implemented fully in MySQL. MongoDB was used to track GPS coordinates, store match results and user’s profile pictures.

The goal of the study is to build a database model which can handle data of the live platform which facilitates racing, marathon and training. Database can efficiently store information of each user, logs of their matches, list of marathons and users’ enrollment in the marathon. Apart from it it should be accurate because the result of the match will be decided from data stored in the database and also it will help to identify players’ performance parameters like percentage win, total distance, stamina, level and other parameters. These parameters are useful for players to track their performance anso useful to identify opponents in the quick match.

There are multiple requirements to build an efficient database who can support live and complete mobile applications. 

Requirements are following:

1. Data Modeling
Enhanced Entity Relation
Unified Modeling Language
Relational Model 

2. SQL to establish relation between data
MySQL Workbench
Various real world situations using query to retrieve

3. NoSQL for fast insert and retrieval of match data
MongoDB
Creation of collections in database on AWS
Maintain LIVE data of matches and users’ Avatar

4. Integration
Python
Database integration and Web App development using Flask - Python

