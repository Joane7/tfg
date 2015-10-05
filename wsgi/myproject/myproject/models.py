# -*- coding: utf-8 -*-
#from django.db import models

class resultat():#Classe resultat
	"""docstring for ClassName"""
	def __init__(self, var, valor, operacio,pas,equacio,numFor):
		self.var=var#variable
		self.valor=valor#valor de la variable
		self.operacio=operacio#operacio realitzada
		self.pas=pas#Numero de operacio feta
		self.equacio=equacio+"=0"#Equacio
		self.numFor=numFor#Numero de formula de la equqacio completa

class equacioCompleta():#Classe equacio
	"""docstring for ClassName"""
	def __init__(self, equacio, canonica, num, tipus):
		self.equacio=equacio#Equacio
		self.canonica=canonica#Canonica
		self.num=num#Identificador
		self.tipus=tipus#Tipus d'equacio

class image():#Classe imatge del graf
	"""docstring for ClassName"""
	def __init__(self, path, num, nom):
		self.path=path#Ruta
		self.num=num#Pas
		self.nom=nom#Nom del graf

class igualacio():#Classe imatge del graf
	"""docstring for ClassName"""
	def __init__(self, equacio,numEquacio, equacio1, numEqua1, equacio2,numEqua2):
		self.equacio=equacio#Ruta
		self.numEquacio=numEquacio#Número d'equació
		self.equacio1=equacio1#Pas
		self.numEqua1= numEqua1#Número d'equació 1
		self.equacio2=equacio2#Nom del graf
		self.numEqua2= numEqua2#Número d'equació 2

class relacio():#Classe imatge del graf
	"""docstring for ClassName"""
	def __init__(self, valor, canonica):
		self.valor=valor#Ruta
		self.canonica=canonica#Pas


	