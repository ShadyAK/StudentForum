# Student-Forum

A simple web application for an institution for doubt clearing and resource sharing.
[Link to web app](https://student-forum-g18.herokuapp.com/)

## Table of Contents
* [General Overview](#general-overview)
* [Requirement Analysis](#requirement-analysis)
* [Technologies](#technologies)
* [Setup](#setup)


## General Overview
While all classes and quizzes have moved from the classroom to the web, discussion and clarification of doubts, and sharing of resources has become very difficult. Doubt resolution and active discussion are a significant part of learning at any stage in life. Hence, we believe that there is an immediate requirement for a Student forum.

A student forum would be an online portal, where teachers of an institute can create rooms for the discussions related to their topics and subjects and students can the same either by enrollment or by using a unique room code. In every room, there will be 2 subsections - one for asking and resolving doubts (this may be done anonymously) and another for sharing course-related resources. Such a platform will encourage students to pose their doubts and actively engage in discussions, leading to a richer learning experience.

## Requirement Analysis
1. Student forum’s main focus is to create a place where everybody can express their concern and clear out their doubts with the help from their respective classmates.
2. Everyone will have a say in every topic i.e. if they like the doubt/question/query and they benefit from it then they can upvote the doubt/question/query.
3. Classmates can give their opinions/solutions/ideas on the given query and get upvotes if others find it helpful.
4. The  doubt/question/query will be posted anonymously in the given branch and semester in which the student is enrolled in and will be visible to the students in the same branch and semester.
5. As of current scene classes and assignments have been switched to online systems rather than classic offline systems and it’s a tough task to go through various class groups and chats to find the appropriate link to the classes and resources . To tackle this problem Student Forum will have specific tabs for class links and more features like events/hackathons details where students can post the specifics.


## Technologies
Project is created with:
* flask version: 1.1.2
* sqlite3
* bootstrap version: 5.0 
* heroku for deployment

## Setup
To run this project locally:

```
$ pip install -r requirements.txt
$ python runner.py
```
