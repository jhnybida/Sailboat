from __future__ import print_function
import scipy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import (Imputer,StandardScaler,RobustScaler)
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn import (metrics,manifold,cluster,decomposition)
from sklearn.cluster import AgglomerativeClustering

df = pd.read_csv('JOINED.csv',low_memory=False)

df['DispLen'] = df.Displacement/2240/(0.01*df.LWL)**3
df['MotionComfort'] = df.Displacement/(0.65*(0.7*df.LWL + 0.3*df.LOA)*df.Beam**1.333)
df['CapsizeScreening'] = df.Beam/(df.Displacement/64)**0.333

feature_names = ['DispLen','SADisp1','MotionComfort','CapsizeScreening']

class_labels = ['AntiqueandClassic','Barge','Catamaran','CenterCockpit','CommercialBoat','Cruiser','CruiserRacer','Cutter',
				'Daysailer','DeckSaloon','Ketch','Motorsailer','Multi-Hull','Pilothouse','RacingSailboat','Schooner','Sloop',	
				'Trimaran','Yawl','Other']

class_totals = df[class_labels].astype(int).sum(axis=0)
sorted_class_totals = sorted(enumerate(class_totals),key=lambda x: x[1],reverse=True)

df['Class'] = 0
label = 1
for ind, tot in sorted_class_totals:
	df.loc[df[class_labels[ind]]==1,'Class'] = label
	label += 1

df['Class2'] = 1
df.loc[df['CruiserRacer']==1,'Class2'] = 2
df.loc[df['RacingSailboat']==1,'Class2'] = 3
df.loc[df['Motorsailer']==1,'Class2'] = 4

# imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
# imp.fit(X)
# X = imp.transform(X)

# sclr = StandardScaler()
# sclr.fit(X)
# X = sclr.transform(X)

# pca = PCA(n_components=6)
# pca.fit(X)
# X = pca.transform(X)
# print("explained variance ratios:")
# print(pca.explained_variance_ratio_)
# print(pca.explained_variance_ratio_.sum())

# #tsne = manifold.TSNE(n_components=2)
# #X = tsne.fit_transform(X)

# #embedder = manifold.SpectralEmbedding(n_components=2,eigen_solver="arpack")
# #X = embedder.fit_transform(X)

# est = KMeans(init='k-means++', n_clusters=3,n_init=10)
# est.fit(X)
# labels = est.labels_
# print("silhouette score:")
# print(metrics.silhouette_score(X, labels,metric='euclidean',sample_size=300))

# #ward = AgglomerativeClustering(n_clusters=4, linkage='ward')
# #ward.fit(X)
# #labels = ward.labels_

# X = pca.inverse_transform(X)
# X = sclr.inverse_transform(X)

# X = df.loc[df.Class2.isin([2,3,4]),feature_names].as_matrix()
# colors = df.loc[df.Class2.isin([2,3,4]),'Class2']

# for i in range(1,len(feature_names)):
# 	plt.figure(i)
# 	plt.scatter(X[:,0], X[:,i],s=0.5,c=colors)
# 	axes = plt.gca()
# 	axes.set_xlim([0,50])
# plt.show()


CR = plt.scatter(df.loc[df['CruiserRacer']==1,'DispLen'],df.loc[df['CruiserRacer']==1,'SADisp1'],s=3)
MS = plt.scatter(df.loc[df['Motorsailer']==1,'DispLen'],df.loc[df['Motorsailer']==1,'SADisp1'],s=3)
RS = plt.scatter(df.loc[df['RacingSailboat']==1,'DispLen'],df.loc[df['RacingSailboat']==1,'SADisp1'],s=3)

plt.legend((CR,MS,RS),
           ('CruiserRacer','MotorSailer','RacingSailboat'),
           scatterpoints=1,
           loc='upper right',
           ncol=3,
           fontsize=8)
axes = plt.gca()
axes.set_ylim([0,50])

plt.xlabel('Displacement Length ratio')
plt.ylabel('Sail Area Displacement ratio')
plt.title('Sail Power vs Weight')
#fig.savefig('SADvDL.jpg')

plt.show()


