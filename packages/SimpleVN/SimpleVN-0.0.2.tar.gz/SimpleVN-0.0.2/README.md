# Simple Vn

A simple Python module for creating super quick visual novels

## Implementation

The module is written entirely in Python 3 (Python 2 Compatible). All classes and code is contained in main.py. The code is organized in a structured, object orientated approach with the use of two main game states: speaking and replying.

## How To Use

Install via pip with the command

	pip -m install simplevn

Make sure python is added to you PATH

The basic code format to get a game going is

	import simplevn

	// Create a new game instance
	g = simplevn.Game()

	// Load all facial expressions/body gestures
	g.load_expressions([
		"smiling.png",
		"frowning.png",
		"laughing.png"
	])

	// Load all backgrounds/backdrops
	g.load_backgrounds([
		"school.png",
		"hallway.png",
		"bedroom.png",
		"gymnasium.png"
	])

	// Load formatted scripts
	g.load_scripts([
		"scene1.txt",
		"scene2.txt"
	]) 

	// Run game continuously
	while(true):
		g.run()


