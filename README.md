# Testris_NEAT

Use NeuroEvolution of Augmenting Topologies(NEAT) to create a neural network playing the Tetris

This concept is inspried by the reference ['This Neural Network has MASTERED TETRIS']([https://www.youtube.com/watch?v=uoR4ilCWwKA](https://www.youtube.com/watch?v=1yXBNKubb2o)) on youtube.

Reference papers:
[Comparing Direct and Indirect Encodings Using Both Raw
and Hand-Designed Features in Tetris](https://dl.acm.org/doi/10.1145/3071178.3071195)
[paper2]





https://user-images.githubusercontent.com/70815842/167260045-bd46aa85-63e1-4f1d-bbcf-499490d2bd90.mp4



## How to run

If you have python, you can just open 'game.py' to play. If you don't have python, open the 'game.exe'.

If you want to change music, put the music file into the folder-'music' and open the 'game.py' with editor then change the 'file_name' in line13.

## What differeces

In order to more near the modern Tetris games, I make some changes in the game.

1. Change the fall of blocks to one set with sevent different shapes.

2. Add the predicted fallen location.

3. The next shapes is up to five.

4. Add a new ability, 'Hold'.

5. Add the music. 'A'

## How to play

Press 'down', 'left', 'right, to move the block.

Press 'space' to immediately make the block to fall down.

Press 'up' and 'z' to make block rotate(clockwise, counterclockwise)

Press 'c' to hold the current block.

## Next updates

1. Add the rule Super Rotation System 'SRS' to the game.

2. Make the AI(neural network) to play the Tettris.

3. Add the human vs human, human vs computer and computer vs computer mode.
