# The Button Notifier

The current [/r/thebutton](https://www.reddit.com/r/thebutton) status for your desktop! The little dot follows the current flair of the button in near realtime. 

![](http://i.imgur.com/TDmEtyA.png)

This app is based heavily off of https://github.com/jamesrom/jamesrom.github.io/ and http://zeflo.com/2015/the-reddit-button/, which are two really neat projects.

## Installation:

Installation instructions:

First, install [AnyBar](https://github.com/tonsky/AnyBar). 

Second, run the following bash commands to install the script:

```bash
git clone git@github.com:HHammond/TheButtonAnybar.git
cd TheButtonAnybar
pip install -r requirements.txt
```

If the last command doesn't run, you might need admin privileges to do `pip install`. There are quite a few guides to getting python and pip setup online.

## Usage:

From inside the `TheButtonAnybar` directory, run the python app:

```bash
python app.py [optional AnyBar port number]
```

## Issues:

I built the app this morning, so it may be buggy (for example if you lose your internet connection the indicator just won't change). I haven't written any unit tests for it.

