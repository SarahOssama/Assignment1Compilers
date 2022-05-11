import json
import UtilityFunDFA as uf


class mDFA(object):
    """
    A class for DFA (Deterministic finite automata).
    """

    def __init__(self):
        """
        initialize a DFA object with
        """
        self.Nstates = []
        self.Ninput_symbols = []
        self.Ntransitions = {}
        self.Ninitial_state = ""
        self.Nfinal_states = {}

    def NFATmDFA(self, transitions, startingState, finalState, inputSymbols):
        # print("T ", transitions)
        # print("S ", startingState)
        # print("I ", inputSymbols)
        self.Ninput_symbols = set(inputSymbols)     # set of input symbols
        DFAStates = {}
        DFAStatesStack = []
        DFASymbols = {}
        temp = self.getEStates(transitions, startingState, finalState)
        temp.append(startingState)
        DFAStates["q0"] = set(temp)
        self.Ninitial_state = "q0"                  # set initial state
        DFAStatesStack.append(temp)
        # print("Final States: ", finalState)
        num = 1
        trans = 0

        for DFAS in DFAStatesStack:  # loop on every new set of states
            first = False
            for isymbol in inputSymbols:  # for each symobol in the input symbols
                statesOFEState = []
                for estate in DFAS:  # for each state in the set get Closures
                    temp2 = self.getNEStates(
                        transitions, estate, isymbol, finalState)
                    statesOFEState.extend(temp2)
                setOfStates = set(statesOFEState)
                if not (first):
                    DFASymbols["q"+str(trans)] = {isymbol: setOfStates}
                    first = True
                else:
                    DFASymbols["q"+str(trans)][isymbol] = setOfStates
                flag = False
                for x, i in DFAStates.items():  # check if the set is already in the dictionary
                    if(len(setOfStates.difference(i)) == 0):
                        flag = True
                        break
                if not(flag):
                    DFAStates["q"+str(num)] = setOfStates
                    num += 1
                DFAStatesStack.append((statesOFEState))if not(flag) else None
            trans += 1

        # print("States:", DFAStates)
        self.Nstates = set(DFAStates.keys())  # Set States for DFA
        self.setFinalStates(finalState, DFAStates)
        self.setFinalStates = set(self.Nfinal_states)
        # print(DFAStatesStack)
        # print("SymbolSet", DFASymbols)
        return DFAStates, DFASymbols

    # get Non epsilone transitions
    def getNEStates(self, Transitions, state, InputSymbol, finalState):
        non_eTransitionStates = []
        # find the states of the epsilon transition
        if(state != finalState):
            if(InputSymbol in list(Transitions[state].keys())):
                # print("Estate: ", (Transitions[state][InputSymbol]))
                for i in Transitions[state][InputSymbol]:
                    non_eTransitionStates = self.getEStates(
                        Transitions, i, finalState)
                    non_eTransitionStates.append(i)
        return non_eTransitionStates

    def getEStates(self, Transitions, state, finalState):
        eTransitionStates = []
        # find the states of the epsilon transition
        if(state != finalState):
            if("Epsilon" in list(Transitions[state].keys())):
                for eState in Transitions[state]["Epsilon"]:
                    eTransitionStates.extend(
                        self.getEStates(Transitions, eState, finalState))
                    eTransitionStates.append(eState)
        return eTransitionStates

        print(eTransitionStates)
        print(Transitions[state])

    def setFinalStates(self, finalState, DFAStates):
        """
        Set the final states of the DFA
        """
        Final = []
        for key, value in DFAStates.items():
            if(finalState in value):
                Final.append(key)
        self.Nfinal_states = set(Final)
        # print("Final States: ", self.Nfinal_states)

    def printDFA(self):
        """
        Print the DFA in a readable format
        """
        print("DFA:")
        print("States: ", self.Nstates)
        print("Input symbols: ", self.Ninput_symbols)
        print("Transitions: ", self.Ntransitions)
        print("Initial state: ", self.Ninitial_state)
        print("Final states: ", self.Nfinal_states)

    def prepToDraw(self):
        """
        Prep the NFA to diagram diagram
        """
        DrawnDFA = mDFA()
        # format the values for Transition dictionary

        # print(from1, to1)
        DrawnDFA.Nstates = set(["{}{}".format("s", i)
                                for i in self.Nstates])  # format the states
        # format the input symbols
        DrawnDFA.Ninput_symbols = set(self.Ninput_symbols)
        # format the transitions
        DrawnDFA.Ntransitions = self.Ntransitions
        # format the initial state  # set( ["{}{}".format("s",i) for i in Nfinal_states])
        DrawnDFA.Ninitial_state = "s"+str(self.Ninitial_state)
        # format the final state to a set
        DrawnDFA.Nfinal_states = {"s"+str(self.Nfinal_states)}
        return DrawnDFA

    def getTransitionFstatesSymbols(self, DFAstates, DFASymbols):
        temp2 = DFAstates
        temp = DFASymbols
        # temp2 = {'q0': {'s2', 's1', 's0', 's6'}, 'q1': {'s4', 's3'}, 'q2': {
        #     's8', 's9', 's7'}, 'q3': {'s5', 's8', 's9'}, 'q4': {'s2', 's6', 's11', 's0', 's10', 's1'}}
        # temp = {'q0': {'A': {'s4', 's3'}, 'B': set(), 'C': {'s8', 's9', 's7'}, 'A-Z': set()}, 'q1': {'A': set(), 'B': {'s5', 's8', 's9'}, 'C': set(), 'A-Z': set()}, 'q2': {'A': set(), 'B': set(), 'C': set(), 'A-Z': {'s2',
        #                                                                                                                                                                                                                 's6', 's11', 's0', 's10', 's1'}}, 'q3': {'A': set(), 'B': set(), 'C': set(), 'A-Z': {'s2', 's6', 's11', 's0', 's10', 's1'}}, 'q4': {'A': {'s4', 's3'}, 'B': set(), 'C': {'s8', 's9', 's7'}, 'A-Z': set()}}
        # temp2 = {"q0": {"s0", "s1"}, "q1": {"s2", "s3", "s4", "s5", "s7", "s0", "s1"}, "q2": {
        #     "s6", "s9"}, "q3": {"s2", "s0", "s1", "s3", "s4", "s5", "s7", "s8", "s9"}}
        # # print("DFA states", temp2)
        # temp = {}
        # temp["q0"] = {"A": "", "B": {"s2", "s3", "s4", "s5", "s7", "s0", "s1"}}
        # temp["q1"] = {"A": {"s6", "s9"}, "B": {"s2", "s0",
        #                                        "s1", "s3", "s4", "s5", "s7", "s8", "s9"}}
        # temp["q2"] = {"A": "", "B": ""}
        # temp["q3"] = {"A": {"s6", "s9"}, "B": {"s2", "s0",
        #                                        "s1", "s3", "s4", "s5", "s7", "s8", "s9"}}

        Transitions = {}
        for(key1, value1), (key2, value2) in zip(temp2.items(), temp.items()):
            # print(key1, value1)
            # print(key2, value2)
            Lilo = {}
            for ikey, ivalue in value2.items():

                if len(ivalue) != 0:
                    for x, i in temp2.items():
                        if(len(ivalue.difference(i)) == 0):
                            # print(key2, ikey, x)
                            Lilo[ikey] = {x}

                            break
                # print(Lilo)
                Transitions.update({key1: Lilo})  # if len(Lilo) > 0 else None
        print(Transitions)
        self.Ntransitions = Transitions             # format the transitions for DFA
        return Transitions

    def moreMinimization(self):
        T = self.Ntransitions
        delDuplicateKeys = {}
        for(key, value) in T.items():
            count = 0
            # print(key, value)
            for iKey, ivalue in T.items():
                if(T[iKey] == T[key] and key not in self.Nfinal_states and iKey not in self.Nfinal_states):
                    count += 1
                    if(count > 1 and key != iKey and key not in delDuplicateKeys.keys() and iKey not in delDuplicateKeys.keys()):
                        # delkeys.append(key)
                        # duplicatekeys.append(iKey)
                        delDuplicateKeys[key] = iKey
            # print(count)

        # print(T)
        for delkey, duplicate in delDuplicateKeys.items():
            if(delkey != ''):
                if(delkey == self.Ninitial_state):
                    self.Ninitial_state = duplicate
                del T[delkey]
                self.Nstates.remove(delkey)
                temp1 = {}
                for key, value in T.items():
                    newkey = duplicate
                    if(key != delkey):
                        for iKey, ivalue in value.items():
                            if(delkey in ivalue):
                                value[iKey] = {duplicate}
                            temp1.update({key: value})
                # print(temp1)
                self.Ntransitions = temp1

# t = mDFA()
# t.getTransitionFstatesSymbols(1, 2)
# Tran = {'s1': {'B': ['s2']}, 's0': {'Epsilon': ['s1']}, 's2': {'Epsilon': ['s3', 's0']}, 's5': {'A': ['s6']}, 's7': {'B': [
#     's8']}, 's4': {'Epsilon': ['s7', 's5']}, 's6': {'Epsilon': ['s9']}, 's8': {'Epsilon': ['s9']}, 's3': {'Epsilon': ['s4']}}
# state = "s0"
# # print(t.getStates(Tran, state))


# T = {'s1': {'B': ['s2']}, 's0': {'Epsilon': ['s1']}, 's2': {'Epsilon': ['s3', 's0']}, 's5': {'A': ['s6']}, 's7': {'B': [
#     's8']}, 's4': {'Epsilon': ['s7', 's5']}, 's6': {'Epsilon': ['s9']}, 's8': {'Epsilon': ['s9']}, 's3': {'Epsilon': ['s4']}}
# S = "s0"
# F = "s9"
# I = ['A', 'B']
# states, symbols = t.NFATmDFA(T, S, F, I)
# t.getTransitionFstatesSymbols(states, symbols)
# f = open('sample.json', "r")

# data = json.loads(f.read())
# minDFA = mDFA()
# transition, start, final, symbols = uf.prepToTransitions(data)
# states, symbols = minDFA.NFATmDFA(transition, start, final, symbols)
# print(states)
# print(symbols)
# minDFA.getTransitionFstatesSymbols(states, symbols)
# minDFA.moreMinimization()
# minDFA.printDFA()

# dictionary = uf.prepToJSON(
#     minDFA.Ntransitions, minDFA.Ninitial_state, minDFA.Nfinal_states)
# print(dictionary)
# with open("dfa.json", "w") as outfile:
#     json.dump(dictionary, outfile)
