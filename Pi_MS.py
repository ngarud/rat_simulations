import sys
from optparse import OptionParser
import copy


######################

def clusterHaplotypes(inFile, outFile):
    #Every 10Kb, calculate Pi
    nSam=29 +1 
    
    lineNumber = 1
    SNP_count = 0
    flies = initialize()
    
    for line in inFile:
        coord = float(line.split(',')[0])
        
        SNP_count +=1
        #add to the flies vector
        for i in range(1,nSam):
            flies[i].append(line.split(',')[i])
        

    # calculate pi
    Pi=calcPi(flies)
    outFile.write(str(SNP_count) + '\t' + str(Pi) + '\n' )
    
def initialize():
    nSam = 29+1
    flies={}
    for i in range(1,nSam):
        flies[i] = []
    return flies

def calcPi(flies):
    # in this definition I will calculate allele frequencies and return a vector of the frequencies in the given population

    nSam=29 + 1
    
    frequencies = []

    for j in range(0, len(flies[1])):
        nucleotides = [0,0,0,0]
        for i in range(1,nSam):

            if flies[i][j] == 'A':
                nucleotides[0] +=1
            if flies[i][j] == 'T':
                nucleotides[1] +=1
            if flies[i][j] == 'G':
                nucleotides[2] +=1
            if flies[i][j] == 'C':
                nucleotides[3] +=1
        
        # check whether or not this SNP has exactly two alleles           
        counter=0
        for y in range(0, len(nucleotides)):
            if nucleotides[y]>0:
                counter +=1
        if  counter == 2:
            frequencies.append(float(max(nucleotides))/sum(nucleotides))


    # Now iterate through the frequencies vector and calculate pi
    Pi=0
    for w in range(0, len(frequencies)):
        Pi += 2*frequencies[w]*(1-frequencies[w])
    Pi = Pi*30/29

#    print frequencies
#    print Pi
    return Pi





    
###############


def mkOptionParser():
    """ Defines options and returns parser """
    
    usage = """%prog  <input.bed> <output.bed> <threshold>
    %prog filters out the lines that don't meet a certain threshold. """

    parser = OptionParser(usage)
   

    return parser



def main():
    """ see usage in mkOptionParser. """
    parser = mkOptionParser()
    options, args= parser.parse_args()

    if len(args) != 2:
        parser.error("Incorrect number of arguments")


    inFN         = args[0]
    outFN        = args[1]
    

    if inFN == '-':
        inFile = sys.stdin
    else:
        inFile      = open(inFN, 'r')

    if outFN == '-':
        outFile = sys.stdout
    else:
        outFile      = open(outFN, 'w')



    clusterHaplotypes(inFile, outFile)


    

#run main
if __name__ == '__main__':
    main()
