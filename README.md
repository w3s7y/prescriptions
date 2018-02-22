# prescriptions
Python project which looks to gain insights into public government prescription data

## The data source
The source for the data in this project is:
https://data.gov.uk/dataset/prescribing-by-gp-practice-presentation-level

For testing, I used the datasets (CSV) from October 2017.

Inside the etl pipeline it is envisaged we eventually use googles geo API to enrich
the data with latitude and longitude coordinates based on the GPs address to enhance
the accuracy of correlations (see Goals / objectives). 

## Goals / objectives
This project aims to answer the following basic questions using a mixture of statistics 
and machine learning models:

###### Are there any correlations between geographic areas and specific drug groups?
* Anti-Depressants
* Drug addiction medicines (methadone or champix for e.g)
* Antibiotics
* Analgesics (pain-killers)
* Beta blockers

We can add more groups, but I think 5 is a good starter for ten to see what is possible. 

###### Are there any GPs that over prescribe certain medicines?
* What is the average amount of antibiotics prescribed by a practice?
* How does that compare to other practices in the same area? 
* Are there any practices in the UK which _really_ overdo it prescribing _X_?

###### Could we predict where and what type of medicine is prescribed in the UK at what time of the year?
This could be used by the NHS for things like stock control and distribution of drugs and ensuring 
pharmacies have the drugs that practices are expected to prescribe in the following months for e.g.

###### Your question for the data here...

## Running the project
At a High-Level

* Goto the above mentioned site and download a dataset (they come in month-by-month csv format)
* Prepare your python venv (see below)
* Ingest the code into database of your choice (see below, I used postgresql and elasticsearch)
* Acvtivate your venv and run the etl pipeline to load the data into a classic relational database.
* Run the statistics module, look at the results...
* Run the ml module to train models and persist trained models in the DB for later use.
* When new datasets are produced at source, use models to predict future prescriptions.

