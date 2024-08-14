# Project Overview: A* and Game-Tree Algorithms Implementation #

## Introduction ##
This project implements the A* and Game-Tree algorithms as part of an AI agent testing framework. Designed to assess the effectiveness of these algorithms, the framework highlights their strengths and weaknesses through both printed results and graphical user interfaces (GUI) for enhanced visualization.

## Configuration Guide ##

### Setting Up Your Game Configuration ###
- **Coordinate Configuration**: Define the total nodes along the X and Y axes (e.g., `#X 8` and `#Y 12`).
- **Package and Delivery**: Specify the location, appearance time, and delivery time for packages (e.g., `#P 2 0 0 D 3 0 13`).
- **Starting Positions**: Set the starting nodes for players (e.g., `#S 0 0` and `#S 6 0`).

### Game Modes ###
Configure the interaction between agents using flags:
- **Zero-Sum Game**: `Z`
- **Semi-Cooperative**: `S`
- **Fully Cooperative**: `W`

**Important**: Ensure consistency in flags across configurations; mixed flags are not supported.

## Configuration File ##
Adjust game settings in the config.txt file located in the support_files folder. Note that larger configurations may lead to extended timeouts. The default maximum depth of the game tree is 13, which can be modified in the consts_and_enums/game_tree_consts directory by changing the MAX_DEPTH_CUTOFF.

## Execution ##
To run the project, navigate to the main directory and execute the program. The logger will track and output the game's progress to the standard output, and a detailed log file will be generated in the support_files/logging_directory at the conclusion of each session.

## Sample Configurations ##
Explore various game modes and their impacts by reviewing the sample configurations provided in the support_files/different_results_config.txt file.
