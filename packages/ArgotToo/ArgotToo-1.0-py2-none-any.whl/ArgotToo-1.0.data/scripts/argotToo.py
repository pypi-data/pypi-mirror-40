##
## ArgotToo - based Falda, Marco, et al. "Argot2: a large scale function prediction tool relying on semantic similarity of weighted Gene Ontology terms." BMC bioinformatics 13.4 (2012): S14.
##
## Author: MJMF Reijnders
##

import sys
from collections import defaultdict
from math import log
from math import log10
import numpy

## Function to read in the BLAST file provided by the user
def readBlast(blastFilePath):
	protGoDicBLAST = defaultdict(dict) ## Dictionary in a dictionary, holding for each [protein] and [goTerm] the sseqid, qseqid, and weight for each BLAST hit
	sseqList = []
	protToGoDic = defaultdict(list)

	for line in open(blastFilePath): ## Initial iteration over the BLAST file to gaather all sseqids
		ssline = line.strip().split('\t')
		sseqId = ssline[1]
		sseqIdIdentifier = sseqId.split('|')[-1].split('_')[0]
		sseqList.append(sseqIdIdentifier)
	sseqSet = set(sseqList)
	
	print('Matching BLAST to GOA')
	for line in open('data/goaPfam.tab'): ## Gather all GO terms related to all sseqids
		ssline = line.strip().split('\t')
		prot = ssline[0]
		if prot in sseqSet:
			for goTerm in ssline[1::]:
				if goTerm.startswith('GO:'):
					protToGoDic[prot].append(goTerm)
			sseqSet.remove(prot)

	for line in open(blastFilePath): ## For each protein, add a dictionary for each GO term it has a hit to, with the corresponding BLAST hit(s)
		protGoDicBLAST = defaultdict(dict)
		ssline = line.strip().split('\t')
		qseqId = ssline[0]
		sseqId = ssline[1]
		sseqIdIdentifier = sseqId.split('|')[-1].split('_')[0]
		evalue = float(ssline[2])
		goList = protToGoDic[sseqIdIdentifier]
		for go in goList:
			if evalue == 0.0:
				evalue = 1e250
			weight = abs(-log(evalue)) ## Weight = -log(evalue)
			if not go == '':
				protGoDicBLAST[qseqId].setdefault(go,[]).append([sseqId,evalue,weight])

	return(protGoDicBLAST)

## Function to read in the HMMScan file provided by the user
def readHMMER(hmmerFilePath):
	print('Matching HMMER to GOA')
	pfam2GoDic = readPfam2Go()
	protGoDicHMMER = defaultdict(dict)
	pfamDic = defaultdict(int)
	pfamProtCountDic = {}
	count = 0

	for line in open(hmmerFilePath): ## Initial iteration over the HMMScan input file to gather all Pfam ID's
		ssline = line.strip().split('\t')
		pfamID = ssline[1].split('.')[0]
		pfamDic[pfamID] = []
		pfamProtCountDic[pfamID] = 0
		count += 1

	print 'Gathering the GO terms of all proteins related to a Pfam model. This will take a few minutes'
	for line in open('data/goaPfam.tab'): ## Iterate over the goaPfam.tab file to gather all the GO terms of all proteins related to the Pfam ID's
		ssline = line.strip().split('\t')
		goList = []
		for part in ssline[1::]:
			if not part.startswith('GO:'):
				pfamID = part
				if pfamID in pfamDic:
					for go in goList:
						pfamDic[pfamID+'~~'+go] += 1
					pfamProtCountDic[pfamID] += 1
			elif part.startswith('GO:'):
				goList.append(part)

	count = 0
	print(len(pfamDic))
	for key,counts in pfamDic.items(): ## Remove all GO terms related to a Pfam entry, enriched through the GOA entries, if the GO term belongs to less than a third of all proteins related to the Pfam model
		pfamID = key.split('~~')[0]
		protCount = pfamProtCountDic[pfamID]
		cutoff = protCount/3
		if counts < cutoff:
			pfamDic.pop(key)

	for line in open(hmmerFilePath): ## Fill a dictionary with a dictionary, with [qseqid] and [goTerm], with each HMMScan hit related to the protein and GO term
		ssline = line.strip().split('\t')
		qseqId = ssline[0]
		pfamID = ssline[1].split('.')[0]
		evalue = float(ssline[2])
		if evalue < 1e250:
			evalue = 1e250
		goList = pfam2GoDic[pfamID]
		if not goList == []:
			weight = abs(-log(evalue)) ## Weight = -log(evalue)
			for go in goList:
				protGoDicHMMER[qseqId].setdefault(go,[]).append([pfamID,evalue,weight])
		for go in set(pfamDic[pfamID]):
			protCount = pfamProtCountDic[pfamID]
			goCount = pfamDic[pfamID +'~~'+go]
			weight = weight*(goCount/protCount) ## Pfam hit weights are multiplied by (goCount/protCount) to compensate for the enrichment of GO terms for each Pfam hit
			protGoDicHMMER[qseqId].setdefault(go,[]).append([pfamID,evalue,weight])
		
	return(protGoDicHMMER)

## Function to merge all annotations from BLAST and HMMScan
def mergeAnnotations(protGoDicBLAST,protGoDicHMMER):
	print('Merging BLAST and HMMER annotations')
	protGoDic = defaultdict(dict)

	for prot,values in protGoDicBLAST.items(): ## For each protein, go term in the blast dictionary, merge the weights. Add the weights of the HMMScan dic if it has the same protein, go term pair
		for goTerm in values:
			totalWeight = 0
			hmmerHits = []
			blastHits = protGoDicBLAST[prot][goTerm]
			for sseqId in protGoDicBLAST[prot][goTerm]:
				weight = float(sseqId[-1])
				totalWeight += weight
			if prot in protGoDicHMMER:
				if goTerm in protGoDicHMMER[prot]:
					for sseqId in protGoDicHMMER[prot][goTerm]:
						weight = sseqId[-1]
						totalWeight += weight
					hmmerHits = protGoDicHMMER[prot][goTerm]
			protGoDic[prot].setdefault(goTerm,[]).append(totalWeight)
			protGoDic[prot].setdefault(goTerm,[]).append(blastHits)
			protGoDic[prot].setdefault(goTerm,[]).append(hmmerHits)

	for prot,values in protGoDicHMMER.items(): ## For the remaining protein, go term pairs in the HMMScan dic, merge the weights for all hits for the protein, go term pair
		for goTerm in values:
			if not goTerm in protGoDic[prot]:
				totalWeight = 0
				hmmerHits = protGoDicHMMER[prot][goTerm]
				blastHits = []
				for sseqId in protGoDicHMMER[prot][goTerm]:
					weight = float(sseqId[-1])
					totalWeight += weight
				protGoDic[prot].setdefault(goTerm,[]).append(totalWeight)
				protGoDic[prot].setdefault(goTerm,[]).append(blastHits)
				protGoDic[prot].setdefault(goTerm,[]).append(hmmerHits)
	return(protGoDic)

## Function to retrieve the merged weights for all protein, go term pairs, and uppropagate the weights up the GO hierarchy
def getGoWeightDic(protGoDic,parentsDic,rootNodeDic):
	weightDic = defaultdict(dict)
	for prot,goTerms in protGoDic.items():
		for goTerm in goTerms:
			totalWeight = protGoDic[prot][goTerm][0]
			rootNode = rootNodeDic[goTerm]
			if not rootNode in weightDic[prot]:
				weightDic[prot][rootNode] = totalWeight
			else:
				weightDic[prot][rootNode] += totalWeight
			weightDic[prot][goTerm] = totalWeight
			for parent in parentsDic[goTerm]:
				if not parent in weightDic[prot]:
					weightDic[prot][parent] = totalWeight
				else:
					weightDic[prot][parent] += totalWeight
	return(weightDic)

## Function which read the pfam 2 go into a dictionary
def readPfam2Go():
	pfam2GoDic = defaultdict(list)
	for line in open('data/pfam2go'):
		if not line.startswith('!'):
			ssline = line.strip().split(' ')
			pfamID = ssline[1]
			go = ssline[-1]
			pfam2GoDic[pfamID].append(go)
	return(pfam2GoDic)

## Function which retrieves the GO slim, go parents, and go children into dictionaries
def getGoSlim():
	childrenDic = defaultdict(list)
	parentsDic = defaultdict(list)
	goSlimDic = defaultdict(list)
	for line in open('data/goRelations.tab'):
		ssline = line.strip().split('\t')
		child = ssline[0]
		parent = ssline[1]
		if not child == parent:
			childrenDic[parent].append(child)
			parentsDic[child].append(parent)
			goSlimDic[child].append(parent)
			goSlimDic[parent].append(child)
	return(childrenDic,parentsDic,goSlimDic)

## Function to calculate the semantic similarity between two GO terms
def getSemanticSimilarity(goTerm1,goTerm2,parentsDic,rootNodeDic,childrenDic,goCountsDic):
	goTerm1Ic = getIcScore(goTerm1,goCountsDic,rootNodeDic,childrenDic)
	goTerm2Ic = getIcScore(goTerm2,goCountsDic,rootNodeDic,childrenDic)
	goTerm1Parents = parentsDic[goTerm1]
	goTerm2Parents = parentsDic[goTerm2]
	commonParents = [val for val in goTerm1Parents if val in goTerm2Parents] 
	highestIc = 0
	highestIcTerm = ''
	for parent in commonParents:
		parentIc = getIcScore(parent,goCountsDic,rootNodeDic,childrenDic)
		if parentIc > highestIc:
			highestIc = parentIc
			highestIcTerm = parent
	if goTerm1 in goTerm2Parents:
		if goTerm1Ic > highestIc:
			highestIcTerm = goTerm1
			highestIc = goTerm1Ic
	elif goTerm2 in goTerm1Parents:
		if goTerm2Ic > highestIc:
			highestIcTerm = goTerm2
			highestIc = goTerm2Ic
	semanticSim = (2*highestIc)/(goTerm1Ic+goTerm2Ic) ## Semantic similarity formula
	return(semanticSim)

## Function to create the groups and their weights
def getGroupScores(incDic,parentsDic,rootNodeDic,childrenDic,goCountsDic):
	print('Getting group scores')
	groupScoreDic = defaultdict(dict)
	groupScoreNcDic = defaultdict(dict)
	for prot,values in incDic.items():
		for go in values:
			incScore = incDic[prot][go]
			incScore = float(incScore)
			groupScoreDic[prot].setdefault(go,0)
			groupScoreDic[prot][go] += incScore
			groupScoreNcDic[prot].setdefault(go,0)
			groupScoreNcDic[prot][go] += incScore
			goParents = parentsDic[go]
			for goParent in goParents:
				semanticSimilarity = getSemanticSimilarity(go,goParent,parentsDic,rootNodeDic,childrenDic,goCountsDic)
				if semanticSimilarity >= 0.7: ## GO parents are only considered if they have >= 0.7 similarity with the predicted GO term
					groupScoreDic[prot].setdefault(goParent,0)
					groupScoreDic[prot][goParent] += incScore

	return(groupScoreDic,groupScoreNcDic)

## Function to create a dictionary with the root node for each GO term
def getRootNodes():
	rootNodeDic = {}
	for line in open('data/nameSpaces.tab'):
		ssline = line.strip().split('\t')
		go = ssline[0]
		rootNode = ssline[1]
		if rootNode == 'biological_process':
			rootNodeDic[go] = 'GO:0008150'
		elif rootNode == 'molecular_function':
			rootNodeDic[go] = 'GO:0003674'
		elif rootNode == 'cellular_component':
			rootNodeDic[go] = 'GO:0005575'
		else:
			rootNodeDic[go] = 'GO:0008150'
	return(rootNodeDic)

## Function to retrieve the internal confidence (inc) scores for each go term in the weight dic, returns a dictionary
def getIncScores(weightDic,rootNodeDic):
	print('Getting inc scores')
	incScoreDic = defaultdict(dict)
	for prot,goTerms in weightDic.items():
		for goTerm in goTerms:
			if not goTerm in rootNodeDic:
				rootNode = 'GO:0008150'
			else:
				rootNode = rootNodeDic[goTerm]
			goWeight = weightDic[prot][goTerm]
			if rootNode in weightDic[prot]:
				rootGoWeight = weightDic[prot][rootNode]
			else:
				rootGoWeight = goWeight
			incScore = goWeight/rootGoWeight
			incScoreDic[prot][goTerm] = incScore
	return(incScoreDic)

## Function to create a standard deviation of all the group scores
def standardDeviation(weightDic):
	list = []
	for prot,goTerms in weightDic.items():
		for goTerm in goTerms:
			list.append(groupScoreDic[prot][goTerm])
	stdDev = numpy.std(list)
	return(stdDev)

## Function to calculate the Z score of a GO term prediction
def getZScore(weightDic,stdDev,rootNodeDic,goSlimDic):
	print('Getting Z-Scores')
	zScoreDic = defaultdict(dict)
	for prot,goTerms in weightDic.items():
		for goTerm in goTerms:
			try:
				rootNode = rootNodeDic[goTerm]
				goWeight = weightDic[prot][goTerm]
				rootGoWeight = weightDic[prot][rootNode]
				goSlim = goSlimDic[goTerm]
				zScore = (goWeight-(rootGoWeight/len(goSlim)))/stdDev
				zScoreDic[prot][goTerm] = zScore
				
			except:
				zScoreDic[prot][goTerm] = 0
				continue
	return zScoreDic

## Function to retrieve the amount of times a GO term occurs in the GOA
def getGoCounts(rootNodeDic):
	goCountsDic = defaultdict(int)
	for line in open('data/goCounts.tab'):
		ssline = line.strip().split('\t')
		go = ssline[0]
		counts = int(ssline[1])
		goCountsDic[go] = counts
		if go in rootNodeDic:
			rootNode = rootNodeDic[go]
			goCountsDic[rootNode] += counts
	return(goCountsDic)

## Function to retrieve the IC score for a given GO term
def getIcScore(goTerm,goCountsDic,rootNodeDic,childrenDic):
	if goTerm in rootNodeDic:
		rootNode = rootNodeDic[goTerm]
	else:
		rootNode = 'GO:0008150'
	totRootProteins = goCountsDic[rootNode]
	ic = 0
	goCounts = float(goCountsDic[goTerm])
	children = childrenDic[goTerm]
	for child in children: ## GO counts for child GO terms are added up to the total
		goCounts += float(goCountsDic[child])
	ic = -log10(float(goCounts)/float(totRootProteins))
	return(ic)

## Calculates the total score for each GO term
def getTotalScores(protGoDic,groupScoreDic,incScoreDic,goCountDic,goTypeDic,childrenDic,goSlimDic,zScoreDic):
	print('Calculating total scores')
	outfile = open(sys.argv[3],'w')
	for prot,values in protGoDic.items():
		for goTerm in values:
			goWeight = protGoDic[prot][goTerm][0]
			incScore = incScoreDic[prot][goTerm]
			groupScore = groupScoreDic[prot][goTerm]
			icScore = getIcScore(goTerm,goCountsDic,rootNodeDic,childrenDic)
			incGroupScore = incScore/groupScore
			if not zScoreDic[prot][goTerm] < 300:
				outfile.write(prot+'\t'+goTerm+'\t'+str(icScore*incScore*goWeight)+'\n')
	outfile.close()

print('ArgotToo usage: <BLAST file (qseqid \\t sseqid \\t evalue)> <HMMER file (qseqid \\t domain \\t evalue)> <output file>')

if not len(sys.argv) == 4:
	print("Not enough commands passed to ArgotToo")
	sys.exit()

childrenDic,parentsDic,goSlimDic = getGoSlim()
rootNodeDic = getRootNodes()
goCountsDic = getGoCounts(rootNodeDic)
protGoDicBLAST = readBlast(sys.argv[1])
protGoDicHMMER = readHMMER(sys.argv[2])
protGoDic = mergeAnnotations(protGoDicBLAST,protGoDicHMMER)
weightDic = getGoWeightDic(protGoDic,parentsDic,rootNodeDic)
incScoreDic = getIncScores(weightDic,rootNodeDic)
groupScoreDic,groupScoreNcDic = getGroupScores(incScoreDic,parentsDic,rootNodeDic,childrenDic,goCountsDic)
stdDev = standardDeviation(weightDic)
zScoreDic = getZScore(weightDic,stdDev,rootNodeDic,goSlimDic)
totalScore = getTotalScores(protGoDic,groupScoreNcDic,incScoreDic,goCountsDic,rootNodeDic,childrenDic,goSlimDic,zScoreDic)
