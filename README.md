#Project Overview
Title: Guess Who! Celebrity Edition

##Description: 
A Python script that uses a decision tree classifier to guess a celebrity based on user-provided attributes (age, profession, nationality, gender, status, etc).

##How It Works
Data Preprocessing:
Loads gathered celebrity data.
Removes duplicate entries.
Groups rare professions into an "Other" category.
Drops irrelevant columns.
Binarizes Age into under_30, bet_30 & 50, and over_50.
One-hot encodes categorical features.

##Model Training:
Trains a DecisionTreeClassifier with entropy criterion to predict celebrity names based on preprocessed features.

##User Interaction:
Prompts the user for celebrity attributes.
Converts inputs into the model’s feature format.
Predicts a celebrity name and offers to play again.