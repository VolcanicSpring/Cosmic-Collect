Cosmic Collect is a casual collecting game in Python focused on stress relieving.

I made this back in late 2024 for fun and left it after school got more stressful. Now I'm coming back to it with more coding experience to improve the game.

In this game you start as one of the smallest objects in the universe and eat your way through the next evolution. 
Gain Food to upgrade the 3 current avaliable upgrades: size/fov, new food and evolve

Controls: joystick

Requirements: Python, kivy (pip install kivy kivymd)

To do list:
- organize code into multiple files
- revamp gui for upgrades, icons, background
- split fov upgrade into 2: bigger size and more food
- add food multipliers for each level up
- add up to 3 evolutions with corresponding upgrades
- add rebirth mechanic for continuous play
- add home screen with following buttons: play, quit, select control, speedrun, restart
- add WASD controls
- add option to choose between joystick and WASD

Known Bugs:
- when code is run, the first entity spawned doesn't respond to changes when a button is pressed. goes away when replaced by new food
- when window size is enlarged, UIs do not adjust
- player may get too big and break game
