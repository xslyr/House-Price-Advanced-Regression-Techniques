#/usr/bin/python3
#!encoding:utf8
#
#	Created at 26-05-2023
#	Coder: Wesley R. Silva
#	Library with functionalities similar a "Pandas Dataframe Describe".
#

import pandas as pd
import numpy as np

class DataOverview:
	possible_dtypes = ['int64','float64','object','bool', 'datetime64']
	cols = ['dtype','count','null','min','mean','max','median','std','std%','25%','50%','75%','mode','n_mode']
	details = pd.DataFrame([], index=cols)

	def __init__(self, dataframe):	
		if not isinstance(dataframe, pd.DataFrame):
			raise ValueError("It's necessary an dataframe argument to instantiate this object.")
		else:
			self.df = dataframe
			for i in range(self.df.columns.size):
				self.details = pd.concat([self.details, self.__extractData(i)], axis=1)
		return
		
	def __extractData(self, i):
		aux = pd.DataFrame(np.zeros(shape=(len(self.cols),1)), index=self.cols, columns=[self.df.columns[i]])
		aux.loc['dtype'] = 'object' if self.df[aux.columns[0]].dtypes == 'O' else self.df[aux.columns[0]].dtypes
		aux.loc['count'] = self.df[aux.columns[0]].count()
		aux.loc['null'] = self.df[aux.columns[0] ].isnull().sum()
		aux.loc['mode'] = self.df[aux.columns[0]].mode(dropna=False).iloc[0]
		aux.loc['n_mode'] = self.df[aux.columns[0]].value_counts().sort_values(ascending=False).iloc[0]
		if self.df[aux.columns[0]].dtypes in ['int64','float64']:
			aux.loc['std'] = float('{:.2f}'.format(self.df[aux.columns[0]].std()))
			aux.loc['min'] = float('{:.2f}'.format(self.df[aux.columns[0]].min()))
			aux.loc['mean'] = float('{:.2f}'.format(self.df[aux.columns[0]].mean()))
			aux.loc['max'] = float('{:.2f}'.format(self.df[aux.columns[0]].max()))
			aux.loc['median'] = float('{:.2f}'.format(self.df[aux.columns[0]].median()))
			aux.loc['std%'] = float('{:.2f}'.format(100*self.df[aux.columns[0]].std()/(self.df[aux.columns[0]].max()-self.df[aux.columns[0]].min())))
			aux.loc['25%'] = self.df[aux.columns[0]].quantile(q=0.25)
			aux.loc['50%'] = self.df[aux.columns[0]].quantile(q=0.5)
			aux.loc['75%'] = self.df[aux.columns[0]].quantile(q=0.75)
		return aux
		
	def columns_type(self):
		cols_dtype = { t:0 for t in self.possible_dtypes }
		for i in self.df.columns:
			cols_dtype[ str(self.df[i].dtypes) ] +=1
		return  cols_dtype
    
	def show(self, type='all'):
		aux = pd.DataFrame([], index=self.cols)
		if type not in ['all']+self.possible_dtypes:
			raise ValueError('Error type parameter. Choose one of this values: {}'.format(['all']+self.possible_dtypes))
		elif (type in self.possible_dtypes) and (self.columns_type()[type]>0):
			for i,col in enumerate(self.details):
				if self.details[col]['dtype'] == type:
					aux = pd.concat([aux, self.__extractData(i)], axis=1)
		else:
			aux = self.details
		if type=='object':
			aux = pd.concat( [aux.iloc[:3,:], aux.iloc[-2:,:]], axis=0 )
		return aux
	
	def __extractDistrib(self, col):		
		aux = self.df.loc[:,col].value_counts(ascending=False)
		distrib_values = [["{} {}".format(e,aux[e])] for e in aux.to_dict()]
		return pd.DataFrame( distrib_values , columns=[col], index=[i+1 for i in range(len(distrib_values))])
	
		
	def obj_distrib(self, column_list=[], axis=1, include_nulls=True):
		axis_option=(0,1)
		if axis not in axis_option:
			raise ValueError("The axis parameter must be 0(lines) or 1(columns). ")
		
		df=self.show('object')
		aux = pd.concat([self.__extractDistrib(col) for col in df], axis=1) if len(column_list)==0 else pd.concat([self.__extractDistrib(col) for col in df[column_list]], axis=1)
		aux = aux.fillna('')
		
		if include_nulls:
			if len(column_list)==0:
				null_values = df[df.columns].iloc[2,:]
				null_df = pd.DataFrame([["null {}".format(e) for e in null_values.to_list() ]], columns=df.columns)
				aux = pd.concat([null_df,aux],axis=0)
			else:
				null_values = df[column_list].iloc[2,:]
				null_df = pd.DataFrame([["null {}".format(e) for e in null_values.to_list() ]], columns=column_list)
				aux = pd.concat([null_df,aux],axis=0)
		
		return aux if axis==1 else aux.transpose()

