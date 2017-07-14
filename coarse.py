from collections import defaultdict
from datetime import datetime, timedelta

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import explained_variance_score


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

	cont_feats =  ['PostedAfter']
	label_feat = ['Price'] 
	all_feats = cont_feats+label_feat

	# input 
	df = pd.read_csv('JOINED.csv',low_memory=False,usecols=all_feats)[all_feats]

	# fix dates
	last_date = int(pd.to_datetime(df['PostedAfter']).max().strftime('%s'))
	df['PostedAfter'] = pd.to_datetime(df['PostedAfter']).apply(lambda x: last_date-int(x.strftime('%s')))


	# drop missing values
	df.dropna(subset = ['PostedAfter'],inplace=True)

	#df['PostedAfter'] = df['PostedAfter'].astype(float)**(-1)

	# create matrix
	data = df.as_matrix()
	labels = data[:,-1].astype(float)
	data = data[:,:-1]

	pipeline = Pipeline([
						('pf', 		PolynomialFeatures()),
						# ('tfidf', 	TfidfTransformer()),
						# ('clf', 	SGDClassifier()),
						('ridge',	Ridge())
						])

	parameters =	{
					'pf__degree': 1,
					'ridge__alpha' : 0.1
					}

	pipeline.set_params(**parameters)
	pipeline.fit(data,labels)

	x = [[i] for i in range(10,150)]
	y = pipeline.predict(x)

	plt.plot(x,y,color='red', linewidth=2,label="fit")

	plt.scatter(df.PostedAfter, df.Price, color='navy', s=3, marker='o', label="training points")
	
	#plt.xlim(0,10**8 ) 
	plt.ylim(0, 10**6)

	plt.xlabel('Age (s)')
	plt.ylabel('Price [USD]')
	plt.title('Polynomial Fit of Price vs Age')

	plt.tight_layout()

	plt.show() 

	print(pipeline.named_steps['ridge'].intercept_)
	print(pipeline.named_steps['ridge'].coef_)

	# sklearn.metrics.mean_absolute_error(labels_test, rf.predict(encoder.transform(test)))
	# sklearn.metrics.median_absolute_error(labels_test, rf.predict(encoder.transform(test)))
	evs = explained_variance_score(df.Price.values.reshape(-1,1), pipeline.predict(df.Length.values.reshape(-1,1)))
	print(evs)
	# sklearn.metrics.r2_score(labels_test, rf.predict(encoder.transform(test)))

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
