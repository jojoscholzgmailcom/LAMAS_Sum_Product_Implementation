import ply.yacc as yacc
import ply.lex as lex
import re
import textwrap
from model import Kripke_Model
from logic_lexer import Logic_Lexer
from logic_parser import Logic_Parser
from logic_parser import *
from feedback import Feedback

def xSmallerEqual(x: int, y: int):
    return x <= y

def xySumLessEq100(x: int, y: int):
    return x + y <= 100

def originalRiddle(model: Kripke_Model):
    announcements = ["Ks-Kp(x & y)", "Kp(x & y)", "Ks(x & y)"]
    feedback.beginningMessage()
    total_worlds = len(model.worlds.keys())
    for _ in range(3):
        model.publicAnnouncementUpdate(parser.parse(announcements[_]))
        string1 = 'statement' + str(_ + 1)
        getattr(feedback, string1)()
        string2 = 'getHint' + str(_ + 1)
        getattr(feedback, string2)()
        feedback.rightTrack(model, total_worlds)
        if len(model.worlds.keys()) >= 1:
            feedback.consideredWorlds(model)
            total_worlds = len(model.worlds.keys())
        else:
            feedback.noSolution()
            break


if __name__ == "__main__":
    # Build the parser
    logic_lexer = Logic_Lexer()
    logic_lexer.build()
    lexer = logic_lexer.lexer
    logic_parser = Logic_Parser()
    logic_parser.build()
    parser = logic_parser.parser

    #print(parser.parse("Kp(x4 & y13) | Ks(-Kp(x4 & y13))"), "\n\n\n\n")# Works
    #print(parser.parse("Kp(x4 & y13) | Ks-Kp(x4 & y13)"))# Works

    # Combined Test (Works)

    # This displays the example of the original Sum and Product riddle
    # Public Announcement can be any logic statement without common knowledge 
    # - is negation; > is the arrow; = is the bidirectional arrow; & is and; | is or
    # p and s are the agents; Knowledge operators have a capital K followed by the letter of the agent e.g. Kp
    # x and y are the two numbers Kpx means that p knows the value of x
    # x14 or y14 indicate that the repective variable has that value

    ##############################################################################################################

    feedback = Feedback()
    print(textwrap.dedent(feedback.welcomeMessage).strip())

    while True:

        choice1 = input("Would you like to see the original Sum and Product riddle? (y/n): ")
        if choice1 == "n":
            minNumber = int(input("What is the minimum value for x and y? "))   
            maxNumber = int(input("What is the maximum value for x and y? "))
            # maximumSum = int(input("What is the maximum value for the sum of x and y? "))
            model = Kripke_Model(minNumber, maxNumber, [xSmallerEqual, xySumLessEq100])

        else:
            model = Kripke_Model(2, 99, [xSmallerEqual, xySumLessEq100])

        total_worlds = len(model.worlds.keys())

        if choice1 == "n":
            choice2 = input("Would you like to specify different logic announcements from the original Sum and Product riddle?  (y/n): ")
            if choice2 == "y":
                while True:
                    input1 = input("Please enter a logic announcement. If this is the last announcement, please enter done.")
                    if input1 == "done":
                        break
                    model.publicAnnouncementUpdate(parser.parse(input1))
                    feedback.rightTrack(model, total_worlds)
                    print(len(model.worlds.keys()))
                    if len(model.worlds.keys()) >= 1:
                        feedback.consideredWorlds(model)
                        total_worlds = len(model.worlds.keys())
                    else:
                        feedback.noSolution()
                        break
            else:
                originalRiddle(model)
        else:
            originalRiddle(model)

        feedback.finalMessage(model)
        user_preference = input("Would you like to try again? (y/n): ")
        if user_preference == "n":
            break    

    print(model.evaluateStatement(parser.parse("x4 & y13"))) # Evaluate whether the statement is true
    print(model.worlds.keys()) # Display all worlds that are considered, only the values of x and y are displayed