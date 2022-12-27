# FocusHelper
This PC software is developed in Python, CSS, HTML, and QT framework.

Features: 
- Multithreading - can control 12 apps concurrently (block apps for a duration and/or close apps at specific times).
- Detect and block or close an app based on user's request. 
- Protect the user's setting (in advanced mode) with their emails and passwords. 
- Block websites upon user's request.
- Verify if the email the user inputs is valid and non-throwable. 
- Notify the user via email (in advanced mode) if there's an unauthorized attempt to close the app. 
- Open browser to navigate to my social media links.  

How to use:
1. Block an app for a duration: 
   - Choose an app from the list of detected apps 
   - Then, select a duration (in multiple of 10 mins) to block the app
   - Click 'Activate'
2. Set a time to close an app:
   - Choose an app from the list of detected apps
   - Then, set the time you want FocusHelper to automatically close the app
   - Click 'Activate'
3. Enabled advanced mode:
   - Click on Options -> Advanced Mode
   - You can add a new (email, password) or delete the old ones. You must enter the correct password for the email you want to delete
   - The email you enter must be valid and non-throwable
   - Once the advanced mode is activated, you cannot close the app. If someone tries closing the app, it will notify the user via email. 
   - The user can force close the app by clicking on 'Forced Terminate' with a correct password. 
