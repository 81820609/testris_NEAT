# Testris_NEAT

Use NeuroEvolution of Augmenting Topologies(NEAT) to create a neural network playing the Tetris

This concept is inspried by the reference ['This Neural Network has MASTERED TETRIS']([https://www.youtube.com/watch?v=uoR4ilCWwKA](https://www.youtube.com/watch?v=1yXBNKubb2o)) on youtube.

Reference papers:

[Comparing Direct and Indirect Encodings Using Both Raw
and Hand-Designed Features in Tetris](https://dl.acm.org/doi/10.1145/3071178.3071195)

[Evolving Indirectly Encoded Convolutional Neural Networks
to Play Tetris With Low-Level Features](https://dl.acm.org/doi/abs/10.1145/3205455.3205459)

AI playing demo

![Hnet-image (3)](https://user-images.githubusercontent.com/70815842/172543658-dc4c3cc0-32f9-499b-96c5-2001cadd14d8.gif)



## How do AI play the Tetris

The decision ai making in Tetris is after-state decision, which means that ai will compare the score of every position the current block put in and choose the best one.

According to papers, the input information to neural work is prefer hand-designed feature than raw screen input. The preformance of former input would much better than the other one.

Also, many papper recommend that the hand=designed features are :

1. the height of columns
2. the hole of columns
3. the height difference between columns
4. max height and min height

In this project, i simplify the hand-designed feature with just five input:

1. the whole holes
2. the whole height
3. the whole difference
4. the max height
5. the min height



