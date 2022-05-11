import json


def prepToTransitions(data):
    transitions = {}
    inputSymbols = []
    for key, value in data.items():
        # print(key, value)
        if(key == "StartingState"):
            startingState = value
        else:

            for iKey, ivalue in value.items():
                temp = {}
                if(iKey != "isTerminatingState"):
                    if(iKey not in inputSymbols and iKey != "Epsilon"):
                        inputSymbols.append(iKey)
                    temp[iKey] = ivalue
                    transitions.update({key: temp})
                else:
                    finalState = key

    print("Final State: ", finalState)
    return transitions, startingState, finalState, inputSymbols


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

    # if(finalFound == False):  # if no final state is found, add final state
    #     for i in finalStates:
    #         jsonTransitions[i] = {"isTerminatingState": True}
    for key, value in transitions.items():
        if(value == {}):
            jsonTransitions.update(
                {key: {"isTerminatingState": (key in finalStates)}})

    # print(jsonTransitions)
    return jsonTransitions


# # JSON file
# f = open('sample.json', "r")

# # Reading from file
# data = json.loads(f.read())
# print(prepToTransitions(data))

# T = {'q0': {'A': {'q1'}, 'C': {'q2'}}, 'q1': {'B': {'q3'}}, 'q2': {
#     'A-Z': {'q4'}}, 'q3': {'A-Z': {'q4'}}, 'q4': {'A': {'q1'}, 'C': {'q2'}}}
# for(key, value) in T.items():
#     count = 0
#     print(key, value)
#     for iKey, ivalue in T.items():
#         if(T[iKey] == T[key] and key != 'q4' and iKey != 'q4'):
#             count += 1
#             if(count > 1 and key != iKey):
#                 delkey = key
#                 duplicate = iKey
#     print(count)
# del T[delkey]
# print(T)

# temp1 = {}
# for key, value in T.items():
#     newkey = duplicate
#     if(key != delkey):
#         for iKey, ivalue in value.items():
#             if(delkey in ivalue):
#                 value[iKey] = {duplicate}
#             temp1.update({key: value})


# print(temp1)
