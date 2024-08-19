from treelib import Node, Tree
import codecs

class myNode:
    PC = None
    StatesRem = {}
    PCList = []
    Requirements = []

def removeCoveredRequirements(leaf, RequirementPCList):
    #Is it null leaf?
    if (leaf.PC is not None):
        #not null state
        if len(leaf.Requirements) != 0: #does it have any requirements?
            #it has requirement(s)
            #given each requirement, check if its met
            for leafReq in leaf.Requirements.copy():
                #given this requirement, check if its met by chain
                coveredReq = False #initialize each requirement as not covered
                #check if requirement is null
                if len(leafReq) != 0:
                    #requirement is not null
                    #check if any leaf PC or its subchain meets the requirement
                    PCListIterate = leaf.PCList.copy()
                    PCListIterate.append(leaf.PC)
                    for PC in (leaf.PCList.copy())+[leaf.PC]:
                        #print(f"Check PC:{PC} vs Reqs:{RequirementPCList[listToString(leafReq)].copy()}")
                        #for ReqPC in RequirementPCList[listToString(leafReq)].copy():
                            #print(f"Parse out a requirement{ReqPC}")
                            #if (listToString(PC) == listToString(ReqPC)):
                                #print(f"PC:{PC} and ReqPC:{ReqPC} are the same")
                        if not coveredReq:
                            #requirement not met yet, so check if next PC in chain meets the requirement
                            coveredReq = any(listToString(PC) == listToString(ReqPC) for ReqPC in RequirementPCList[listToString(leafReq)].copy())
                        else:
                            #a PC in the chain met the requirement, no need to check rest of chain
                            break
                else:
                    #requirement is null, so it is met
                    coveredReq = True
                if coveredReq:
                    #requirement is met, so remove it
                    #print("Printing requirement to remove",leafReq)
                    leaf.Requirements.remove(leafReq)
        #else it has no requirements
    #else is null state, null state can't have requirements

def branchARequirement(leaf, RequirementPCs, PCRequirements, new_leaves, tree, mode, labelType, ClosedCoverPCList, foundCount):
    aClosedFound = False
    closedCoverCount = 0
    if(len(leaf.Requirements) != 0):
        branched = True
        ReqCopy = leaf.Requirements.copy()
        leafReq = ReqCopy[0]
        for newPC in RequirementPCs[listToString(leafReq)].copy():
            #Any requirement that would be met by a PC in chain has been pruned
            #So all PCs that meet requirement need to branched to
            ReqCarryOver = ReqCopy.copy()
            #print(ReqCarryOver)
            #print("Printing PC Reqs\n", PCRequirements)
            ReqCarryOver.extend(PCRequirements[listToString(newPC)].copy())
            ReqCarryOver.remove(leafReq)
            statesCarryOver = leaf.StatesRem.copy()
            for state in statesCarryOver.copy():
                if state in newPC:
                   del statesCarryOver[state]
            PCListCarryOver = leaf.PCList.copy()
            PCListCarryOver.append(leaf.PC)
            nleaf = myNode()
            nleaf.PC = newPC
            nleaf.Requirements = ReqCarryOver.copy()
            nleaf.StatesRem = statesCarryOver.copy()
            nleaf.PCList = PCListCarryOver.copy()
            removeCoveredRequirements(nleaf, RequirementPCs)
            new_leaves.append(nleaf)
            if len(leaf.PCList) == 0:
                tree.create_node(listToString(newPC), listToString(leaf.PC)+"."+listToString(newPC), parent = listToString(leaf.PC))
            else:
                joined = ""
                if len(leaf.PCList) != 1:
                    for item in leaf.PCList.copy():
                        joined += listToString(item)
                        joined += "."
                else:
                    joined = listToString(leaf.PCList[0])
                    joined += "."
                tree.create_node(listToString(newPC), joined+listToString(leaf.PC)+"."+listToString(newPC), parent = joined+listToString(leaf.PC))
                #tree.create_node(PC, joined+leaf.PC+"."+PC, parent = joined+leaf.PC)
            if leaf.PC is None:
                print("From root, branching to", listToString(newPC))
                raise Exception("Something is wrong, root/null state should have zero requirements, therefore never branch")
            elif len(leaf.PCList) == 0:
                print("Req Branch(",listToString(leafReq),"): ", listToString(leaf.PC), "->", listToString(newPC))
                #print(leaf.PC+"."+newPC)

            else:
                print("Req Branch(",listToString(leafReq),"): ", joined+listToString(leaf.PC), "->", listToString(newPC))
                #print(joined+leaf.PC+"."+newPC)
            print(f'New PC:{newPC}, has requirements: {nleaf.Requirements}')
            closedFound = isClosedCover(nleaf, ClosedCoverPCList, tree, labelType, foundCount+closedCoverCount)
            if (closedFound):
                closedCoverCount += 1
                aClosedFound = True
                if (mode == 1):
                    break
            
    else:
        branched = False
    return branched, aClosedFound, closedCoverCount


def to_graphviz(self, filename=None, shape='circle', graph='digraph'):
        """Exports the tree in the dot format of the graphviz software"""
        nodes, connections = [], []
        if self.nodes:

            for n in self.expand_tree(mode=self.WIDTH):
                nid = self[n].identifier
                if ("*" in nid):
                    state = '"{0}" [label="{1}", shape={2}, color="green"]'.format(
                        nid, self[n].tag, shape)
                else:
                    state = '"{0}" [label="{1}", shape={2}]'.format(
                        nid, self[n].tag, shape)
                nodes.append(state)

                for c in self.children(nid):
                    cid = c.identifier
                    connections.append('"{0}" -> "{1}"'.format(nid, cid))

        # write nodes and connections to dot format
        is_plain_file = filename is not None
        if is_plain_file:
            f = codecs.open(filename, 'w', 'utf-8')
        else:
            f = StringIO()

        f.write(graph + ' tree {\n\tsplines=polyline\n\tordering=out\n')
        for n in nodes:
            f.write('\t' + n + '\n')

        if len(connections) > 0:
            f.write('\n')

        for c in connections:
            f.write('\t' + c + '\n')

        f.write('}')

        if not is_plain_file:
            print(f.getvalue())

        f.close()

def listToString(alist):
    myString = ""
    if (len(alist) != 0):
        for item in alist:
            myString = myString + item + ','
        myString = myString[:-1]
    return myString
        
        

def convertPrimeCompatiblesDict(prime_compatibles):
    new_prime_compatibles = {}
    for key, value in prime_compatibles.items():
        PC = ""
        ReqList = []
        
        for char in key:
            if (char != ","):
                PC = PC+char
        for req in value:
            combinedReq = ""
            for state in req:
                combinedReq = combinedReq+state
            ReqList.append(combinedReq)
        new_prime_compatibles[PC] = ReqList
    return new_prime_compatibles

def stateToPrimeCompatiblesDict(state_list, prime_compatibles):
    state_prime_compatibles = {}
    for state in state_list:
        tempStatePCList = []
        for PC in prime_compatibles:
            PC = PC.split(",") #get list 
            if state in PC:
                tempStatePCList.append(PC)
        state_prime_compatibles[state] = tempStatePCList
    return state_prime_compatibles

#gets all PCs that meet the particular requirement. In the form key = req, value = PCs
def requirementToPrimeCompatiblesDict(prime_compatibles):
    #make a list of compatibles without duplicates or empty
    requirements = []
    
    #collapses 2d array into 1d array of strings and excludes empty lists
    for req_list in (list(prime_compatibles.values())):
        if len(req_list) != 0:
            for req in req_list:
                if req not in requirements:
                    requirements.append(req)
    
    #using list of requirements, create dict with requirement as key to access
    #list of prime compatibles that meet it
    requirement_prime_compatibles = {}
    for req in requirements:
        tempPCList = []
        for PC in list(prime_compatibles.keys()):
            if all(state in PC for state in req): #if req is in PC
                PC = PC.replace("[", "")
                PC = PC.replace("]", "")
                PC = PC.replace(" ", "")
                PC = PC.split(",")
                tempPCList.append(PC)
        requirement_prime_compatibles[listToString(req)] = tempPCList
    return requirement_prime_compatibles
    


def meisel(state_list, prime_compatibles):
    print("\nMinimizing with Meisel's Method...")

    print('State Frequencies:')
    #Determine state frequencies by...
    
    #Create dict that takes in a state as a key and returns the number
    #of times that state appears in the list of prime compatibles
    state_frequency = {}
    for state in state_list:
        count = 0
        for key in prime_compatibles:
            pc_states = key.split(',')
            if state in pc_states:
                count += 1
        state_frequency[state] = count
        print(f'{state}: {count}')


    #Joining states in PCs, aka prior key = "a,b,e", new key = "abe"
    #prime_compatibles = convertPrimeCompatiblesDict(prime_compatibles)
    print("\nPrinting Dictionary of PC to CS")
    for k, v in prime_compatibles.items():
        print(f'{k}:{v}')

    #Create dict that takes in a state as a key
    #and returns list of prime compatibles with that state
    state_prime_compatibles = stateToPrimeCompatiblesDict(state_list, prime_compatibles)
    print("\nPrinting all states")
    for s in state_list:
        print(s)
    print("\nPrinting Dictionary of State to PC")
    for k, v in state_prime_compatibles.items():
        print(f'{k}:{v}')

    #Create dict that takes in a requirement as a key
    #and returns list of prime compatibles that meet that requirement
    requirement_prime_compatibles = requirementToPrimeCompatiblesDict(prime_compatibles)
    print("\nPrinting Dictionary of Requirement to PC")
    for k, v in requirement_prime_compatibles.items():
        print(f'{k}:{v}')

    #Modifiers for different modes on type of search for closed covers.
    mode = 1 #selects the mode on how exhaustively to search for closed covers
    levelLimit = 1 #control up to what level leafs are explored in. Only works in mode = 3
    labelType = 'stars' #How to label the node that indicates the end of a chain
    
    #mode= 0:explore every leaf to the fullest
    #mode= 1:find 1st closed cover
    #mode= 2:if closed cover found, explore all on the same level
    #mode= 3:go up to level as defined in levelLimit. Note: null is level 0
    #labelType = 'stars': all chains that close are labeled with '*'
    #labelType = 'number': all chains that close are labeled with a number, which increases for each found closed cover

    if (mode == 0):
        print("\nSearching through each branch for closed covers\n")
    elif (mode == 1):
        print("\nSearching for the first closed cover\n")
    elif (mode == 2):
        print("\nSearch for first closed cover and all on the same level that the first closed cover is found\n")
    elif (mode == 3):
        print(f"\nSearching for closed covers down to level {levelLimit}\n")

    #Find closed covers based on the mode options selected
    closed_cover_prime_compatibles = meisel_search(state_frequency,
                                                   prime_compatibles,
                                                   state_prime_compatibles,
                                                   requirement_prime_compatibles
                                                   ,mode, levelLimit, labelType)

    if (len(closed_cover_prime_compatibles) == 0):
        print("\nNo closed covers were found")
    else:
        print()
        for CCList in closed_cover_prime_compatibles:
            print("Closed Cover PCs:", CCList)
        print("\nNumber of closed covers found:", len(closed_cover_prime_compatibles))
    return closed_cover_prime_compatibles

def isClosedCover(leaf, ClosedCoverPCList, tree, labelType, foundCount):
    if (len(leaf.Requirements) == 0 and len(leaf.StatesRem) == 0):
        ClosedCoverPCList.append(leaf.PCList.copy())
        ClosedCoverPCList[-1].append(leaf.PC)
        joined = ""
        if (labelType == 'stars'):
            label = '*'
        elif (labelType == 'number'):
            label = str(foundCount+1)
        else:
            label = '*'
        if len(leaf.PCList) == 0:
            tree.create_node(label, "*."+str(foundCount+1), parent = listToString(leaf.PC))
        else:
            if len(leaf.PCList) != 1:
                for item in leaf.PCList.copy():
                    joined += listToString(item)
                    joined += "."
            else:
                joined += listToString(leaf.PCList[0])
                joined += "."
            tree.create_node(label, "*."+str(foundCount+1), parent = joined+listToString(leaf.PC))
        return True
    else:
        return False

def branchAState(leaf, nleaves, statePCs, PCReqs, ReqPCs, tree, mode, labelType, ClosedCoverPCList, foundCount):
    aClosedFound = False
    closedCoverCount = 0
    if(len(leaf.StatesRem) != 0):
        branched = True
        minimumValue = None
        lowFreqState = None
        for k, v in leaf.StatesRem.items():
            if (minimumValue is None):
                minimumValue = v
                lowFreqState = k
            elif (minimumValue > v):
                minimumValue = v
                lowFreqState = k
        PCList = statePCs[lowFreqState].copy()
        for PC in PCList.copy():
            if leaf.PC is None:
                print("Initial State Branch(",lowFreqState,"): ", listToString(PC))
            elif len(leaf.PCList) == 0:
                print("State Branch(",lowFreqState,"): ", listToString(leaf.PC), "->", listToString(PC))
            else:
                leafPCListStr = ""
                for leafPC in leaf.PCList.copy():
                    leafPCListStr = leafPCListStr+listToString(leafPC)+"."
                print("State Branch(",lowFreqState,"): ", leafPCListStr+listToString(leaf.PC),"->", listToString(PC))
            PCListCarryOver = leaf.PCList.copy()
            if (leaf.PC is not None):
                PCListCarryOver.append(leaf.PC)
            ReqCarryOver = leaf.Requirements.copy()
            ReqCarryOver.extend(PCReqs[listToString(PC)])
            #print("PC:", PC, "\nPC String:", listToString(PC))
            #print("\nleaf reqs extended", ReqCarryOver)
            statesCarryOver = leaf.StatesRem.copy()
            #print("States that remain in current State", leaf.StatesRem.copy())
            for state in statesCarryOver.copy():
                if state in PC:
                   del statesCarryOver[state]
            nleaf = myNode()
            nleaf.PC = PC
            nleaf.Requirements = ReqCarryOver.copy()
            nleaf.StatesRem = statesCarryOver.copy()
            nleaf.PCList = PCListCarryOver.copy()
            removeCoveredRequirements(nleaf, ReqPCs)
            nleaves.append(nleaf)
            print(f'New PC:{PC}, has requirements: {nleaf.Requirements}')
            #Uncomment to print out what it looks like on the tree node
            if leaf.PC is None:
                tree.create_node(listToString(PC), listToString(PC), parent = "null")
                #print(listToString(PC))
            elif len(leaf.PCList) == 0:
                tree.create_node(listToString(PC), listToString(leaf.PC)+"."+listToString(PC), parent = listToString(leaf.PC))
                #print(listToString(leaf.PC)+"."+listToString(PC))
            else:
                joined = ""
                if len(leaf.PCList) != 1:
                    for item in leaf.PCList.copy():
                        joined += listToString(item)
                        joined += "."
                else:
                    joined = listToString(leaf.PCList[0])
                    joined += "."
                #print(joined+listToString(leaf.PC)+"."+listToString(PC))
                tree.create_node(listToString(PC), joined+listToString(leaf.PC)+"."+listToString(PC), parent = joined+listToString(leaf.PC))
            #print("States that are carrying over", statesCarryOver.copy())

            
            closedFound = isClosedCover(nleaf, ClosedCoverPCList, tree, labelType, foundCount+closedCoverCount)
            if (closedFound):
                closedCoverCount += 1
                aClosedFound = True
                if (mode == 1):
                    break
    else:
        branched = False
    return branched, aClosedFound, closedCoverCount

def meisel_search(state_frequency, PCReqs, statePCs,
                  ReqPCs, mode, levelLimit, labelType):

    #INIT
    root = myNode()
    root.StatesRem = state_frequency
    leaves = [root]
    nleaves = []
    foundAClosed = False #whether a closed cover has been found in a list of leaves
    foundClosed = False #whether a closed cover has been found in a branch
    tree = Tree()
    tree.create_node("Null", "null") #root
    
    foundCount = 0 #number of closed covers found
    ClosedCoverPCList = [] #list of closed covers found
    level = 0 #Current tree level that search is occuring in.
    
    while(len(leaves) != 0):
        foundAClosed = False
        for leaf in leaves.copy():
            removeCoveredRequirements(leaf, ReqPCs)
            branched, foundClosed, CCcount = branchARequirement(leaf,ReqPCs, PCReqs, nleaves, tree, mode, labelType, ClosedCoverPCList, foundCount)
            foundCount += CCcount
            if (mode == 1 and foundClosed):
                break
            if (not branched):
                branched, foundClosed, CCcount = branchAState(leaf, nleaves, statePCs, PCReqs, ReqPCs, tree, mode, labelType, ClosedCoverPCList, foundCount)
                foundCount += CCcount
                if (mode == 1 and foundClosed):
                    break
            if (foundClosed and not foundAClosed):
                foundAClosed = True
        if (mode == 1 and (foundClosed or foundAClosed)):
            leaves = []
            nleaves = []
            break
        if (mode == 2 and foundAClosed):
            leaves = []
            nleaves = []
        else:
            leaves = nleaves
            nleaves = []
        level += 1
        if (level >= levelLimit and mode == 3):
            leaves = []
            nleaves = []
            break
    to_graphviz(tree, 'meiseltree.gv','circle', 'digraph') #generate graphviz formatted file
    tree.save2file('meiseltree.txt') #save text file of the tree, not required
    return ClosedCoverPCList
