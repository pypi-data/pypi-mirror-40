import pandas as pd 
from sklearn.datasets import load_breast_cancer
from sklearn.datasets import load_boston

class Dominance_Datasets(object):
	"""docstring for Dominance_Datasets"""
	def __init__(self):
		pass

	def get_breast_cancer():
		print("""The copy of UCI ML Breast Cancer Wisconsin (Diagnostic) dataset is downloaded from: https://goo.gl/U2Uwz2""")
		print("""Internally using load_breast_cancer function from sklearn.datasets """)
		breast_cancer_data=pd.DataFrame(data=load_breast_cancer()['data'],columns=load_breast_cancer()['feature_names'])
		breast_cancer_data['target']=load_breast_cancer()['target']
		target_dict=dict({j for i,j in zip(load_breast_cancer()['target_names'],enumerate(load_breast_cancer()['target_names']))})
		breast_cancer_data['target_names']=breast_cancer_data['target'].map(target_dict)
		return breast_cancer_data.iloc[:,:-1]


	def get_boston():
		print("""The copy of Boston Housing Dataset is downloaded from: https://www.cs.toronto.edu/~delve/data/boston/bostonDetail.html""")
		print("""Internally using load_boston function from sklearn.datasets """)
		boston_data=pd.DataFrame(data=load_boston()['data'],columns=load_boston()['feature_names'])
		boston_data['House_Price']=load_boston()['target']
		return boston_data