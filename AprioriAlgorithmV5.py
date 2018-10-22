"""
Version 5: Going to convert everything into functions.; 
So we can call only one function to get all association rules
"""

from itertools import combinations, permutations 


def findUniqueItems(ItemTransactionDic):
    #Input: Pass a dictionary with items in it
    #Output: All the unique items in the transaction list; returns a list with strings
    uniqueItems=[]
    for key in ItemTransactionDic:
        for val in ItemTransactionDic[key]: 
          if val in uniqueItems: 
            continue 
          else:
            uniqueItems.append(val)
    return(uniqueItems)

def one_hot_encode(data,uniqueItems):
    # creates one hot encoding for the tranaction list with 0s and 1s
    
    one_hot_encodeArr=[]
    temp=[0]*len(uniqueItems)
    for key in data:
        for item in uniqueItems:
            if item in data[key]: 
                idx=uniqueItems.index(item)
                temp[idx]=1
        one_hot_encodeArr.append(temp)   
        temp=[0]*len(uniqueItems)
    return one_hot_encodeArr

def frequentItemset(support,min_support,comboList):
    # Input: (1) support is a list of suport value for each itemset
    #       (2) min_support: single value set by user
    #       (3) comboList: list of uniqueITems in 
    # outputs: index value
    passItem=[]
    rejectItem=[]
    support_value=[]
    for i in range(0,len(support)):
        if support[i] >= min_support:
            passItem.append(comboList[i])
            support_value.append(support[i])
        else:
        	rejectItem.append(comboList[i])
    return passItem,rejectItem,support_value

def findSupport(combinationList, data):
	#Finds support for all the items
	#Input: (1) CombinationList= type list
	#       (2) data dictionary!
	#Return a list of supports
    total_entries=len(data)
    support=[]
    count=0
    for j in combinationList:
        #print(j)
        for key in data:    
            if set(j).issubset(set(data[key])):
                count=count +1  
        #print(count)
        support.append(count)
        count=0
    support=[j/total_entries for j in support]
    return support

def combos(One_Itemset, c):
    #Input: (1) One_Itemset: is a list of singe frequent items
    #       (2) c is the number of items per set; 2= {pen,bag}, 3= {pen,cookie,candy}, etc
    #Output: returns all the combo as a list
    TotalCombo=combinations(One_Itemset, c) 
    combo=[]
    for i in list(TotalCombo):
        combo.append(i)
        #print(i)    
    
    return combo


"""
Creating the first frequent Itemset or L1
Input: ItemTransactionDic, min_support, 
Output: One_Itemset,ItemRejList,Support_value 

uses the defined functions: findUniqueItems, one_hot_encode and frequentItemset
"""

def getItemsetL1(ItemTransactionDic,min_support):

    total_entries=len(ItemTransactionDic)
    
    """
    Find all unique items in datasets
    """
    uniqueItems= findUniqueItems(ItemTransactionDic)       
        
    """
    Convert each tuple into a one hot encoder
    """
    ohe=one_hot_encode(ItemTransactionDic,uniqueItems)
             
    """
    Find First Frequenct Itemsets
    """
    #Going to sum each column and find Support of each item
    support=[]
    for i in range(0,len(uniqueItems)):
        s=sum([pair[i] for pair in ohe])
        support.append(s)
    support=[j/total_entries for j in support ]
    # Filter by min support and return passing items and rejected items for just single items
    One_Itemset,ItemRejList,Support_value=frequentItemset(support,min_support,uniqueItems)
    #print("\nfor c =", 1)
    #print("Items passed by support: ",One_Itemset)
    #print("Items rejected by support: ",ItemRejList)
    return(One_Itemset,ItemRejList,Support_value)


"""
Rest of the combinations
=> Inputs: One_Itemset,ItemRejList,Support_value
=> Output: Frequent_Itemlist, FreqItemsetSup
"""

def scanNprun(ItemTransactionDic,min_support):

    One_Itemset,ItemRejList,Support_value=getItemsetL1(ItemTransactionDic,min_support)
    maxCombo=len(One_Itemset)
    
    Frequent_Itemlist=[]
    supports_Itemlist=[]
    Frequent_Itemlist.append(One_Itemset)
    supports_Itemlist.append(Support_value)
    
    for c in range(2,maxCombo):
        #find combinations
        #print("\n****for c =", c," ****")
        combo=combos(One_Itemset, c)
        #print("Before combinations are filtered w/ rej: \n",combo)
        #Check if rejected is in combination
        for j in ItemRejList:
            for i in combo:
                if set(j).issubset(set(i)):
                    combo.remove(i)
                    #print(combo)
        #print("After combinations are filtered with Rej: \n",combo)
        # Scan dataset and calculate support
        sup=findSupport(combo, ItemTransactionDic)
        #print("Support value: ",s)
        #Make a list of passing items and reject items
        Pass_Itemset,ItemRejList,Support_value=frequentItemset(sup,min_support,combo)
        #print("Items passed by support: ",Pass_Itemset)
        #print("Items rejected by support: ",ItemRejList)
        Frequent_Itemlist.append(Pass_Itemset)
        supports_Itemlist.append(Support_value)
    
    #modifies the only items from list of string to list of lists!!!
    for i in range(0, len(Frequent_Itemlist[0])):
        Frequent_Itemlist[0][i]=[Frequent_Itemlist[0][i]]
    
    for j in range(1,len(Frequent_Itemlist)):
        for idx in range(0,len(Frequent_Itemlist[j])):
            Frequent_Itemlist[j][idx]=list(Frequent_Itemlist[j][idx])
    
    
    """
    Create a FreqItemsetSup dictionary with frequent Item as key and support as value
    eg. ('cheese', 'juice'): 0.5 etc for items group 2 or greater
    """
    
    mapped=[]
    for i in range(0,len(Frequent_Itemlist)): # note that len of Frequent_Itemlist will equal len(supports_Itemlist) ALWAYSS IF NOT there is a bug
        
        m=list(zip(Frequent_Itemlist[i],supports_Itemlist[i]))
        mapped.append(m)
        
    FreqItemsetSup={}
    for i in range(0,len(mapped)):
        for j in range(0,len(mapped[i])):
                 
            strItem = mapped[i][j][0] # e.g['pen'] or ['cheese', 'milk', 'juice']
            supItem = mapped[i][j][1] # 0.5, or 0.75
            
            if len(strItem) == 1:# have to do this bc single item like tuple(['pen'])= ('cheese',) annoying
                FreqItemsetSup[strItem[0]]=[strItem,supItem]
            else:
                 FreqItemsetSup[tuple(strItem)]=[strItem,supItem]
                 
    return(Frequent_Itemlist, FreqItemsetSup)     

"""
Find confidence and assocoation rule

Input: Frequent_Itemlist,FreqItemsetSup
output: Cleaned AssociationRules
"""
def findAssociationRules(ItemTransactionDic,min_support,min_confid):
    
    Frequent_Itemlist,FreqItemsetSup=scanNprun(ItemTransactionDic,min_support)
    
    AssociationRules=[] # save the rule: Antecedent, consequent, support,confidence
    for i in range(1,len(Frequent_Itemlist)):
        for item in Frequent_Itemlist[i]: # just gets the item eg 'cheese', 'milk', 'juice')
            perm=permutations(item, len(item))
            #print("THis is item: ",item)
           
            #find support; remain same despite change in order; Finding the numaerator of equation
            sup=FreqItemsetSup[tuple(item)][1]*100        
           
            #Step2: find the permuation and find the denominator of equation
            for p in list(perm):#Iterates trhough the permutations
                #print("-----",p,"-----")
                for k in FreqItemsetSup:# iterates to the dictionary of frequent items (1 item, 2 items, 3 item etc and corresponding supports)
                    
                    p=list(p)
                    for v in range(1,len(p)):
                        l=len(p[0:len(p)-v])
                        compareVal=FreqItemsetSup[k][0]
                        #print("\nComparing to K: ", compareVal,len(list(compareVal)))
                        #print("Looking at AR: ",p[0:len(p)-v],"-->",p[-v:], l)      # Note the logically error is in the length of key-pen give 3 instead of 1 smh                 
    
                        if set(p[0:len(p)-v]).issubset(compareVal) and len(compareVal)==l:                       
                            denominator=FreqItemsetSup[k][1]
                            confidence=round(sup/denominator,2)
                            if confidence >= (min_confid*100):
                                antecedent=p[0:len(p)-v]
                                consequent=p[-v:]
                                supportVal=sup             
                                AssociationRules.append([antecedent,consequent,round(supportVal,2),confidence])
                                #print(p[0:len(p)-v],"-->",p[-v:],"{",sup,"%,",confidence,"%}\n")
    
    """
    Clean up: Removing Duplicate Association Rules
    Input: AssociationRules
    output: Cleaned AssociationRules and printing results
    """
    removeIDK=[]
    for a in range(0,len(AssociationRules)):
        for IDK_nextAR in range(a+1,len(AssociationRules)):
            antcdentA=AssociationRules[a][0]
            antcdentNext=AssociationRules[IDK_nextAR][0]
            precdentA=AssociationRules[a][1]
            precdentNext=AssociationRules[IDK_nextAR][1]
            
            # Must check if len of antcendentand precedent of first rule is te same as the next one
            if len(antcdentA)==len(antcdentNext) and len(precdentA)==len(precdentNext):
                if set(antcdentA).issubset(antcdentNext) and set(precdentA).issubset(precdentNext):
                    removeIDK.append(IDK_nextAR)

    AssociationRules = [i for j, i in enumerate(AssociationRules) if j not in removeIDK]
    #for a in AssociationRules:
        #print(a[0],"-->",a[1],"{",a[2],"%, ",a[3],"%}")
        
    return(AssociationRules)
    
    
    




