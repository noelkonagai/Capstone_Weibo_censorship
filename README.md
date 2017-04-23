## Capstone Project - Data Driven Analysis of Self-Censorship on Weibo

This is my senior final project that concludes my Autocracy and Democracy Studies major with a focus on computational methods. For this project I have collected data from www.greatfire.org/analyzer on 31162 keywords monitored. As the website does not have a publicly accessible API at the time of the project, I created several Python programs to navigate myself through the data collection. 

## Overview of the project
First, I created a program to scrape the monitored keywords on GreatFire.org. Second, I made a program making POST requests (post_request.py) to collect the response JSON files. As some of the URLs on GreatFire.org were encoded incorrecltly, or if they were long the end of the string was cut off when displaying on the website, those returned an empty JSON file. Third, to filter out erroneous JSON files, I created an exceptions list (exceptions.txt). This left me with 23597 keywords. Next, I created a program to create a unified JSON file that contains the relevant measurements from the previous 23597 JSON files, meaning I only recodred a keyword ID, the keyword itself, and the verdicts on whether it was blocked or unblocked with the given timestamps. For data manipulation purposes, I created a CSV file as well.

**More updates coming soon**

## Contributors
Noel Konagai - Project Lead
Dr. Pierre Landry - Falculty Mentor
