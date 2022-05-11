def preptoConcat(Regex):
    afterDots = []
    for i in range(len(Regex)-1):
        if((Regex[i].isalpha() | Regex[i].isdigit() | (Regex[i] == ')') | (Regex[i] == '*') | (Regex[i] == '+')) and ((Regex[i+1] != '|') and (Regex[i+1] != '+') and (Regex[i+1] != '*') and (Regex[i+1] != ')'))):
            afterDots.append(Regex[i])
            afterDots.append('.')
        else:
            afterDots.append(Regex[i])

    afterDots.append(Regex[len(Regex)-1])
    emptyDots = ''
    finalDots = emptyDots.join(afterDots)
    return finalDots


def preptoCharacterSet(Regex):
    afterPrep = []
    newCharacter = ""
    for i in range(len(Regex)-1):
        if(Regex[i] == "["):
            newCharacter = ""
            Regex.index("]")
            for j in range(i+1, Regex.index("]")):
                newCharacter += Regex[j]
            # while(Regex[i] != "]"):
            #     Regex = Regex.replace(Regex[i], "")
            # replacement = "(" + "X" + ")"
            Regex = Regex.replace(newCharacter, "X")
            Regex = Regex.replace("[", "(")
            Regex = Regex.replace("]", ")")
            break

    # print(newCharacter)
    return newCharacter, Regex


def postfix(regex):
    outputQueue = []
    OperatorStack = []
    for i in range(0, len(regex)):
        if(regex[i].isalpha() | regex[i].isdigit()):
            # is a letter or digit so add to output queue
            outputQueue.append(regex[i])
        elif(regex[i] == '('):
            # special character to push to operator stack
            OperatorStack.append(regex[i])
            # print("(")
        elif(regex[i] == ')'):
            # pop all elemenets from operatpr stack till (  and add them to output queue
            while(OperatorStack[-1] != '(' and len(OperatorStack) != 0):
                outputQueue.append(OperatorStack.pop())
            # throw the open Bracket "("
            if(OperatorStack[-1] == '(' and len(OperatorStack) != 0):
                OperatorStack.pop()
            # print(")")
        else:
            # add to operator stack
            OperatorStack.append(regex[i])

    # pop all elements from operator stack and add to output queue
    while(len(OperatorStack) != 0):
        outputQueue.append(OperatorStack.pop())

    postfixVal = ''
    out = postfixVal.join(outputQueue)
    return out


def prepToJSON(transitions, startingState, finalStates):
    jsonTransitions = {}
    jsonTransitions["StartingState"] = startingState
    finalFound = False
    for key, value in transitions.items():
        # value["isTerminatingState"] = False
        # print(key, value)
        # jsonTransitions.update({key: tem})
        for iKey, ivalue in value.items():
            endStates = []
            for i in ivalue:
                endStates.append(i)
            # print(iKey, endStates)
            iKey = "Epsilon"if(iKey == "") else iKey
            temp = {}
            finalFound = key in finalStates
            temp["isTerminatingState"] = (key in finalStates)
            temp[iKey] = endStates

            # print(temp)
            jsonTransitions.update({key: temp})
    if(finalFound == False):  # if no final state is found, add final state
        for i in finalStates:
            jsonTransitions[i] = {"isTerminatingState": True}
    # print(jsonTransitions)
    return jsonTransitions


# dictTemp = {'s1': {'A': {'s2'}}, 's3': {'B': {'s4'}}, 's2': {'': {'s3'}}, 's5': {'C': {'s6'}}, 's0': {'': {'s1', 's5'}}, 's4': {
#     '': {'s7'}}, 's6': {'': {'s7'}}, 's9': {'A-Za-z': {'s10'}}, 's8': {'': {'s9'}}, 's10': {'': {'s8', 's11'}}, 's7': {'': {'s8'}}}

# prepToJSON(dictTemp, 's0', {'s11'})

# str = "(((AB)|C)[A-Z])+"
# print(preptoCharacterSet(str))
# str = preptoCharacterSet(str)
# print(preptoConcat(str))
# print(postfix(preptoConcat(str)))
