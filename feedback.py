class Feedback(object):

    def __init__(self):
        self.welcomeMessage = """
    Welcome to the Sum and Product (Impossible) Riddle! Do not get discouraged by its name - it can be solved though not easily.
    Alright, let's start! Throughout the riddle, you will receive several prompts offering help and explanations
    if you want by typing y, otherwise, you can ignore them by typing n. Either way, good luck!\n"""

    def beginningMessage(self):
        print("The original Sum and Product riddle is as follows: ") 
    
    def statement1(self):
        print("The first statement is: S knows that P does not know x and y.")
    
    def statement2(self):
        print("The second statement is: P knows x and y.")
    
    def statement3(self):
        print("The third statement is: S knows x and y.")
    
    def getHint1(self):
        user_preference1 = input("Would you like to get a hint? (y/n): ")
        if user_preference1 == "y":
            print("""Consider the first statement: S knows that P does not know x and y. The hint is that for each
sum decomposition of the number (x + y), the product has more than one product decomposition.""")
        user_preference2 = input("Would you like to get another hint? (y/n): ")
        if user_preference2 == "y":
            print("""If x and y were prime numbers, then the product would have only one product decomposition.
Hence, x and y are not prime numbers.""")
        
    def getHint2(self):
        user_preference1 = input("Would you like to get a hint? (y/n): ")
        if user_preference1 == "y":
            print("""Consider the second statement: P knows x and y. The hint is that the number (x * y) has only one product
decomposition for which the previous fact (S knows that P does not know x and y) is true.""")
        
    def getHint3(self):
        user_preference1 = input("Would you like to get a hint? (y/n): ")
        if user_preference1 == "y":
            print("""Consider the third statement: S knows x and y. The hint is that the number x + y has only one sum
decomposition for which the previous fact is true ( P knows x and y) is true."""
                                  )
    
    def rightTrack(self, model, total_worlds):
        user_preference3 = input("Would you like to check if you are on the right track? (y/n): ")
        if user_preference3 == "y":
        # Display the number of deleted and possible worlds
            print("While the number of deleted worlds/pairs of (x,y) is " + str(total_worlds - len(model.worlds.keys())) +
            ", the number of possible worlds/pairs of (x,y) is " + str(len(model.worlds.keys())) + ".")

    def consideredWorlds(self, model):
        user_preference4 = input("Would you like to see the worlds that are still considered? (y/n): ")
        if user_preference4 == "y":
            print(model.worlds.keys())
    
    def finalMessage(self, model):
        print("""The possible values for x and y after the first statement are """ + str(model.worlds.keys()) + """.""")

    def noSolution(self):
        print("""The number of possible worlds is 0 for the logic announcements you specified. In other words,
the riddle is impossible to solve with the given logic announcements, as there is no solution.""")
