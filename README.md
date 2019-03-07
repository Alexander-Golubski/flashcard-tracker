# Teach_SR Outline

### Overview

[Spaced repetition](https://en.wikipedia.org/wiki/Spaced_repetition) is a technique for placing information in a learner’s long-term memory. It accomplishes this through spacing out reviews of the material. [There is a wealth of empirical data on the efficacy of spaced repetition.](https://www.gwern.net/Spaced-repetition#literature-review) There currently exist several spaced repetition software programs that help users implement this technique, including Anki, Mnemosyne, and SuperMemo. These programs allow users to create digital flashcards, and then prompt the user to review a given flashcard at a certain time based on an algorithm that considers if the user reported recalling the correct information, and, if so, how difficult it was (typically on a scale of 1 to 5).

I personally found the spaced repetition software program Anki to be extremely useful in learning mandarin vocabulary. Programs like Anki are commonly used by other language learners and medical students, and have been for decades. However, in all of my years of language classes, I never had a teacher who used spaced repetition software in the classroom. I believe this is because existing programs do not have any way for teachers to see if students are actually completing their flashcard reviews.

To meet this need, Teach_SR will allow teachers to assign digital flashcards to their students. The web app will use a spaced repetition algorithm to determine when students will be asked to review a given card. Teachers will be able to see if students are keeping up with their reviews.


### Features

1. User Accounts: Students and teachers will be able to create accounts and log in to the app. Students can be invited to cohorts (groupings of students) by teachers.

2. Create Cards: Digital flashcards can be created by teachers, and assigned to cohorts.

3. Review Cards: While logged in, students can review cards that are due for that day. They will rate, on a scale of 1 to 5, how difficult it was to recall the information as they review the cards.

4. Spaced Repetition: Students will be prompted to review cards at a time determined by the spaced repetition algorithm.

5. Teacher Oversight: Teachers will be able to view any given student's progress on their reviews, provided the student is in a cohort that the teacher created. This could be used for grading purposes, or to help students who need it.

### Technologies

* Python
* Flask
* MySQL
* SQLAlchemy
* Flask-login
* WTForms
* Jinja2 templates
* Pivotal Tracker

### What I'll Have to Learn

I'll need to determine which spaced repetition algorithm to use. Anki uses [SuperMemo-2](https://www.supermemo.com/english/ol/sm2.htm), but there are [some issues with it](http://www.blueraja.com/blog/477/a-better-spaced-repetition-learning-algorithm-sm2).

I'll need to learn two new modules: Flask-login and WTForms.

I'd like to make sure that the web app looks nice and is functional on desktops as well as mobile devices in case teachers want to have their students complete their reviews in class (on, for example, school-provided iPads). I'm not sure if I can do that with the technologies I've listed so far.