# BoltBackend
This is the backend for the Bolt app made by Nirav A, Jordan B., Zeyu W., Sam S. for the 2021 HackSC Hackathon

## Components
This backend takes care of matching users of Bolt and creating matchActivities. It does this by exposing a Heroku-Flask REST API to the application to check the waiting list for possible matches. It also computes and returns a start time for the activity.

The matching is done both using a simple closest preferred distance calculation, as well as a more complex machine learning based algorithm based on running characteristics 
