import pandas as pd
import matplotlib.pyplot as plt

from sklearn import linear_model

from fuzzywuzzy import process
from fuzzywuzzy import fuzz

if __name__ == '__main__':

	df = pd.read_csv('JOINED.csv',low_memory=False)

	designers = list(df.Designer.value_counts().index)

	designer_dict = {'J. Valentijn' : 'Johan Valentijn', 
					 'Turun Veneveistramo':'Turien Veneveistramo',
					 'D. Tortarolo' : 'Daniel Tortarolo',
					 'Van de Stadt':'E. G. van de Stadt',
					 'Eric Segerlind':'Erik Segerlind',
					 'Jac. de Ridder':'Jacques de Ridder',
					 'J. De Ridder':'Jacques de Ridder',
					 'Ray Richards':'Raymond Richards', 
					 'Philip Rhodes':'Phillip Rhodes',
					 'Homann & Pyle':'Holman & Pyle',
					 'Holman & Pye':'Holman & Pyle',
					 'Mike Pocock':'Michael Pocock',
					 'Bob Perry':'Robert Perry',
					 'Dave Pedrick' : 'David Pedrick',
					 'Dick Newick' : 'Richard Newick',
					 'Morelli & Melvin' : 'Morrelli & Melvin',
					 'Al Mason': 'Alvin Mason',
					 'D. Martin' : 'Don Martin',
					 'Frans Maas' : 'Franz Maas',
					 'M. Lombard' : 'Marc Lombard',
					 'Lazarra' : 'Lazzara',
					 'Kaufman & Ladd' : 'Kaufmann & Ladd',
					 'Robb Ladd' : 'Robert Ladd',
					 'Paul Kettenburg': 'Paul Kettenberg',
					 'Rob Humphries' : 'Robert Humphreys',
					 'Humphreys' : 'Robert Humphreys',
					 'L. F. Herreshoff' : 'L. Francis Herreshoff',
					 'Phillippe Harle' : 'Philippe H. Harl',
					 'P. Harle' : 'Philippe H. Harl',
					 'Philip Harle' : 'Philippe H. Harl',
					 'B. Farr' : 'Bruce Farr',
					 'O. Enderlien' : 'Olle Enderlein',
					 'M. Dufour' : 'Michel Dufour',
					 'Ed Dubois' : 'Edward Dubois',
					 'W.I.B. Crealock' : 'William Crealock',
					 'Dick Carter' : 'Richard Carter',
					 'H. Amel & J. Carteau' : 'Henry Amel & J. Carteau',
					 'F. Butler' : 'Frank Butler',
					 'P. Briand':'Philippe Briand',
					 'Rob Ball':'Bob Ball',
					 'R. Ball':'Bob Ball',
					 'Berret': 'Jean Berret',
					 'Jean Beret' : 'Jean Berret',
					 'Henry Adriaanse' : 'Henri Adriaanse',
					 'Morgan' : 'Charles Morgan',
					 'Morelli & Melvin' : 'Morrelli & Melvin'}

	for i,designer in enumerate(designers):
		best_match = process.extractOne(designer,designer_dict.values(), scorer=fuzz.token_set_ratio)
		if best_match:
			if best_match[1] > 93:
				designer_dict[designer] = best_match[0]
				continue
		best_match = process.extractOne(designer,designers[:i], scorer=fuzz.token_set_ratio)
		if best_match:
			if best_match[1] > 93:
				designer_dict[designer] = best_match[0]

	def designer_match(designer):
		if not designer:
			return None
		if designer in designer_dict:
			return designer_dict[designer]
		else:
			return designer

	df.Designer = df.Designer.apply(designer_match)

	df.to_csv('DESIGNER.csv',index=False)

	print(df.Designer.value_counts())
	for designer in map(" ".join,sorted(map(lambda x: x.split(),df.Designer.value_counts().index),key=lambda x: x[-1])):
		print(designer)
