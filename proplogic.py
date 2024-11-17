import sat_interface

def tt2():
    """Propositions: 
    A: Amy is honest
    B: Bob is honest
    C: Cal is truthteller
    
    is truthteller and is honest mean the same"""

    print("Truthtellers and liars 2: \n")
    ttprob=sat_interface.KB(["~A A","~A C","~A ~C A","C B","~B ~C","~C B ~A","~B C","A C"])
    entailed = []
    if ttprob.test_literal("A") == False:
        entailed.append(False)
        print("Amy is a liar")
    if ttprob.test_literal("~A") == False:
        entailed.append(True)
        print("Amy is a truth-teller")
    if ttprob.test_literal("B") == False:
        entailed.append(False)
        print("Bob is a liar")
    if ttprob.test_literal("~B") == False:
        entailed.append(True)
        print("Bob is a truth-teller")
    if ttprob.test_literal("C") == False:
        entailed.append(False)
        print("Cal is a liar")
    if ttprob.test_literal("~C") == False:
        entailed.append(True)
        print("Cal is a truth-teller")
    print("-------------------------")
    output=tuple(entailed)
    return output

def tt3():
    """Propositions:
    A:Amy is a truthteller
    B:Bob is a truthteller
    C:Cal is a truthteller"""
    print("Truthtellers and liars 3: \n")
    ttprob=sat_interface.KB(["C A","~A ~C","~B A","~B C","~A ~C B","~C B","~B C"])
    entailed = []
    if ttprob.test_literal("A") == False:
        entailed.append(False)
        print("Amy is a liar")
    if ttprob.test_literal("~A") == False:
        entailed.append(True)
        print("Amy is a truth-teller")
    if ttprob.test_literal("B") == False:
        entailed.append(False)
        print("Bob is a liar")
    if ttprob.test_literal("~B") == False:
        entailed.append(True)
        print("Bob is a truth-teller")
    if ttprob.test_literal("C") == False:
        entailed.append(False)
        print("Cal is a liar")
    if ttprob.test_literal("~C") == False:
        entailed.append(True)
        print("Cal is a truth-teller")
    print("-------------------------")
    output=tuple(entailed)
    return output

def salt():
    """Propositions:
    C: Caterpillar is honest
    B: Billy the lizard is honest
    CH:Cheshire the cat is honest
    SC: Caterpillar stole the salt
    SB:Billy the Lizard stole the salt
    SCH:Cheshire the cat stole the salt""" 
    print("\nRobbery and salt\n")   
    mydict={}
    #ttprob=sat_interface.KB(["~C ~SB ~SC","~C ~SB ~SCH","~C SC SCH SB","~B ~C ~SC","~B ~C ~SCH","~B SC SCH C","~CH SCH SC SB","~CH ~SCH ~SC","~CH ~SB ~SCH"])
    #ttprob=sat_interface.KB(["C B CH","~C ~B ~CH","SC SB SCH","~SCH ~SC","~SB ~SCH","~C SB","~SB C","~B SB","~SB B","~CH ~SCH","CH SCH","~SB ~SC","~SB ~SCH"])
    ttprob=sat_interface.KB(["~C SB","~SB C","~B C","B ~C","~CH ~SCH","SCH CH","C B CH","~C ~B ~CH","~SC ~SB","~SC ~SCH","~SB ~SCH","SB SCH SC"])
    if ttprob.test_literal("C")==False:
        mydict["Caterpillar is truthful"]='False'
    if ttprob.test_literal("~C")==False:
        mydict["Caterpillar is truthful"]='True'
    if ttprob.test_literal("B")==False:
        mydict["Billy the lizard is truthful"]='False'
    if ttprob.test_literal("~B")==False:
        mydict["Billy The Lizard is truthful"]='True'
    if ttprob.test_literal("CH")==False:
        mydict["Cheshire the cat is truthful"]='False'
    if ttprob.test_literal("~CH")==False:
        mydict["Cheshire the cat is is truthful"]='True'
    if ttprob.test_literal("SC")==False:
        mydict["Caterpillar stole the salt"]='False'
    if ttprob.test_literal("~SC")==False:
        mydict["Caterpillar stole the salt"]='True'
    if ttprob.test_literal("SB")==False:
        mydict["Billy the lizard stole the salt"]='False'
    if ttprob.test_literal("~SB")==False:
        mydict["Billy the lizard stole the salt"]='True'
    if ttprob.test_literal("SCH")==False:
        mydict["Cheshire the cat stole the salt"]="False"
    if ttprob.test_literal("~SCH")==False:
        mydict["Cheshire the cat stole the salt"]='True'

    return mydict

def golf():
    """ Propositions:
    T1: Tom is in the first position
    T2: Tom is in the second position
    T3: Tom is in the third position
    D1: Dick is in the first position
    D2: Dick is in the second position
    D3: Dick is in the third position
    H1: Harry is in the first position
    H2: Harry is in the second position
    H3: Harry is in the third position
    T: Tom is saying truth
    D: Dick is saying truth
    H: Harry is saying truth
    """
    print("\n A honest name \n")
    dict1={}
    ttprob=sat_interface.KB(["~T1 ~T H2","~T1 T ~H2","~D1 ~D H2","~D1 D ~H2","~H1 ~H H2","~H1 H ~H2","~T2 ~T D2","~T2 T ~D2","~D2 ~D D2","~D2 D ~D2","~H2 ~H D2","~H2 H ~D2","~T3 ~T T2","~T3 T ~T2"
                             "~D3 ~D T2","~D3 D ~T2","~H3 ~H T2","~H3 H ~T2","T","~H","~T1 ~T2","~T1 ~T3","~T1 ~H1","~T1 ~D1","T2 T3 H1 D1 T1","~T2 ~T3","~T2 ~H2","~T2 ~D2","T1 T3 H2 D2 T2",
                             "~T3 ~H3","~T3 ~D3","T1 T2 T3 H3 D3","~H1 ~H2","~H1 ~H3","~H1 ~D1","H1 H2 H3 D1 T1","~H2 ~H3","~H2 ~D2","H1 H2 H3 D2 T2","~H3 ~D3","H1 H2 H3 T3 D3","~D1 ~D2","~D1 ~D3"
                             ,"D1 D2 D3 T1 H1","~D2 ~D3","D1 D2 D3 H2 T2","D1 D2 D3 H3 T3"])

    if ttprob.test_literal("T1")==False:
        dict1["Tom is in the first position"]='False'
    if ttprob.test_literal("~T1")==False:
        dict1["Tom is in the first position"]='True'
    if ttprob.test_literal("T2")==False:
        dict1["Tom is in the second position"]='False'
    if ttprob.test_literal("~T2")==False:
        dict1["Tom is in the second position"]='True'
    if ttprob.test_literal("T3")==False:
        dict1["Tom is in the third position"]='False'
    if ttprob.test_literal("~T3")==False:
        dict1["Tom is in the third position"]='True'
    if ttprob.test_literal("D1")==False:
        dict1["Dick is in the first position"]='False'
    if ttprob.test_literal("~D1")==False:
        dict1["Dick is in the first position"]='True'
    if ttprob.test_literal("D2")==False:
        dict1["Dick is in the second position"]='False'
    if ttprob.test_literal("~D2")==False:
        dict1["Dick is in the second position"]='True'
    if ttprob.test_literal("D3")==False:
        dict1["Dick is in the third position"]='False'
    if ttprob.test_literal("~D3")==False:
        dict1["Dick is in the third position"]='True'
    if ttprob.test_literal("H1")==False:
        dict1["Harry is in the first position"]='False'
    if ttprob.test_literal("~H1")==False:
        dict1["Harry is in the first position"]='True'
    if ttprob.test_literal("H2")==False:
        dict1["Harry is in the second position"]='False'
    if ttprob.test_literal("~H2")==False:
        dict1["Harry is in the second position"]='True'
    if ttprob.test_literal("H3")==False:
        dict1["Harry is in the third position"]='False'
    if ttprob.test_literal("~H3")==False:
        dict1["Harry is in the third position"]='True'
    if ttprob.test_literal("T")==False:
        dict1["Tom is a truthteller"]="False"
    if ttprob.test_literal("~T")==False:
        dict1["Tom is a truthteller"]="True"
    if ttprob.test_literal("D")==False:
        dict1["Dick is a truthteller"]="False"
    if ttprob.test_literal("~D")==False:
        dict1["Dick is a truthteller"]="True"
    if ttprob.test_literal("H")==False:
        dict1["Harry is a truthteller"]="False"
    if ttprob.test_literal("~H")==False:
        dict1["Harry is a truthteller"]="True"
    
    return dict1

def main():
    print(tt2())
    print(tt3())
    print(salt())
    print(golf())

if __name__=='__main__':
    main()