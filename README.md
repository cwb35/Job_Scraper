# Job_Scraper

Analytics 903 Project

Authors: Colin Cambo, Robin Marra, John MacLeod

# Overview

This repository is meant to help people compare keyword frequency among job listings for a specified title in a specified area, by scraping Indeed.com for the most recent job postings. 

# About

Today's job market is moving very fast. With the fast paced advance of technology new skills are always being sought after, and old skills are being replaced. With the following script one is easily able to compare the job market's desire for any skills in any geographical region.

# Requirements

This script has very little requirements. To install them type the following command into the terminal when in the same directory as the project.

` pip install -r requirements.txt `

This should install everything needed to start running the project.

# How to run

The program is run from the command line as follows:

`python Job_Scraper.py <job_title> <location> <radius> <num_jobs> <-terms> <-output>`

Where the arguments are:
  * __job_title:__ String - Title of job interested, surrounded in quotes
  * __location:__ String - Location of the job posting, surrounded in quotes
  * __radius:__ Integer - How far from location you want job postings
  * __num_jobs:__ Integer - How many job postings should be returned
  * __-terms:__ (Optional) List of Strings - The terms you want to search each document for
  * __-output:__ (Optional) String - Name of file you want results outputted to
  
# Example

Here is what an example run would look like:

`python Job_Scraper.py "Data Scientist" "Durham NH" 50 100 -terms "SAS" "Python" "R" "Machine Learning" `

