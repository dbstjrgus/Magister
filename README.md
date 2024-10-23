# GOMOKU AI magister

This is a traditional Gomoku game played by 2 players and it is a five-in-a-row.

- Gomoku from wiki: Gomoku, also called Five in a Row, is an abstract strategy board game. Players alternate turns placing a stone of their color on an empty section. The winner is the first player to form an unbroken chain of five stones horizontally, vertically, or diagonally. (Reference: https://en.wikipedia.org/wiki/Gomoku)

That was what the original readme said. If I am also correct, game pigeon also has some gomoku variation. I don't know. I don't have an iphone. 

I made a Gomoku AI. The AI part is pretty self explanatory. It is supposed to play Gomoku really well. 

After the loss of Lee Sae Dol against AlphaGo in 2016, what most people don't know is that Google had two more deepmind AIs developed. Maister (p) and Magister (p). They each went 33 - 0 and 35 - 0 (i think) on the largest online Baduk platform, beating the best players in the world like it was nothing. 
That is why I decided to name my project Magister. 

To be completely honest, I tried reinforcement learning and failed. 

## How to run
```bash
python main.py
```
The actual player goes first. In actual Gomoku, the black stone goes first, but while I was tinkering with the game I made white go first.
You have to click on the board one more time for AI to operate and make a move. 
Be careful not to press aplace in the board where there is already a stone. Also, always press "new game" button to start. The code won't operate if you don't.  




## Requirement
```bash
pygame==1.9.6
```

## Game screenshots

![GOMOKU for 2 players](https://raw.githubusercontent.com/positive235/gomoku/master/img/20190504gomoku.gif)

## Methods
First AI is an MCTS algorithm. It works like a normal MCTS algorithm where the state of the board is the current node in the tree. If the node is fully expanded, the tree simulates a random game multiple times to see how "good" a current situation is and how good a proceeding move can be. 
After that, using the Upper Confidence bound function it returns the move that is the most promising. 
```bash
mcts.expand()
mcts.best()
mcts.ai_make_move() 
```
This itself isn't really learning. It simply makes better moves as the game goes. The problem with this is that in a two player game where moves are limitless, the MCTS may not find the best next move easily. That is why I made another AI using CNNs.
The CNN uses a numpy array of binary data of whether a stone is placed or not, or whether the stone is white or not. The neural model extracts key features and spits out the ideal coordinates for the stone to go. 

The part I am still working on that I have partially got to work was combining the two. Theoretically, when the CNN generates a probability distribution given a situation, the MCTS will search given such distribution. 
## Datasets 
I used the dataset in gomocup championships which logs all the games played in the tournament. I essentially made one "state" the solution for another state to train the model, imitating the playing of the great players who played in that touranment. Yes that is an actual thing. 
So, when there is a certain situation on the board, the AI will approach it like solving puzzles.

Also, I took code from a few people and some from CHATGPT. I was inspired by this person -->  @bbanghyong.
I also made a cnn model and took one of his pretrained model to compare performances. I modified his neural network to make mine because his was way too complex for my macbook, so I simplified layers to detect more local patterns instead of the whole board, most notably making my convolution matrixes size 3 and not 7. That part I got help from CHATGPT. 

I also used some of his preprocessing data, and then wrangled it to work with my pygame, since he was using a package called ursina which was a lot nicer but I had to work within project parametres. 

