#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Script for simulating pan-genomes. Outputs a Roary-like gene_presence_absence.csv and a Traits file
# Use: Simulate_pan_genome.py causal_gene_penetrance desired_number_of_samples
# Author: Ola Brynildsrud

import random
import copy
import sys

class SimStrain:
	
	def __init__(self, genome=None, core_genes=3000, pan_genes=6000, trait=0):
		if genome is None:
			self.genome = self.create_genome(core_genes, pan_genes)
		else:			
			self.genome = genome
		self.trait = trait
		
	def mutate(self):
		try:
			for gene in self.genome:
				if random.random() <= self.genome[gene].mutchance:
					self.genome[gene].switchstate()
					if self.genome[gene].name == "causal":
						if self.genome["causal"].present:
							if random.random() <= penetrance:
								self.trait = 1
							else:
								self.trait = 0
						else:
							if random.random() <= penetrance:
								self.trait = 0
							else:
								self.trait = 1
		except TypeError:
			print(self.genome)
						
	def create_genome(self,core_genes=3000, pan_genes=6000):
		genome = {}
		for x in xrange(core_genes):
			genome["gene_" + str(x)] = Gene("gene_" + str(x), mutchance=0, present=1, causal=False)
		for y in xrange(core_genes, (core_genes + pan_genes)):
			genome["gene_" + str(y)] = Gene("gene_" + str(y), mutchance=(random.random()/100), present=0, causal=False)
		genome["causal"] = Gene("causal", mutchance=0.01,present=0,causal=True)
		return genome
			
	def switchTrait(self):
		if self.trait == 1:
			self.trait = 0
		else:
			self.trait = 1	
		
class Gene:
	
	def __init__(self, name, mutchance,present=0,causal=False):
		self.name = name
		if mutchance is None:
			self.mutchance = random.random() / 100
		else:
			self.mutchance = mutchance
		self.causal = causal
		self.present=present
		
	def switchstate(self):
		if self.present == 1:
			self.present = 0
		else:
			self.present = 1
		
def main():

	root = SimStrain()
	Genome_collection = {}
	Genome_collection["root"] = root
	Number_of_completed_genomes = 1
	add_these_genomes = []

	while Number_of_completed_genomes < number_of_tips:
		for genome in Genome_collection:
			Genome_collection[genome].mutate()
			if random.random() <= 0.01:
			# MUTATE AND BRANCH. Check success to determine which genome will mutate next
				new_genome = copy.deepcopy(Genome_collection[genome])
				new_genome.mutate()
				add_these_genomes.append(new_genome)
				
		# Add the additional genomes
		for newgenome in add_these_genomes:
			try:
				Genome_collection[strain_names.pop()] = newgenome
			except IndexError:
				break
			Number_of_completed_genomes += 1
		add_these_genomes = []
	
	print Number_of_completed_genomes
	
	# Write genome presence/absence matrix and phenotype
	
	with open("Gene_presence_absence.csv", "w") as gpa:
		with open("Trait.csv","w") as t:
			
			# Header line:
			header = ","
			for Strain in sorted(Genome_collection.keys()):
				header = header + Strain + ","
			header = header.rstrip(",") + "\n"
			gpa.write(header)
			
			# Gene presence absence matrix
			for gene in sorted(root.genome.keys()):
				line = gene + ","
				for Strain in sorted(Genome_collection.keys()):
					line = line + str(Genome_collection[Strain].genome[gene].present) + ","
				line = line.rstrip(",") + "\n"
				gpa.write(line)
				
			# Traits file
			t.write(",Trait\n")
			for Strain in sorted(Genome_collection.keys()):
				line = Strain + "," + str(Genome_collection[Strain].trait) + "\n"
				t.write(line)
		
if __name__ == '__main__':
	# Set parameters
	penetrance = float(sys.argv[1])
	number_of_tips = int(sys.argv[2])
	strain_names = [str(x) for x in xrange(number_of_tips)]
	
	main()
