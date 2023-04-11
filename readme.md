# World Cup Betting App
This is a web application built with Python, JavaScript, and Flask, as the final project for the CS50 course from Harvard University. The app allows users to create accounts and place bets on the results of matches in the 2022 FIFA World Cup in Qatar. The app uses an API to fetch the latest match results and calculates points for each user based on how accurately they predicted the outcomes. The app displays a leaderboard with the ranking of all users based on their total points.

## Installation
To install the app, you need to have Python and Flask installed on your system. You can clone the repository by running the following command in your terminal:

```
git clone https://github.com/gryllifish/prode
```

Then, navigate to the project directory and install the required dependencies using pip:

```
cd Final
pip install -r requirements.txt
```

## Usage
To start the app, run the following command in your terminal:

```
flask run
```

This will start a local server on your machine, and you can access the app by opening a web browser and navigating to http://localhost:5000. From there, you can create an account, place bets on upcoming matches, and view the leaderboard to see how you rank compared to other users.

## API
The app uses the World Cup JSON 2022 API to fetch the latest match results and information about upcoming matches. The API provides data in JSON format, which is parsed by the app using the requests library in Python.
https://github.com/estiens/world_cup_json

## Contributing
This project is currently not accepting contributions, as it was created as part of a course assignment. However, if you have any feedback or suggestions for improvement, feel free to open an issue or send a pull request.