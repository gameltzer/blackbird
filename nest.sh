#!/bin/bash

# This is just for intelligbitlity. 

sample1=$1

sample2=$2

reference=$3 
#this is what the new output files are built using. (ecept for with bowtie2-build)
filebase=$4
#This is creating the index.
bowtie2-build --offrate 3 $reference $reference
echo "build is done"

#This uses filebase for the SAM file output by bowtie2. 
samName=$filebase.sam

metFile=metrics$samName
#This requires that 1 and 2 must be properly associated with the correct 1 and 2 options.

bowtie2 --no-mixed  --seed 3 -x $reference -1 $sample1 -2 $sample2 -S $samName --met-file $metFile 

# This stores the bam name
bamName=$fileBase.bam

# this converts the file to a bam file.
samtools view -b $samName > $bamName

#this indexes the bam file so it can be sorted.
samtools faidx $reference

#This stores the vcfName, and the sortedBamName

vcfName=$filebase.vcf
sortedBamName=$filebase.Sorted.bam 

#The creates a sorted bam file, and then, using bcftools mpileup, generates a vcf file with he proper annotations.
samtools sort -m 250M -O BAM $bamName -o $sortedBamName && bcftools mpileup -f $reference -a INFO/AD -o $vcfName -O v $sortedBamName

## this gets us a variant only file. The ploidy is specified as 1 because it is a bacterial genome. 
bcftools call --ploidy 1 -mv -Ov -o final$vcfName $vcfName
