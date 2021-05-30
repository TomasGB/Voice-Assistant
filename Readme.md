# Hanna Voice Assistant

Python Assistant capable of taking voice commands and interact with different third party APIs (Google calendar, Twitch,Twitter, OpenWeather). The goal it's to automate daily tasks.

## Project structure

* src /

    * `apiCredential.py` In this file are located all API's credentials.

    * `functionalities.py` In this file are located all the asisstant functionatilies. 

    * `main.py` This is the file that runs the assistant.

    * `speak.py` In this file is located all the speech recognition and text to speech code related.

    * `triggers.py` In this file are located all lists of sentences or words that triggers the functionalities.


## Functionalities

Hanna has different functionalities, that can be found inside "functionalities.py". Some of them are:

-   Check for upcoming events on Google Calendar.
-   Check if your favourites Twitch streamers are currently live.
-   Read the latest tweets on your timeline.
-   Read your countrys Trending Topics.
-   Publish a tweet.
-   Open websites.
-   Play videos or songs on Youtube.

## Dependencies

-   Twitch API [Link](https://dev.twitch.tv/docs/api/)
-   Twitter API [Link](https://developer.twitter.com/en)
-   Google Calendar API [Link](https://developers.google.com/calendar)
-   OpenWeatherMap API [Link](https://openweathermap.org/api)
-   Selenium [Link](https://selenium-python.readthedocs.io/)
-   PyAudio [Link](https://pypi.org/project/PyAudio/)
-   Pyttsx3 [Link](https://pypi.org/project/pyttsx3/)

## How to use:

-   Open up command prompt / terminal.
-   Install all the dependencies.
-   Rename the 'apiCredentialsSample.py' file to "apiCredentials.py" and put your own keys.
-   Change directory inside src folder with "cd src".
-   Run "main.py".
-   Click the start button on the GUI.
-   To wake up Hanna just say the wake word "Hanna".
-   Ask for a task.
