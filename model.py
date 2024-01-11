from typing import Callable

# Stores the two numbers that are valid in this world
class World:

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.sum = x + y
        self.product = x * y
        self.relations_S = []
        self.relations_P = []

# Stores all currently considered worlds
class Kripke_Model:

    # The range minNumber to maxNumber is inclusive on both ends
    def __init__(self, minNumber: int, maxNumber: int, constraints: list [Callable[[int, int], bool]]) -> None:
        self.minNumber = minNumber
        self.maxNumber = maxNumber
        self.constraints = constraints
        self.worlds = {}

        #Worlds with the same product or sum (both are dictionaries of the form (int, set[tuple[int,int]]))
        self.pWorlds = {}
        self.sWorlds = {}

        # Add the appropriate worlds and relations between worlds
        self._generateWorlds()
        self._generateRelations()

    def _generateWorlds(self) -> None:
        for x in range(self.minNumber, self.maxNumber + 1):
            for y in range(self.minNumber, self.maxNumber + 1):
                valid_world = True

                # Check whether the world is in accordance with all initial constraints
                for constraint in self.constraints:
                    valid_world = valid_world and constraint(x, y)
                    if not valid_world:
                        break
                
                if valid_world:
                    # Add the valid to the dictionary of worlds
                    self.worlds[(x,y)] = World(x,y)

                    # Group Worlds with the same Sums or Products
                    pWorld = self.pWorlds.get(x*y, set())
                    pWorld.add((x,y))
                    sWorld = self.sWorlds.get(x+y, set())
                    sWorld.add((x,y))
                    self.pWorlds[x*y] = set(pWorld)
                    self.sWorlds[x+y] = set(sWorld)

    # Adds Product or Sum relations if the Product/Sum is the same between them (also includes reflexive relations)
    def _generateRelations(self) -> None:
        for world in self.worlds.values():
            world.relations_S = list(self.sWorlds[world.sum])
            world.relations_P = list(self.pWorlds[world.product])

    # The announcement is presumed to be truthful
    # The announcement is assumed to be a function that returns a boolean, use the logic_parser to convert logic statements to python functions
    def publicAnnouncementUpdate(self, announcement: Callable[[World, dict[tuple [int, int], World]], bool]) -> None:
        delete_worlds = []

        # Mark all worlds in which that announcement is not truthful
        for world in self.worlds.values():
            if not announcement(world, self.worlds):
                delete_worlds.append((world.x, world.y))

        # Delete the worlds as well as all connections to it
        for worldNums in delete_worlds:
            world = self.worlds[worldNums]
            
            for productWorld in world.relations_P:
                if productWorld != worldNums:
                    self.worlds[productWorld].relations_P.remove(worldNums)
            
            for sumWorld in world.relations_S:
                if sumWorld != worldNums:
                    self.worlds[sumWorld].relations_S.remove(worldNums)
            self.worlds.pop(worldNums)

    # Will evaluate the given function on either the given world or all if None is specified and
    # Will determine whether the function is true for the scope
    def evaluateStatement(self, statement: Callable[[World, dict[tuple [int, int], World]], bool], evaluatedWorld: tuple [int, int] | None = None) -> bool:
        if evaluatedWorld is not None:
            return statement(self.worlds[evaluatedWorld], self.worlds) 

        for worldCoords in self.worlds:
            if not statement(self.worlds[worldCoords], self.worlds):
                return False
        return True


#*****************************************************************
# Functions for testing

def xSmallerEqual(x: int, y: int):
    return x <= y

def xySumLessEq100(x: int, y: int):
    return x + y <= 100

def p_does_not_know(world: World, worlds: World):
    return len(world.relations_P) > 1

def s_knows_p_does_not_know(world: World, worlds: World):
    for worldNums in world.relations_S:
        if p_knows(worlds[worldNums], worlds):
            return False
    return True

def s_knows_p_does_not_know_and_p_does_not_know(world: World, worlds: World):
    return p_does_not_know(world, worlds) and s_knows_p_does_not_know(world, worlds)

def p_knows(world: World, worlds: World):
    return len(world.relations_P) <= 1

def s_does_not_know(world: World, worlds: World):
    return len(world.relations_S) > 1

def s_knows(world: World, worlds: World):
    return len(world.relations_S) <= 1

def x4_and_y13(world: World, worlds: World):
    return world.x == 4 and world.y == 13

if __name__ == "__main__":
    model = Kripke_Model(2, 100, [xSmallerEqual, xySumLessEq100])
    print(model.evaluateStatement(x4_and_y13))
    model.publicAnnouncementUpdate(s_knows_p_does_not_know)
    model.publicAnnouncementUpdate(p_knows)
    model.publicAnnouncementUpdate(s_knows)
    print(model.evaluateStatement(x4_and_y13))
    print(model.worlds.keys())