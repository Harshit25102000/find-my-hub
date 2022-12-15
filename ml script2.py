import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
df = pd.read_csv(r'clustered_amenities.csv')
from sklearn.model_selection import train_test_split
x=df.drop(['cluster'],axis='columns')
y=df.cluster
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=1)
from sklearn.neighbors import KNeighborsClassifier
knn=  KNeighborsClassifier(n_neighbors=4)
knn.fit(x_train,y_train)
print(knn.score(x_test,y_test))
import joblib
file='amenity_classifier_py.sav'
joblib.dump(knn,file)