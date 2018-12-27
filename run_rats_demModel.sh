#!/bin/bash
# This script takes in an MS file  with 1000 simulations, and outputs a concatenated processed file. 
file=$1
#rho_in=$2
#adaptive_theta=$3
#selection=$4
#locusLength=$5

#rho_in=5e-9
#adaptive_theta=10
#selection=True
#file=tmp.txt

outFile=~/rats/analysis/rats_neutrality_H12

for i in `seq 1 1000`; do

echo $i

~/./msms/bin/msms 29 1 -t 402 -r 26.16 5153846  -G 7.54E-2 -eG 341572.5 1.07E-4 > $file


# proceed with analyzing the sweep                                   

# cut the file

lineNo=`cat $file | grep -n segsites | cut -f1 -d ':'`
(( lineNo = lineNo + 30 ))
cat $file | head -${lineNo} | tail -30 > ${file}_cut


#numLines=`cat ${file}_cut | egrep '(2|3|4|5|6|7|8|9|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)' | wc -l`

#if [ $numLines == 1 ]
#then
#HS=1
#else
#HS=0
#fi


#convert to MSMS format

python ~/rats/scripts/convertMS.py ${file}_cut ${file}_MS


# cluster 

python ~/rats/scripts/H12_H2H1_simulations.py ${file}_MS 29 -o ${file}_cluster_snps -w 201 -j 50 -d 0 -s 0.5

cat ${file}_cluster_snps >> ${outFile}_snps.txt
#cat ${file}_cluster_bps >> ${outFile}_bps.txt

python ~/rats/scripts/Pi_MS.py ${file}_MS ${file}_pi
cat ${file}_pi >> ${outFile}_pi.txt

rm ${file}
rm ${file}_var
rm ${file}_cut
rm ${file}_MS
rm ${file}_cluster_snps
rm ${file}_pi 
#rm ${file}_cluster_bps


done

