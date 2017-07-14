from collections import defaultdict

import pandas as pd
import matplotlib.pyplot as plt

from sklearn import base
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder


class_features = ['AntiqueandClassic','Barge','Catamaran','CenterCockpit','CommercialBoat','Cruiser','CruiserRacer',
				  'Cutter','Daysailer','DeckSaloon','Ketch','Motorsailer','Multi-Hull','Pilothouse','RacingSailboat',
				  'Schooner','Sloop','Trimaran','Yawl','Other']

generic_features = ['Length','Year','PostedAfter','LatLon','Material','NumEngines']

specific_features = ['Ballast','Beam','Displacement','MaxDraft','MinDraft','LOA','LWL','SA',	# continuous
					 'RigType','HullType','BallastType','Construction',							# catagorical
					 'Water','Fuel']															# other

derived_features = ['BallastDisp','SADisp1','SADisp2']

rig_features = ['E','EY','I','ISP','J','P','PY','SPLTPS','SAFore','MastHeight','ListedSA']

engine_features = ['HP','EngineMake','EngineModel']

build_features = ['NumBuilt','Builder','Designer','FirstBuilt','LastBuilt']

other_features = ['Name','ID','Broker','Description','ListingType','Location','MakeModel','Price','href','FuelType_x','FuelType_y']



if __name__ == '__main__':

	cat_feats =  ['HullType','RigType']
	cont_feats = []# ['Length','Year']
	label_feat = ['Price'] 
	all_feats = cat_feats+cont_feats+label_feat

	# input 
	df = pd.read_csv('JOINED.csv',low_memory=False,usecols=all_feats)[all_feats]

	# drop missing values
	df.dropna(subset = cat_feats,inplace=True)

	# encode catagorical features
	cat_dict = defaultdict(LabelEncoder)
	df[cat_feats] = df[cat_feats].apply(lambda x: cat_dict[x.name].fit_transform(x))

	# create matrix
	data = df.as_matrix()
	labels = data[:,-1].astype(float)
	data = data[:,:-1]
	cat_inds = range(0,len(cat_feats))

	pipeline = Pipeline([
						('ohe', 	OneHotEncoder()),
						# ('tfidf', 	TfidfTransformer()),
						# ('clf', 	SGDClassifier()),
						('rf',		RandomForestRegressor())
						])

	parameters =	{
					'ohe__categorical_features': cat_inds,
					'rf__n_estimators' : 50,
					'rf__min_samples_leaf' : 20
					}

	pipeline.set_params(**parameters)
	enc_data = pipeline.fit_transform(data,labels)

	ohe = pipeline.named_steps['ohe']
	rf = pipeline.named_steps['rf']

	all_enc_feats = []
	for cat in cat_feats:
		all_enc_feats += list(cat_dict[cat].classes_)
	all_enc_feats += cont_feats


	importances = pd.DataFrame({'features':all_enc_feats,'importance':rf.feature_importances_})

	importances.plot(kind='barh',x='features',title='Feature Importance',legend=False,figsize=(20,8))
	
	plt.tight_layout()

	plt.show()

	# le = sklearn.preprocessing.LabelEncoder()
	# HullType_data = le.fit_transform(df['HullType'].as_matrix())
	# HullType_data = HullType_data.astype(float)

	# encoder = sklearn.preprocessing.OneHotEncoder(categorical_features=le.classes_)
	# encoded_HullType_data = encoder.fit_transform(HullType_data)

#	train, test, labels_train, labels_test = train_test_split(data, labels, train_size=0.80)

	



	# # uncommenting more parameters will give better exploring power but will
	# # increase processing time in a combinatorial way
	# parameters = {
	#     'vect__max_df': (0.5, 0.75, 1.0),
	#     #'vect__max_features': (None, 5000, 10000, 50000),
	#     'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
	#     #'tfidf__use_idf': (True, False),
	#     #'tfidf__norm': ('l1', 'l2'),
	#     'clf__alpha': (0.00001, 0.000001),
	#     'clf__penalty': ('l2', 'elasticnet'),
	#     #'clf__n_iter': (10, 50, 80),
	# }

	#grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)

	# rf = RandomForestRegressor(n_estimators=50,min_samples_leaf=20)
	# rf.fit(data,labels)

	# sklearn.metrics.mean_absolute_error(labels_test, rf.predict(encoder.transform(test)))
	# sklearn.metrics.median_absolute_error(labels_test, rf.predict(encoder.transform(test)))
	# sklearn.metrics.explained_variance_score(labels_test, rf.predict(encoder.transform(test)))
	# sklearn.metrics.r2_score(labels_test, rf.predict(encoder.transform(test)))

	# importances = pd.DataFrame({'features':all_features,'importance':rf.feature_importances_})

	# importances.plot(kind='bar',x='features',title='Feature Importance',legend=False,figsize=(20,8))
	
	# plt.show()

	# train, test, labels_train, labels_test = sklearn.model_selection.train_test_split(data, labels, train_size=0.80)

	# imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
	# imp.fit(data)
	# imp_train = imp.transform(train)

	# rf = sklearn.ensemble.RandomForestRegressor(n_estimators=500,n_jobs=1)
	# rf.fit(imp_train, labels_train)

	# print(sklearn.metrics.mean_absolute_error(labels_test, rf.predict(imp.transform(test))))
	# print(sklearn.metrics.median_absolute_error(labels_test, rf.predict(imp.transform(test))))
	# print(sklearn.metrics.explained_variance_score(labels_test, rf.predict(imp.transform(test))))
	# print(sklearn.metrics.r2_score(labels_test, rf.predict(imp.transform(test))))

	# tot_imp = pd.DataFrame({'features':feature_names[:-1],'importance':rf.feature_importances_})

	# tplt = tot_imp.plot(kind='bar',x='features',title='Feature Importance',legend=False)
	# plt.tight_layout()
	# plt.show()
