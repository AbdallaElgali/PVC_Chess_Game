# Chess Game with Depth-Limited Minimax Algorithm and Alpha-Beta Pruning

## Overview

This project implements a Chess Game using the Kivy framework in Python, featuring a player versus computer mode. The application follows the Model-View-Controller (MVC) architecture, where the game logic (Model), user interface (View), and user interaction logic (Controller) are separated into distinct components, promoting modularity and maintainability of the codebase.


## Project Structure
- model.py: This module contains the logic of the chess game, including the rules for each move of each piece, the logic for implementing an AI player and the entire functionality of the game.
- view.py: This module contains the visual aspect of the game and some functionality which concerns the visual interaction between the user and the game. 
- main.py: This is the controller of the game which connects the game functionality in the model.py and the visual in the view.py. 
- images: This folder contains the images which are used in the game
- ChessLayout.kv: This is the layout of the chess app, together with the view.py represents the visual aspect of the game. This part is written in the kivy-framework language. 
  
## Features
1. Interactive GUI: The game provides a user-friendly graphical interface built with Kivy, enabling players to interact with the chessboard seamlessly.
3. AI Opponent: The computer opponent uses the Depth-Limited Minimax Algorithm with Alpha-Beta Pruning to analyze the game state and make strategic moves.
4. Move Validation: The game ensures that all player moves adhere to the rules of chess, preventing illegal moves.
5. Checkmate Detection: The game detects when a player's king is in checkmate, signaling the end of the game.
   
## Implementation Details
- Kivy Framework: The graphical user interface is developed using Kivy, providing cross-platform support and facilitating the creation of dynamic user interfaces.
- Chess Logic: The game logic handles most aspects of chess, including piece movement, capture and checkmate detection. 
- Minimax Algorithm: The AI opponent utilizes the Depth-Limited Minimax Algorithm with Alpha-Beta Pruning to search through the game tree and determine optimal moves.
- Evaluation Function: A heuristic evaluation function is used to evaluate board positions and assign scores to potential moves, guiding the AI in decision-making. The Evaluation function used is only based on material score, however a better evaluation function will lead to a better AI overall.
- 
## Usage
1. Starting the Game: Run the Python script to launch the Chess Game.
2. Game Setup: Select the player versus computer mode and any other settings (such as difficulty level for the AI).
3. Gameplay: Make moves by clicking on the piece you want to move and then clicking on the destination square. The computer opponent will respond with its move.
4. Ending the Game: The game ends when a player achieves checkmate or stalemate. Players can also resign or exit the game at any time.
 
## Future Enhancements
1. AI Improvements: Enhance the AI's intelligence by fine-tuning the evaluation function or implementing more advanced search algorithms.
2. User Interface Enhancements: Add features such as move history display, customizable themes, and sound effects to enhance the gaming experience.
3. Difficulty Levels: Implement multiple difficulty levels for the AI, allowing players to adjust the challenge based on their skill level.



