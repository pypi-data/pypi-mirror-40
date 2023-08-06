##
## CrowdGO: a wisdom of the crowd based Gene Ontology annotation tool
## Author: MJMF Reijnders
##

import argparse
from collections import defaultdict
import os
import copy
from math import log10
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.externals import joblib

## Function to read the input arguments: -i <input.tab>, -r <rfModel>, -o <output_dir>.
def readArguments():
	parser = argparse.ArgumentParser(description='CrowdGO protein function prediction')
	parser.add_argument('-i','--input',help='Input prediction file. Tab separated. Column 1 = prediction method, column 2 = protein ID, column 3 = GO term prediction ("GO:<number>"), column 4 = confidence interval',required=True,action='store')
	parser.add_argument('-r','--randomforest',help='Input random forest file. Created using CrowdGO_training.py',required=True,action='store')
	parser.add_argument('-o','--outdir',help='Dir for storing the annotations and other produced files',required=True,action='store')
	args = parser.parse_args()
	inputFilePath = args.input
	rfFilePath = args.randomforest
	outDirPath = args.outdir
	return(inputFilePath,rfFilePath,outDirPath)

## Reads the <input.tab> file, returns a dictionary with each GO annotation method as key and a list in a list containing 1 protein, 1 GO, and 1 score for each annotation.
def readInput(inputFilePath):
	infile = open(inputFilePath)
	predictionDictionary = defaultdict(list)
	for line in infile.readlines():
		method,protein,go,score = line.strip().split('\t')
		if not [protein,go,score] in predictionDictionary[method]:
			predictionDictionary[method].append([protein,go,score])
	infile.close()
	return(predictionDictionary)

## Function reading the data/goRelations.tab file. Returns three dictionaries: a dictionary with all the parent GO terms for a GO term, a dictionary with all the child GO terms for a go term, and a dictionary with all the parent and child terms for a GO term (goSlimDic).
def goSlim(crowdGOPath):
    goRelationsFilePath = crowdGOPath+'/data/goRelations.tab'
    infile = open(goRelationsFilePath)
    parentDic = defaultdict(list)
    childDic = defaultdict(list)
    goSlimDic = defaultdict(list)
    for line in infile.readlines():
        goParent,goChild = line.strip().split('\t')
        goSlimDic[goParent].append(goChild)
        goSlimDic[goChild].append(goParent)
        parentDic[goChild].append(goParent)
        childDic[goParent].append(goChild)
    return goSlimDic,parentDic,childDic

## Function reading the data/goCounts.tab file. Returns a dictionary containing the amount of times a GO term is assigned to a protein in the UniProt database (via goCounts.tab), and an integer containing the total amount of GO terms assigned to a protein in the UniProt database.
def getGoCounts(crowdGOPath):
	totalGoCounts = 0
	goCountDic = defaultdict(int)
	infile = open(crowdGOPath+'/data/goCounts.tab')
	for line in infile.readlines():
		go,count = line.strip().split('\t')
		go = 'GO:'+go
		goCountDic[go] = int(count)
		totalGoCounts += int(count)
	return(goCountDic,totalGoCounts)

## Function to retrieve all the name spaces for a GO term: biological process, molecular function, or cellular component. Returns a dictionary with as key the GO term and value the name space.
def getNameSpaces(crowdGOPath):
	nameSpaceDic = defaultdict(str)
	infile = open(crowdGOPath+'/data/nameSpaces.tab')
	for line in infile.readlines():
		go,nameSpace = line.strip().split('\t')
		go = 'GO:'+go
		nameSpaceDic[go] = nameSpace
	return nameSpaceDic

## Function to cluster GO terms from different methods for the same protein. A cluster contains GO terms which are in each others GO Slim (goSlimDic). Returned is the clusterDic which has a protein as key, and a list of list as values. Each list contains the predictions for each method. In the case of an absent prediction for this cluster for one of the methods, that methods 'prediction' is a 'None' value
def createClusters(predictionDictionary,goSlimDic):
	methods = list(predictionDictionary.keys())
	emptyList = [None]*len(methods) ## Create a list the size of the amount of methods used for input predictions
	clusterDic = defaultdict(list)
	for i in range(0,len(methods)): ## Loop over the methods
		method1 = methods[i]
		for predictionMethod1 in predictionDictionary[method1]: ## Loop over the predictions of each method
			protein1,go1,score1 = predictionMethod1 ## Extract the prediction
			clusterList = copy.copy(emptyList)
			clusterList[i] = [method1,go1,score1]
			for k in range(0,len(methods)): ## Do a second loop over the methods
				if not k == i: ## Exclude the same method as is already evaluated in i
					method2 = methods[k]
					for predictionMethod2 in predictionDictionary[method2]:
						protein2,go2,score2 = predictionMethod2 ## Extract the prediction
						if protein2 == protein1: ## If the prediction for method 1 and method 2 is for the same protein, continue
							if go2 in goSlimDic[go1]: ## If the predicted method 2 GO term for this prediction is in the GO slim of the GO term predicted by method 1, continue
								clusterList[k] = [method2,go2,score2] ## Add the prediction to the list at position k
								predictionDictionary[method2].remove(predictionMethod2) ## Remove the prediction from the dictionary to avoid doubles
			clusterDic[protein1].append(clusterList) ## Add the list with predictions to the clusterDic for the protein
		predictionDictionary[method1].remove(predictionMethod1) ## Remove the prediction to avoid doubles
	return(clusterDic)

## Function to calculate the information content for each GO term, aka how informative a GO term is relative to the entire UniProt database
def calculateInformationContent(clusterDic,parentDic,childDic,goCountDic,nameSpaceDic,totGoCounts):
	for protein,clusters in clusterDic.items(): ## For each prediction calculate the IC score
		for cluster in clusters:
			for i in range(0,len(cluster)):
				prediction = cluster[i]
				if not prediction == None:
					method,go,score = prediction
					goCount = goCountDic[go]
					ic = 0
					children = childDic[go]
					for child in children:
						if child in goCountDic:
							goCount += goCountDic[child]
					if goCount == 0:
						goCount = 0.1
					ic = -log10(float(goCount)/totGoCounts) ## IC calculation
					prediction.append(ic) ## Append the IC score to each prediction

## Function to calculate the semantic similarity for each GO term combination in a cluster
def calculateSemanticSimilarity(clusterDic):
	for protein,clusters in clusterDic.items():
		for cluster in clusters:
			representativeTerm = [0,'GO:'] ## List to store the term with the highest IC, to represent the cluster
			for i in range(0,len(cluster)): ## Loop over each prediction in the cluster
				prediction1 = cluster[i]
				if not prediction1 == None and isinstance(prediction1,list): ## Exclude 'None' values
					method1,go1,score1,ic1 = prediction1 ## Extract the prediction
					if ic1 >= representativeTerm[0]: ## If the IC is higher than the current highest IC, make it the highest IC and representative GO term
						representativeTerm[0] = ic1
						representativeTerm[1] = go1
					for k in range(0,len(cluster)): ## Loop over the methods to compare against method[i]
						if not k <= i: ## k has to be greater than i to avoid double comparisons
							prediction2 = cluster[k]
							if not prediction2 == None and isinstance(prediction2,list): ## If the instance in the clusterDic is a list, it is a prediction
								method2,go2,score2,ic2 = prediction2 ## Unpack
								lowestIC = ic1
								if ic2 < ic1: ## Check which IC is the lowest
									lowestIC = ic2
								semanticSim = (2*lowestIC)/(ic1+ic2) ## 2x lowest IC divided by (ic1 + ic2) = semantic similarity
								cluster.append(semanticSim)## Append the semantic similarity to the back of the cluster list
							else:
								cluster.append(None) ## If the prediction doesn't exist, semantic similarity = None
				else:
					cluster.append(None) ## If the cluster doesn't exist, semantic similarity = None
			cluster.append(representativeTerm[1]) ## Add the representative GO term
			cluster.append(representativeTerm[0]) ## Add the IC for the representative GO term

## Function to write the predictions to a file format usable for the random forest step. None values are converted to 0's. See the 'tmp' folder
def writePredictions(clusterDic,predictionDictionary,outDirPath):
	header = 'Count,Protein,GO,Information content,Cluster count'
	header_abstract = 'Information content,Cluster count'
	methods = list(predictionDictionary.keys())
	print(outDirPath)
	if not os.path.isdir(outDirPath):
		os.makedirs(outDirPath)
	outfile1 = open(outDirPath+'/randomForestInput.tab','w') ## Contains the full predictions
	outfile2 = open(outDirPath+'/randomForestInput_abstract.tab','w') ## Contains the 'abstract' predictions, used for the random forest algorithm
	for method in methods:
		header += ','+method+' GO,'+method+' score,'+method+' information content'
		header_abstract += ','+method+' score,'+method+' information content'
	for i in range(0,len(methods)):
		method1 = methods[i]
		for k in range(0,len(methods)):
			if not k <= i:
				method2 = methods[k]
				header += ','+method1+'_'+method2+' semantic similarity'
				header_abstract += ','+method1+'_'+method2+' semantic similarity'
	outfile1.write(header)
	#outfile3.write(header_abstract)
	count = 1
	for protein,clusters in clusterDic.items():
		for cluster in clusters:
			representativeGO = cluster[-2]
			representativeIC = cluster[-1]
			clusterCount = 0
			for part in cluster:
				if isinstance(part,list):
					clusterCount += 1
			row = '\n'+str(count)+','+protein+','+representativeGO+','+str(representativeIC)+','+str(clusterCount)
			row_abstract = str(representativeIC)+','+str(clusterCount)
			for i in range(0,len(methods)):
				prediction = cluster[i]
				if prediction == None:
					row += ',0,0,0'
					row_abstract += ',0,0'
				else:
					row += ','+prediction[1]+','+str(prediction[2])+','+str(prediction[3])
					row_abstract += ','+str(prediction[2])+','+str(prediction[3])
			for i in range(3,len(methods)+3):
				semanticSim = cluster[-i]
				if semanticSim == None:
					semanticSim = '0'
				row += ','+semanticSim
				row_abstract += ','+semanticSim
			outfile1.write(row)
			outfile2.write(row_abstract+'\n')
	outfile1.close()
	outfile2.close()

## Function to execute the random forest algorithm. Imports an RF model created by CrowdGO_training.py
def randomForest(rfFilePath,outDirPath):
	predictionsFile_abstract = pd.read_csv(outDirPath+'/randomForestInput_abstract.tab',header=None) ## Read the abstract predictions
	predictionsFile = open(outDirPath+'/randomForestInput.tab') ## Read the full predictions
	randomForestTrained = joblib.load(rfFilePath) ## Load the random forest model
	predictions = randomForestTrained.predict_proba(predictionsFile_abstract) ## Apply the random forest model to the predictions
	count = 0
	outFileRaw = open(outDirPath+'/annotations.raw.csv','w') ## Write the raw annotations to the temporary folder
	outfile = open(outDirPath+'/annotations.csv','w') ## Write the predictions to the user supplied outfile path
	outFileRaw.write(predictionsFile.readline().strip()+',pred')
	outfile.write('Protein,GO term,Score')
	for line in predictionsFile.readlines():
		ssline = line.strip().split(',')
		protein = ssline[1]
		go = ssline[2]
		score = predictions[count][1]
		outFileRaw.write('\n'+line.strip()+','+str(score))
		outfile.write('\n'+protein+','+go+','+str(score))
		count += 1
	outfile.close()
	outFileRaw.close()

crowdGOPath = os.path.dirname(os.path.abspath(__file__))
inputFilePath,rfFilePath,outDirPath = readArguments()
predictionDictionary = readInput(inputFilePath)
goSlimDic,parentDic,childDic = goSlim(crowdGOPath)
goCountDic,totGoCounts = getGoCounts(crowdGOPath)
nameSpaceDic = getNameSpaces(crowdGOPath)
clusterDic = createClusters(predictionDictionary,goSlimDic)
calculateInformationContent(clusterDic,parentDic,childDic,goCountDic,nameSpaceDic,totGoCounts)
calculateSemanticSimilarity(clusterDic)
writePredictions(clusterDic,predictionDictionary,outDirPath)
randomForest(rfFilePath,outDirPath)
