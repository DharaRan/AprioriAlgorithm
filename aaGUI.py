# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 13:46:38 2018

@author: dhara
"""

from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import AprioriAlgorithmV5 as apriori


def close_window():
    window.destory()
    exit()



def mfileopen():
    # Load Data
    file = fd.askopenfile()
    Filenameoutput.delete(0.0,END)
    Filenameoutput.insert(END,file.name)
    
    #Give Preview of data
    file=Filenameoutput.get("1.0",END)
    file=file.rstrip()
    print(file)
    f = open(file, "r")
    lines = f.readline()
    lines=next(f)
    
    ItemTransactionDic={} #This is how you create a dictionary
    while(lines !=''):
        a=lines.split()
        ItemTransactionDic[a[0]]=a[1:]
        lines=f.readline() 
    f.close()
    
    TransactionListOutput.delete(0.0,END)
    TransactionListOutput.insert(END,"TID:   Transactions")
    TransactionListOutput.insert(END,"\n")
    for key in ItemTransactionDic:
        s= key+ ": "+str(ItemTransactionDic[key])
        TransactionListOutput.insert(END,s)
        TransactionListOutput.insert(END,"\n")
        
def getApriori():
    file=Filenameoutput.get("1.0",END)
    file=file.rstrip()
    print(file)
    f = open(file, "r")
    lines = f.readline()
    lines=next(f)
    
    ItemTransactionDic={} #This is how you create a dictionary
    while(lines !=''):
        a=lines.split()
        ItemTransactionDic[a[0]]=a[1:]
        lines=f.readline() 
    f.close()
    #print(ItemTransactionDic)
    min_support= float(SupportLabelInput.get("1.0",END))
    min_confid= float(ConfidenceLabelInput.get("1.0",END))
    print(type(min_support))
    print(type(min_confid))
    associationsRule=apriori.findAssociationRules(ItemTransactionDic,min_support,min_confid)
    print(associationsRule)
    ApriorOutput.delete(0.0,END)
    ApriorOutput.insert(END,"The minimum support is: "+str(min_support) )
    ApriorOutput.insert(END,"\n")
    ApriorOutput.insert(END,"The minimum confidence is: "+str(min_confid) )
    ApriorOutput.insert(END,"\n\n")
    ApriorOutput.insert(END,"There are "+str(len(associationsRule))+ " association rules:")
    ApriorOutput.insert(END,"\n")
    for a in associationsRule:
        s=str(a[0]) +" --> "  +str(a[1])+ " {"+ str(a[2])+"%,"+ str(a[3])+"%}"
        ApriorOutput.insert(END,s)
        ApriorOutput.insert(END,"\n")
        
        #print(a[0],"-->",a[1],"{",a[2],"%, ",a[3],"%}") 
    
##### main####:
window=Tk()

    
        
window.title("Apriori Algorithm")
window.configure(background="black")
window.geometry("1200x700")
#window.resizable(0, 0)

# Get file from computer and show path being used

titleLabel=ttk.Label(window,text="Apriori Algorithm",foreground="white",background="black")
titleLabel.config(font=("Verdana", 20))
titleLabel.grid(row=0,column=2, padx=10, pady=10)


filename=ttk.Button(window,text="Click Here: Open File", width=30,command=mfileopen)
filename.grid(row=1,column=0,sticky=W, padx=10, pady=10)
Filenameoutput=Text(window, width=50,height=2,wrap=WORD,background="white")
Filenameoutput.grid(row=1,column=1,columnspan=2,sticky=E,pady=10)

SupportLabel=ttk.Label(window,text="Minimum Support (0-1): ",foreground="white",background="black")
SupportLabel.config(font=("Verdana", 12))
SupportLabel.grid(row=2,column=0,columnspan=2,sticky=W,padx=10, pady=10)
SupportLabelInput= Text(window, width=10,height=2,wrap=WORD,background="white")
SupportLabelInput.grid(row=2,column=1,columnspan=2,sticky=W, pady=10)

ConfidenceLabel=ttk.Label(window,text="Minimum Confidence (0-1):  ",foreground="white",background="black")
ConfidenceLabel.config(font=("Verdana", 11))
ConfidenceLabel.grid(row=3,column=0,columnspan=2,sticky=W,padx=10, pady=10)
ConfidenceLabelInput= Text(window, width=10,height=2,wrap=WORD,background="white")
ConfidenceLabelInput.grid(row=3,column=1,columnspan=2,sticky=W,pady=10)



TransactionLabel=ttk.Label(window,text="Transactions: ",foreground="white",background="black")
TransactionLabel.config(font=("Verdana", 12))
TransactionLabel.grid(row=4,column=0,columnspan=2,padx=10, pady=10)

AssociationRuleLabel=ttk.Label(window,text="Association Rules: ",foreground="white",background="black")
AssociationRuleLabel.config(font=("Verdana", 12))
AssociationRuleLabel.grid(row=4,column=10,columnspan=2,padx=10, pady=10)

TransactionListOutput=Text(window, width=50,height=25,wrap=WORD,background="white")
TransactionListOutput.grid(row=10,column=0,columnspan=2,sticky=W,padx=10)


# Run the Aprior Algorithm and show results
ApriorButton=ttk.Button(window,text="Get Association Rules", width=30,command=getApriori)
ApriorButton.grid(row=10,column=2,sticky=W,padx=10)

ApriorOutput=Text(window, width=50,height=25,wrap=WORD,background="white")
ApriorOutput.grid(row=10,column=10,columnspan=2,sticky=E,padx=10)




######tun the main loop
window.mainloop()
