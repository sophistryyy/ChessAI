#script to test AI against random player

import chess_game

print("Test function of minimax AI vs random AI opponent")
print("**************")
for i in range(1,11):
    print("Test", i, ":")
    winner = chess_game.main("random") 
    if(winner == "black"):
        print("PASSED")
    else:
        print("FAILED")
    print("**************")