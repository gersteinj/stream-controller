# GSCRL Stream Manager

## Getting Started 

This is *very* specific to the October 1 event. I'll generalize this later.

You'll need Python 3.11 (3.10 *might* work?) for the backend and node/npm for the frontend. I'll make this easier to run in the future, but there isn't time right now.

### Installation
1. Clone the repository. If that's not possible, just download the zip file and unzip it somewhere you can find it. There are plenty of people there who can help you.
2. Open the command line. If you're not comfortable with that, get someone who is or reach out to me and I can walk you through it in more detail.
3. Navigate into the `app` directory and run `pip install -r requirements.txt` to install all requirements for the backend.
4. Navigate into the `webUI` directory and run `npm install` to install all requirements for the frontend

### Run the backend
1. Navigate to the root directory of the repository
2. Run `uvicorn app.main:app --reload` to run the backend
3. Don't close the terminal or the backend will stop running!

### Run the frontend
1. Open a _new_ terminal window/tab
2. Navigate to the `webUI` directory
3. Run `npm run dev` to start a local server running the website. Technically you should be able to build this and run it as a static site but I don't have time to test it right now.

## Using the stream controller

Go to [the main page for the stream controller](http://localhost:3000/), which will also be linked in the command line when you run the front end. Navigation links are at the top of the main page. The Control Panel is used for resetting the timer and the arena.

If you want to try using the stream overlay, you can add the robots and let me know if you need help.

Good luck! You have my phone number if you need me.
