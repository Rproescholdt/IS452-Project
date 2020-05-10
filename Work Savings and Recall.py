import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def main():
    n, worksavings_abstract = abstractCalc()
    o, recall_fulltext, o2, worksavings_fulltext = fullTextCalc()
    p, recall_included = includedCalc()
    plt.figure(figsize=(10,6), dpi=100)
    plt.plot(o, recall_fulltext, label = "Recall during abstract screening")
    plt.plot(o2, worksavings_fulltext, label = "Work savings during full-text screening")
    plt.plot(n, worksavings_abstract, label = "Work savings during abstract screening")
    plt.plot(p, recall_included, label = "Recall during full-text screening")
    plt.xticks([0, .0001, .001, .01, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1])
    plt.yticks([0,.2,.4,.6,.8, 1])
    plt.xlabel('Prediction Threshold')
    plt.ylabel('Recall and Work Savings')
    plt.title('RCT Work Savings and Recall', fontdict={'fontsize': 20})
    plt.legend()
    plt.show()
    plt.savefig('WorkSavingsPCSK9_RCT_regular.png', dpi = 300)

def abstractCalc():
    # Input abstract screened predictions here:
    abstractScreened = open('Tagger Scores only  - Abstract Screened - PCSK9.txt', 'r')
    abstractScreenedList = abstractScreened.readlines()
    abstractScreened.close()

    numAbstractScreened = 0

# Counter to figure out the total number of predictions; will use for calculations in next step
    for prediction in abstractScreenedList:
        numAbstractScreened = numAbstractScreened + 1
    print("Number of articles abstract screened:", numAbstractScreened, "\n")

    ## Work Savings: Calculate the percent of predictions below each threshold:

    n = [0, .0001, .001, .01, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
    # n holds the list of "thresholds"; we will be calculating the amount of work someone doing this
    # review would have saved if they filtered out all articles with predictions below these numbers
    worksavings_abstract = []
    NumDiscarded = 0
    for threshold in n: #loop through predictions
        for prediction in abstractScreenedList: #loop through list from input file
            if ((eval(prediction.strip()))) <= threshold:
                NumDiscarded = NumDiscarded + 1         # counting up the number that are below the threshold
        workSavings = NumDiscarded / numAbstractScreened # Number below threshold divided total
        # print("Threshold:", threshold)
        # print("Number filtered out:", NumDiscarded)
        # workSavings = NumDiscarded / numAbstractScreened
        worksavings_abstract.append(workSavings)   #making a list of the work savings values at each threshold
        NumDiscarded = 0 #Set NumDiscarded back to zero to get a fresh count for the next prediction
        # print("Work Savings:", workSavings, "\n")
    return n, worksavings_abstract # the values that will be x and y for this line on the graph


def fullTextCalc():
    #Input Full-Text screened predictions here:
    fullText = open('Full-Text Assessed - Predictions only - PCSK9.txt', 'r')
    fullTextList = fullText.readlines()
    fullText.close()

    numFullText = 0

    for prediction in fullTextList:
        numFullText = numFullText + 1
    print("Number of articles full-text screened:", numFullText, "\n")

    ##Recall: Calculate the percent of predictions above each threshold:

    o = [0, .0001, .001, .01, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
    recall_fulltext = []
    NumRetained = 0
    for threshold in o:
        for prediction in fullTextList:
            if ((eval(prediction.strip()))) >= threshold: # Check whether the predictions are above threshold
                NumRetained = NumRetained + 1
        # print("Threshold:", threshold)
        # print("Number retained:", NumRetained)
        Recall = NumRetained / numFullText
        recall_fulltext.append(Recall)
        NumRetained = 0
        # print("Percent recall:", Recall, "\n")
    # print(n)
    # print(recall_full_text)

#This file will be checked for both recall and work savings, since it is the result of filtering
#after abstract screening, and will undergo further filtering after full-text screening.

#This work savings calculation is the same as the previous one for the abstract screened files.

    o2 = [0, .0001, .001, .01, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
    worksavings_fulltext = []
    NumDiscarded = 0
    for threshold in o2:
        for prediction in fullTextList:
            if ((eval(prediction.strip()))) <= threshold:
                NumDiscarded = NumDiscarded + 1
        # ft_worksavings = NumDiscarded / numFullText
        # print("Threshold:", threshold)
        # print("Number filtered out:", NumDiscarded)
        workSavings = NumDiscarded / numFullText
        worksavings_fulltext.append(workSavings)
        NumDiscarded = 0
        # print("Work Savings:", workSavings, "\n")
    return o, recall_fulltext, o2, worksavings_fulltext #2 x's and 2 y's


#Included articles are only checked for recall; they will not be filtered any further, so there
#is no more work savings to calculate

def includedCalc():
    #Input included article predictions here:
    included = open('Included RCT Scores(19).txt', 'r')
    includedList = included.readlines()
    included.close()

    numIncluded = 0

    for prediction in includedList:
        numIncluded = numIncluded + 1
    print("Number of articles included in final review:", numIncluded, "\n")

    ##Recall (the number of predictions above a certain threshold, calculated
    #using full-text assessed and included):

    p = [0, .0001, .001, .01, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
    recall_included = []
    incNumRetained = 0
    for threshold in p:
        for prediction in includedList:
            if ((eval(prediction.strip()))) >= threshold:
                incNumRetained = incNumRetained + 1
        inc_recall = incNumRetained / numIncluded
        # print("Threshold:", threshold)
        # print("Number retained:", incNumRetained)
        Recall = incNumRetained / numIncluded
        recall_included.append(Recall)
        incNumRetained = 0
        # print("Percent recall:", Recall, "\n")
    return p, recall_included

if __name__ == '__main__': main()
