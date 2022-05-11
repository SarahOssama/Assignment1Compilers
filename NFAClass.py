import numpy


class nNFA(object):
    """
    A class for NFA (Non-deterministic finite automata).
    """

    def __init__(self):
        """
        initialize a NFA object with
        """
        self.Nstates = []
        self.Ninput_symbols = []
        self.Ntransitions = {}
        self.Ninitial_state = ""
        self.Nfinal_states = ""

    def newNFA(self, inp):
        self.Nstates.extend((0, 1))  # add two states
        # add input string value to symbol list
        self.Ninput_symbols.append(inp)

        self.Ninitial_state = 0  # specify the state for the initial state
        self.Nfinal_states = 1  # specify the state for the final state
        # set the initial state from 1 to "s1"
        from1 = "s"+str(self.Ninitial_state)
        to1 = "s"+str(self.Nfinal_states)  # set the final state from 1 to "s1"
        # add the transition from the initial state to the final state
        self.Ntransitions[from1] = {self.Ninput_symbols[0]: {to1}}

    # to prepare the transitions to the updated states before appending
    def prepUpdateTransition(self, transDic, maxState):
        temp1 = {}
        for key, value in transDic.items():
            newkey = "s"+str(int(key[1])+maxState)
            temp1.update({newkey: value})
            for iKey, ivalue in value.items():
                value[iKey] = {"s"+str(int(x[1])+maxState) for x in ivalue}
            temp1.update({newkey: value})
        return temp1

    # implement regez AB
    def concatinate(self, other):
        # 1- we comnine the states to 2 state
        maxState = max(self.Nstates)+1
        for i in other.Nstates:
            self.Nstates.append(i+maxState)

        # 2- combine the input symbols
        self.Ninput_symbols = self.Ninput_symbols+other.Ninput_symbols

        # 3- combine the transitions
        other.Ntransitions = self.prepUpdateTransition(
            other.Ntransitions, maxState)

        self.Ntransitions.update(other.Ntransitions)
        # add the transition to link the 2 objects
        from1 = "s"+str(self.Nfinal_states)
        to1 = "s"+str(other.Ninitial_state+maxState)
        self.Ntransitions[from1] = {"": {to1}}
        # 4- initial state will be my initial state
        self.Ninitial_state = self.Ninitial_state
        # 5- final state will be the concatinated state's sinal state
        self.Nfinal_states = other.Nfinal_states+maxState

    # implement regex A+B
    def OR(self, other):
        # 1 - Combine the states
        maxState = max(self.Nstates)+1
        for i in other.Nstates:
            self.Nstates.append(i+maxState)

        for i in range(0, max(self.Nstates)+1):
            self.Nstates[i] = self.Nstates[i]+1

        # 1.2 - add new initial and final states
        newInitState = 0
        newFinalState = max(self.Nstates)+1
        self.Nstates.append(newInitState)
        self.Nstates.append(newFinalState)

        # 2- combine the input symbols
        self.Ninput_symbols = self.Ninput_symbols+other.Ninput_symbols

        # 3- combine the transitions
        # 3.1 prep the added transitions
        other.Ntransitions = self.prepUpdateTransition(
            other.Ntransitions, maxState)
        self.Ntransitions.update(other.Ntransitions)
        # 3.2 prep the self transitions
        self.Ntransitions = self.prepUpdateTransition(
            self.Ntransitions, 1)
        # 3.3 prep the old self and other initial and final states
        self.Ninitial_state = int(self.Ninitial_state)+1
        self.Nfinal_states = int(self.Nfinal_states)+1
        other.Ninitial_state = int(self.Nfinal_states)+1
        other.Nfinal_states = int(self.Nfinal_states)+1+other.Nfinal_states
        # add the transition to link the 2 objects
        from1 = "s"+str(newInitState)
        to1 = "s"+str(newFinalState)
        self.Ntransitions[from1] = {
            "": {"s"+str(self.Ninitial_state), "s"+str(other.Ninitial_state)}}
        self.Ntransitions["s"+str(self.Nfinal_states)] = {"": {to1}}
        self.Ntransitions["s"+str(other.Nfinal_states)] = {"": {to1}}

        # 4- new state will be initial for all
        self.Ninitial_state = newInitState
        # 5- new final state will be final for OR
        self.Nfinal_states = newFinalState

    # implement regex A*
    def star(self):
        # 1- add new initial and final states
        for i in range(0, max(self.Nstates)+1):
            self.Nstates[i] = self.Nstates[i]+1
        newInitState = 0
        newFinalState = max(self.Nstates)+1
        self.Nstates.append(newInitState)
        self.Nstates.append(newFinalState)

        # 2- Symbols are the same
        # 3- Update Transitions
        # 3.1- Prep Self Transitions
        self.Ntransitions = self.prepUpdateTransition(self.Ntransitions, 1)
        # 3.2- Add new transitions  1) form new initial to new Final b) from self final to new initial
        self.Ninitial_state = int(self.Ninitial_state)+1
        self.Nfinal_states = int(self.Nfinal_states)+1
        from1 = "s"+str(newInitState)
        to1 = "s"+str(newFinalState)
        self.Ntransitions[from1] = {"": {to1, "s"+str(self.Ninitial_state)}}
        self.Ntransitions["s"+str(self.Nfinal_states)] = {"": {from1, to1}}
        # 4- new state will be initial for all
        self.Ninitial_state = newInitState
        # 5- new final state will be final for star
        self.Nfinal_states = newFinalState

    # implement regex A+
    def plus(self):
        # 1- add new initial and final states
        for i in range(0, max(self.Nstates)+1):
            self.Nstates[i] = self.Nstates[i]+1
        newInitState = 0
        newFinalState = max(self.Nstates)+1
        self.Nstates.append(newInitState)
        self.Nstates.append(newFinalState)

        # 2- Symbols are the same
        # 3- Update Transitions
        # 3.1- Prep Self Transitions
        self.Ntransitions = self.prepUpdateTransition(self.Ntransitions, 1)
        # 3.2- Add new transitions  1) form new initial to new Final b) from self final to new initial
        self.Ninitial_state = int(self.Ninitial_state)+1
        self.Nfinal_states = int(self.Nfinal_states)+1
        from1 = "s"+str(newInitState)
        to1 = "s"+str(newFinalState)
        self.Ntransitions[from1] = {"": {"s"+str(self.Ninitial_state)}}
        self.Ntransitions["s"+str(self.Nfinal_states)] = {"": {from1, to1}}
        # 4- new state will be initial for all
        self.Ninitial_state = newInitState
        # 5- new final state will be final for star
        self.Nfinal_states = newFinalState

    def printNFA(self):
        print("Test NFA:")
        print("Nstates:", self.Nstates)
        print("Ninput_symbols:", self.Ninput_symbols)
        print("Ntransitions:", self.Ntransitions)
        print("Ninitial_state:", self.Ninitial_state)
        print("Nfinal_states:", self.Nfinal_states)

    def prepToDraw(self):
        """
        Prep the NFA to diagram diagram
        """
        drawnNFA = nNFA()
        # format the values for Transition dictionary

        # print(from1, to1)
        drawnNFA.Nstates = set(["{}{}".format("s", i)
                                for i in self.Nstates])  # format the states
        # format the input symbols
        drawnNFA.Ninput_symbols = set(self.Ninput_symbols)
        # format the transitions
        drawnNFA.Ntransitions = self.Ntransitions
        # format the initial state  # set( ["{}{}".format("s",i) for i in Nfinal_states])
        drawnNFA.Ninitial_state = "s"+str(self.Ninitial_state)
        # format the final state to a set
        drawnNFA.Nfinal_states = {"s"+str(self.Nfinal_states)}
        return drawnNFA


# Exp1 = nNFA()
# Exp1.newNFA("Hello")
# Exp1.printNFA()
# # # Exp1.printNFA()
# # draw1 = Exp1.prepToDraw()
# # # draw1.printNFA()
# Exp2 = nNFA()
# Exp2.newNFA("World")
# Exp1.OR(Exp2)

# Exp1.star()

# # # # Exp2.printNFA()
# # # # print(Exp2.Nstates)
# # # Exp1.concatinate(Exp2)
# Exp1.printNFA()
# # drawn2 = Exp1.prepToDraw()
# # drawn2.printNFA()
