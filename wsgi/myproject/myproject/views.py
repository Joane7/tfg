# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import Template, Context, RequestContext
from django.forms.fields import CheckboxInput

from myproject.models import *
import time
import string#Per poder fer el replace
from string import *#Per retornar boolean
import sympy#Llibreria per calcular les equacions
from sympy import *
import os#En permet eliminar imatges

#*************************Funcions amb retorn a un template**************************

def funcionament(request):
	return render(request,'funcionament.html',locals())

def quisom(request):
	return render(request,'quisom.html',locals())

def afegir(request):
	s = request.POST['equacio']
	if(len(s)==0) | ('=' not in s):
		equacio2=equacio
		return render(request,'inici.html',locals())
	#Mirem si l'usuari ha posar els * de la multiplicació-> Per la biblioteca
	s=multiplicacions(s)#Posar * -> 22a=22*a
	s=multiplicacionsInvertida(s)#Posar * ->a22=a*22
	equacio.equacioInicial = s
	equacio.plt.clf()
	separacio()#Separem les parts pel igual
	canonica()#Creem la canònica
	if not(equacio.equacioCanonica in equacio.nodelistFormules):
		if(len(s)!=0):
			variablesIndividuals()
			equacio2=""
			num=str(equacio.G.number_of_nodes())
			dibuixarGrafInicial()
			#dibuixarGrafInicialValors()
			#dibuixarGrafComplert()
			equacio2=equacio
			return render(request,'inici.html',locals())
	else:
		equacio2=equacio
		return render(request,'inici.html',locals())

def afegirInputs(request):
	equacio2=equacio
	return render(request,'inputs.html',locals())

#Metode per a l'inici i per reiniciar les dades
def inici(request):
	#equacio.llistatEquacions=[]
	equacio2=equacio
	return render(request,'inici.html',locals())

def afegirFormula(request):
	equacio2=equacio
	return render(request,'inici.html',locals())

def reinicia(request):
	reiniciarValors()
	return render(request,'inici.html',locals())

def error404(request):
    return render(request,'error404.html')

#Metode que inicia la resolució del problema
def graf(request):
	#Reiniciem els valors a 0 o buits
	equacio.listFormulesGrau=[]
	equacio.listCheckInValor=[]
	equacio.listCheckOutValor=[]
	equacio.listConegudesTotalsValor=[]
	equacio.listConegudes=[]
	equacio.listDesconegudes=[]
	equacio.listCheckOut=[]
	equacio.listCheckOutFixa=[]
	equacio.grau=0
	equacio.llargadaCheckOut=0
	equacio.nodeInicialDibuixat=False
	equacio.nodeInicialIgualacioDibuixat=False
	equacio.nodelistVarConFinal=[]#Aqui guardarem tots els nodes inputs utilitzats
	equacio.nodelistVarDesFinal=[]#Aqui guardarem tots els nodes que hem trobat solució que eren desconeguts
	equacio.nodelistVarOutputsFinal=[]#Aqui guardarem tots els nodes outputs trobats
	equacio.nodelistFormulesFinal=[]#Aquí guardarem tots els nodes formula utilitzats
	equacio.edgelistFinal=[]#Aquí guardarem tots els enllaços dels nodes variables als nodes formules
	equacio.edgelistCamiFinal=[]#Aquí guardarem els enllaços per seguir el camí
	equacio.labelsFinal={}#Valor que posarem als nodes
	equacio.GF = equacio.nx.Graph()#Reiniciem el graf pas a pas
	equacio.listRelacioEdgesNovesFormules=[]

	#Borrem imatges en cas que ja n'haguem creat
	if(len(equacio.listPath)>2):
		for valor in equacio.listPath:
			try:os.remove("myproject/static/img/"+valor.path+".png")
			except:None
	equacio.listPath=[]#Borrem els paths anteriors i afegim l'inicial
	if(len(equacio.pathFotoInicial)>0):
		equacio.listPath.insert(0,image(equacio.pathFotoInicial,"0","Graf inicial"))#L'afegim a la posicio 0 perque és l'inicial
	else:
		dibuixarGrafInicial()

	if(len(equacio.listPath2)>0):
		for valor in equacio.listPath2:
			try:os.remove("myproject/static/img/"+valor.path+".png")
			except:None
	equacio.listPath2=[]#Borrem els paths anteriors
	
	p = request.POST#Agafem tots els valors del post per obtenir els valors dels inputs
	equacio.listCheckOut = request.POST.getlist('check2')#Agafem els outputs
	equacio.listCheckOutFixa = [x[:] for x in equacio.listCheckOut]
	retorn=agafarValors(p)#Donem valor a les 3 llistes per poder fer el calcul

	#Control d'error d'introducció de dades
	if(retorn==False) | (len(equacio.listCheckOut)==0):
		equacio2=equacio
		sms="ouhhh!! No has introduït bé les dades :("
		return render(request,'inputs.html',locals())
	equacio.llargadaCheckOut=len(equacio.listCheckOut)#Llargada dels outs que hi ha
	reanudarGraf()#Tornem a crear el Graf Complert per poder veure els enllaços

	#Dupliquem les variables per dibuixar les imatges anteriors al pas
	equacio.nodelistConegudesUnica=[x[:] for x in equacio.listConegudes]
	equacio.nodelistCheckOutUnica=[x[:] for x in equacio.listCheckOut]
	equacio.nodelistDesconegudesUnica=[x[:] for x in equacio.listDesconegudes]
	#equacio.nodelistFormulesUnica=[x[:] for x in equacio.nodelistFormules]


	#Dupliquem les llistes
	nodelistVariablesInicial=[x[:] for x in equacio.nodelistVariables]
	nodelistFormulesInicial=[x[:] for x in equacio.nodelistFormules]

	#Tornem a dibuixar el graf pero amb valors
	dibuixarGrafInicialValors()


	buscarCheckOuts(len(equacio.listCheckOut))#Passem la llargada de outputs

	if(len(equacio.listPath)==2):del equacio.listPath[1]#Si només hi ha 2 borrem l'ultim perque no el necessitem

	resultats=None
	if(len(equacio.listPath2)==0):
		resultats=None
	else:
		resultats="SI"
		#ultima imatge amb tot resolt
		llarg=len(equacio.listPath2)+1
		numOpe = str(len(equacio.listCheckOutValor)+1)
		dibuixarGrafUnica2(llarg,numOpe)

	equacio2=equacio
	return render(request,'graf.html',locals())

#*************************Funcions de l'aplicació **************************
#Mètode per dibuixar graf inicial
def dibuixarGrafInicial():
	try:os.remove("myproject/static/img/"+equacio.pathFotoInicial+".png")
	except:None
	equacio.plt.clf()
	temps=time.time()
	equacio.pathFotoInicial=str(temps)+"_0"
	path = "myproject/static/img/"+equacio.pathFotoInicial+".png"
	pos=equacio.nx.spring_layout(equacio.GI)
	equacio.nx.draw_networkx_nodes(equacio.GI,pos,nodelist=equacio.nodelistVariables,node_color='#FFFF00',node_size=500,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.GI,pos,nodelist=equacio.listNovesVariablesFuncions,node_color='#FFFF00',node_size=2000,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.GI,pos,nodelist=equacio.nodelistFormules,node_color='#1E90FF',node_size=500,node_shape='s',alpha=1)#Blue
	equacio.nx.draw_networkx_edges(equacio.GI,pos,edgelist=equacio.edgelist,width=4,alpha=1,edge_color='black')
	equacio.nx.draw_networkx_labels(equacio.GI,pos,equacio.labels,font_size=16)
	equacio.plt.axis('off')
	equacio.plt.savefig(path)
	if(len(equacio.listPath)>0):
		equa=equacio.listPath[0]
		if(equa.num=="0"):
			image2=equacio.listPath.pop(0)
			try:os.remove("myproject/static/img/"+image2.path+".png")
			except:None
	equacio.listPath.insert(0,image(equacio.pathFotoInicial,"0","Graf inicial"))#L'afegim a la posicio 0 perque és l'inicial

def dibuixarGrafInicialValors():
	try:os.remove("myproject/static/img/"+equacio.pathFoto+".png")
	except:None
	equacio.plt.clf()
	temps=time.time()
	equacio.pathFoto=str(temps)+"_1"
	path = "myproject/static/img/"+equacio.pathFoto+".png"
	pos=equacio.nx.spring_layout(equacio.G)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.listConegudes,node_color='g',node_size=500,alpha=1)#Blau
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.listCheckOut,node_color='r',node_size=800,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.listDesconegudes,node_color='r',node_size=500,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.nodelistFormules,node_color='#1E90FF',node_size=500,node_shape='s',alpha=1)#Blue
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.listNovesVariablesFuncions,node_color='r',node_size=2000 ,alpha=1)
	equacio.nx.draw_networkx_edges(equacio.G,pos,edgelist=equacio.edgelist,width=4,alpha=1,edge_color='black')
	equacio.nx.draw_networkx_labels(equacio.G,pos,equacio.labels,font_size=16)
	equacio.plt.axis('off')
	equacio.plt.savefig(path)
	if(len(equacio.listPath)>1):
		equa=equacio.listPath[1]
		if(equa.num=="1"):
			image2=equacio.listPath.pop(1)
			try:os.remove("myproject/static/img/"+image2.path+".png")
			except:None
	equacio.listPath.insert(1,image(equacio.pathFoto,"1","Graf inicial amb valors"))#L'afegim a la posicio 0 perque és l'inicial

def dibuixarGrafInicialIgualacioValors():
	try:os.remove("myproject/static/img/"+equacio.pathFotoInicialIgualacioValors+".png")
	except:None
	equacio.plt.clf()
	temps=time.time()
	equacio.pathFotoInicialIgualacioValors=str(temps)+"_2"
	path = "myproject/static/img/"+equacio.pathFotoInicialIgualacioValors+".png"
	pos=equacio.nx.spring_layout(equacio.G)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.listConegudes,node_color='g',node_size=500,alpha=1)#Blau
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.listCheckOut,node_color='r',node_size=800,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.listDesconegudes,node_color='r',node_size=500,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.nodelistFormules,node_color='#1E90FF',node_size=500,node_shape='s',alpha=1)#Blue
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.listNovesVariablesFuncions,node_color='r',node_size=2000 ,alpha=1)
	equacio.nx.draw_networkx_edges(equacio.G,pos,edgelist=equacio.edgelist,width=4,alpha=1,edge_color='black')
	equacio.nx.draw_networkx_labels(equacio.G,pos,equacio.labels,font_size=16)
	equacio.plt.axis('off')
	equacio.nodeInicialIgualacioDibuixat=True
	equacio.plt.savefig(path)
	if(len(equacio.listPath)>2):
		equa=equacio.listPath[2]
		if(equa.num=="2"):
			image2=equacio.listPath.pop(2)
			try:os.remove("myproject/static/img/"+image2.pathFotoInicialIgualacioValors+".png")
			except:None
	equacio.listPath.insert(2,image(equacio.pathFotoInicialIgualacioValors,"2","Graf: unificació de variables per realitzar l'igualació"))#L'afegim a la posicio 0 perque és l'inicial

def dibuixarGrafComplertValors():
	num=len(equacio.listPath2)+1
	pas = str(len(equacio.listCheckOutValor)+1)
	equacio.plt.clf()
	temps=time.time()
	equacio.pathFotoValors=str(temps)+"_3"
	path = "myproject/static/img/"+equacio.pathFotoValors+".png"
	pos=equacio.nx.spring_layout(equacio.G)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.listConegudes,node_color='green',node_size=500,alpha=1)#Blau
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.listConegudesOutput,node_color='green',node_size=800,alpha=1)#Blau
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.listCheckOut,node_color='r',node_size=800,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.listDesconegudes,node_color='r',node_size=500,alpha=1)#Groc
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.nodelistFormules,node_color='#1E90FF',node_size=500,node_shape='s',alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.listNovesVariablesFuncions,node_color='r',node_size=2000 ,alpha=1)
	equacio.nx.draw_networkx_edges(equacio.G,pos,edgelist=equacio.edgelist,width=4,alpha=1,edge_color='black')
	equacio.nx.draw_networkx_labels(equacio.G,pos,equacio.labels,font_size=16)
	equacio.plt.axis('off')
	equacio.plt.savefig(path)
	if(len(equacio.listPath2)>=num):
		image2=equacio.listPath2.pop(num)
		try:os.remove("myproject/static/img/"+image2.path+".png")
		except:None
	equacio.listPath2.insert(num,image(equacio.pathFotoValors,str(num-3),"Graf amb tots els nodes"))#L'afegim a la posicio 0 perque és l'inicial

def dibuixarGrafIntermig(num,pas):#rep la llargada del listPath, que és la posició on ha d'anar l'imatge
	equacio.plt.clf()
	temps=time.time()
	equacio.pathFotoFinal=str(temps)+"_"+str(num)
	path = "myproject/static/img/"+equacio.pathFotoFinal+".png"
	pos=equacio.nx.spring_layout(equacio.GF)
	equacio.nx.draw_networkx_nodes(equacio.GF,pos,nodelist=equacio.nodelistVarDesOutPutPas,node_color='r',node_size=800,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.GF,pos,nodelist=equacio.nodelistVarDesNoOutPutPas,node_color='r',node_size=500,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.GF,pos,nodelist=equacio.nodelistVarConPas,node_color='green',node_size=500,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.GF,pos,nodelist=equacio.nodelistVarConPasOut,node_color='green',node_size=800,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.GF,pos,nodelist=equacio.nodelistFormulesPas,node_color='#1E90FF',node_size=500,node_shape='s',alpha=1)
	equacio.nx.draw_networkx_edges(equacio.GF,pos,edgelist=equacio.edgelistPas,width=4,alpha=0.8)
	equacio.nx.draw_networkx_labels(equacio.GF,pos,equacio.labelsPas,font_size=16)
	equacio.plt.axis('off')
	equacio.plt.savefig(path)
	if(len(equacio.listPath2)>=num):
		image2=equacio.listPath2.pop(num)
		try:os.remove("myproject/static/img/"+image2.path+".png")
		except:None
	equacio.listPath2.insert(num,image(equacio.pathFotoFinal,str(num-3),"Pas número: "+pas))

def dibuixarGrafUnica(num,pas):#rep la llargada del listPath2, que és la posició on ha d'anar l'imatge
	equacio.plt.clf()
	temps=time.time()
	equacio.pathFotoFinal=str(temps)+"_"+str(num)
	path = "myproject/static/img/"+equacio.pathFotoFinal+".png"
	pos=equacio.nx.spring_layout(equacio.G)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.nodelistConegudesUnica,node_color='green',node_size=500,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.listConegudesOutput,node_color='green',node_size=800,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.nodelistCheckOutUnica,node_color='r',node_size=800,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.nodelistDesconegudesUnica,node_color='r',node_size=500,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.nodelistFormules,node_color='#1E90FF',node_size=500,node_shape='s',alpha=1)#Blue
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.listNovesVariablesFuncions,node_color='r',node_size=2000 ,alpha=1)
	equacio.nx.draw_networkx_edges(equacio.G,pos,edgelist=equacio.edgeListVariablesNoUnica,width=4,alpha=0.8)
	equacio.nx.draw_networkx_edges(equacio.G,pos,edgelist=equacio.edgeListVariablesUnica,width=4,alpha=0.8,style='dashed')#dashed es descontinua
	equacio.nx.draw_networkx_labels(equacio.G,pos,equacio.labels,font_size=16)
	equacio.plt.axis('off')
	equacio.plt.savefig(path)
	if(len(equacio.listPath2)>=num):
		image2=equacio.listPath2.pop(num)
		try:os.remove("myproject/static/img/"+image2.path+".png")
		except:None
	equacio.listPath2.insert(num,image(equacio.pathFotoFinal,str(num-3),"Graf amb tots els nodes on s'indica el pas número: "+pas))

def dibuixarGrafUnica2(num,pas):#rep la llargada del listPath2, que és la posició on ha d'anar l'imatge
	equacio.plt.clf()
	temps=time.time()
	equacio.pathFotoFinal=str(temps)+"_"+str(num)
	path = "myproject/static/img/"+equacio.pathFotoFinal+".png"
	pos=equacio.nx.spring_layout(equacio.G)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.nodelistConegudesUnica,node_color='green',node_size=500,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.listConegudesOutput,node_color='green',node_size=800,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.nodelistCheckOutUnica,node_color='blue',node_size=800,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.nodelistDesconegudesUnica,node_color='r',node_size=500,alpha=1)
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.nodelistFormules,node_color='#1E90FF',node_size=500,node_shape='s',alpha=1)#Blue
	equacio.nx.draw_networkx_nodes(equacio.G,pos,nodelist=equacio.listNovesVariablesFuncions,node_color='r',node_size=2000 ,alpha=1)
	equacio.nx.draw_networkx_edges(equacio.G,pos,edgelist=equacio.edgeListVariablesNoUnica,width=4,alpha=0.8)
	equacio.nx.draw_networkx_edges(equacio.G,pos,edgelist=equacio.edgeListVariablesUnica,width=4,alpha=0.8)#dashed es descontinua
	equacio.nx.draw_networkx_labels(equacio.G,pos,equacio.labels,font_size=16)
	equacio.plt.axis('off')
	equacio.plt.savefig(path)
	if(len(equacio.listPath2)>=num):
		image2=equacio.listPath2.pop(num)
		try:os.remove("myproject/static/img/"+image2.path+".png")
		except:None
	equacio.listPath2.insert(num,image(equacio.pathFotoFinal,str(num-3),"Graf final"))

#Metode inicial per buscar les solucions dels outputs.
def buscarCheckOuts(large):
	for out in equacio.listCheckOut:
		equacio.calcularMesFormules = False
		equacio.grau=0#Posem el grau a 0
		valor_Bool=calcularCami(out)
		if(valor_Bool):
			if(len(equacio.listCheckOut)>0):#Si hi ha checkouts a buscar
				if(large!=len(equacio.listCheckOut)):#Si la llargada es diferent seguim la recursivitat, sinó la finalitzem
					buscarCheckOuts(len(equacio.listCheckOut))#Segona recursivitat amb els outputs
		else:
			if(len(equacio.listCheckOut)>0):
				if(large!=len(equacio.listCheckOut)):#Si la llargada es diferent seguim la recursivitat, sinó la finalitzem
					buscarCheckOuts(len(equacio.listCheckOut))#Segona recursivitat amb els outputs


def reiniciarValors():
	equacio.equacioCanonica = ""#equacio canònica
	equacio.equacioInicial=""#Equacio inicial
	equacio.partEsq = ""#part del canto esquerre de l'equacio
	equacio.partDre = ""#part del canto dret de l'equacio
	equacio.num=""#Número que identificarà l'equació al graf
	equacio.pathFoto = None #Path foto graf complert
	equacio.pathFotoFinal = None #Path foto graf resolt
	equacio.pathFotoInicial = None
	equacio.pathFotoValors = None
	equacio.pathFotoInicialIgualacio = None
	equacio.pathFotoInicialIgualacioValors = None
	equacio.nodeInicialDibuixat=False#Variable per controlar si s'ha dibuixat o no
	equacio.nodeInicialIgualacioDibuixat=False

	#Llistats per els templates
	equacio.llistat=[]#Llistat on guardem totes les variables
	equacio.llistatEquacions=[]#Llista amb totes les equacions vistes, amb el número de label i la seva canònica#ARRAY

	#Grafs
	equacio.GI = equacio.nx.Graph()#Graf inicial que contindrà les equacions introduides per l'usuari
	equacio.G = equacio.nx.Graph()#Graf complert
	equacio.GV = equacio.nx.Graph()#Graf unicament amb variables per a tractarles
	equacio.GF = equacio.nx.Graph()#Graf pas a pas

	#Llistes i diccionaris per crear el Graf
	equacio.nodelistVariables=[]#Aqui guardarem tots els nodes variable
	equacio.nodelistFormules=[]#Aquí guardarem tots els nodes formula
	equacio.edgelist=[]#Aquí guardarem tots els enllaços dels nodes variables als nodes formules
	equacio.labels={}


	equacio.listRelacioEdgesNovesFormules=[]
	equacio.listNovesFormules=[]
	equacio.listNovesVariablesFuncions=[]

	#Borrem imatges en cas que ja n'haguem creat
	if(len(equacio.listPath)>0):
		for valor in equacio.listPath:
			try:os.remove("myproject/static/img/"+valor.path+".png")
			except:None
	equacio.listPath=[]#Borrem els paths anteriors
	if(len(equacio.listPath2)>0):
		for valor in equacio.listPath2:
			try:os.remove("myproject/static/img/"+valor.path+".png")
			except:None
	equacio.listPath2=[]#Borrem els paths anteriors

	#Llistes i diccionaris per crear el Graf
	equacio.nodelistVarConFinal=[]#Aqui guardarem tots els nodes inputs utilitzats
	equacio.nodelistVarDesFinal=[]#Aqui guardarem tots els nodes que hem trobat solució que eren desconeguts
	equacio.nodelistVarOutputsFinal=[]#Aqui guardarem tots els nodes outputs trobats
	equacio.nodelistFormulesFinal=[]#Aquí guardarem tots els nodes formula utilitzats
	equacio.edgelistFinal=[]#Aquí guardarem tots els enllaços dels nodes variables als nodes formules
	equacio.edgelistCamiFinal=[]#Enllaços del camí
	equacio.labelsFinal={}#Valor que posarem als nodes

	#LListes per resoldre els problemes
	equacio.listCheckInValor=[]#Llista on guardarem les variables INPUTS amb els seus valors
	equacio.listCheckOut=[]#Llista on guardarem quines variables son OUTPUTS
	equacio.listCheckOutValor=[]#Llista on guardarem les variables OUTPUTS amb els seus valors#ARRAY
	equacio.listDesconegudes=[]#LLista on guardarem les variables que desconeixem
	equacio.listConegudes=[]#Llista de conegudes
	equacio.listConegudesTotalsValor=[]#Llista on guardarem totes les variables que en sabem els valors
	equacio.listFormulesGrau=[]#Llista on guardarem el grau de les formules, el terme grau es les variables que desconeixem el valor
	equacio.grau=0#Grau en que ens trobarem per resoldre les equacions
	equacio.llargadaCheckOut=0#Variable per finalitzar la recursivitat

#Metode que agafar els checkIn,checkOut,desconegudes i dona valors als checkIn
def agafarValors(p):
	for i in equacio.nodelistVariables:
		if not(i in equacio.listNovesVariablesFuncions):
			#i es la variable
			#p[i] es el valor de la variable i
			valor=p[i]
			if(len(valor)>0):#Si te valor positiu(+gran que 0)
				if valor.isdigit():#Si es un numero es correcte
					equacio.listCheckInValor.append((i,p[i]))#Afegim la variable amb el seu valor
					equacio.listConegudesTotalsValor.append((i,p[i]))#Afegim la variable amb el seu valor
					equacio.listConegudes.append(i)
				else:
					if(valor[0]=="-")|(valor[0]=="+"):
						if(valor[1:len(valor)].isdigit()):#si porta simbol i es un numero
							equacio.listCheckInValor.append((i,p[i]))#Afegim la variable amb el seu valor
							equacio.listConegudesTotalsValor.append((i,p[i]))#Afegim la variable amb el seu valor
							equacio.listConegudes.append(i)
						else:return False
					else:return False
			else:
				if not(i in equacio.listCheckOut):#Si no es troba ni en inputs ni en outputs
					equacio.listDesconegudes.append(i)#Afegim la variable a la llista de desconegudes
			#i=symbols(i)#Afegim les variables a la biblioteca sympy
	return True

#Mètode que inicia la cerca de la solució d'una variable.
def calcularVariable(var,out):
	listPossiblesCaminsVar=equacio.G.neighbors(var)#Retorna les formules amb les que esta enllaçat
	listPossiblesCaminsOut=equacio.G.neighbors(out)
	for posCami in listPossiblesCaminsVar:
		if not(posCami in listPossiblesCaminsOut):#Si no es una equació on hi hagi l'output
			valor_Bool=mirarNivell(posCami,var)#Retorna True si out ja te valor, si no s'ha pogut calcular retorna False
			if(valor_Bool):
				return True
			else:
				return False
	return False

#Metode que recorre tots els possibles camins
def calcularCami(out):
	listPossiblesCamins=equacio.G.neighbors(out)#Retorna les formules amb les que esta enllaçat
	for posCami in listPossiblesCamins:
		valor_Bool=mirarNivell(posCami,out)#Retorna True si out ja te valor, si no s'ha pogut calcular retorna False
		if(valor_Bool):
			equacio.listFormulesGrau=[]#Posem el valor buit per seguretat
			return True#Perque ja hem trobat el valor de out
		else:
			contador=0
			cont=0
			listForm=equacio.listFormulesGrau#Variable que guardem perque anirem borrant i modificant
			for opcio in listForm:#Per cadascuna de les opcions
				if(len(listForm[cont][2])>0):#Si hi ha minim una variable
					for var in listForm[cont][2]:#Per cadascuna de les variables
						booleano=calcularVariable(var,out)#Si es resolt retorna true, sino false
						if(booleano):contador=contador+1#Aumentem el contador
				if(contador>0):#Vol dir que s'ha resolt minim una variable de l'opció
					booleano = calcularCami(out)#Tornem a mirar de calcular el out
					if(booleano):
						if(opcio in equacio.listFormulesGrau):
							equacio.listFormulesGrau.remove(opcio)#Eliminem l'element que busquem ja el camí
						return booleano#Si es True ho retornem(hem trobat la solucio), sino no
				else:#Si no hem pogut resoldre les variables individualmente mirem de fer-ho conjuntament
					if(listForm[cont][1]>1):#Si el grau es mes gran que 1
						if(equacio.calcularMesFormules == False):
							mesFormules = miremFormulesComu(posCami,listForm[cont][1],listForm[cont][2],out)#Formula,grau,variables desconegudes i sortida
							booleano = calcularCami(out)#Recursivitat
							if(booleano):return booleano
				cont=cont+1#Anem a per la seguent opcio
				if(opcio in equacio.listFormulesGrau):equacio.listFormulesGrau.remove(opcio)#Eliminem l'element que busquem ja el camí
	return False#No es possible calcular aquesta opcio

#Mirem quines variables coneixem, ens passa la formula i el checkOut
def mirarNivell(posCami,out):
	equacio.grau=equacio.grau+1#Aumentem el grau
	equacio.listFormulesGrau=[]
	listEdgesFormula = equacio.G.neighbors(posCami)
	grau=0#Variable local
	checkOut=False#Booleà que si hi ha una variable checkout, per tal de que no ho resolgui
	listGrau=[]#Llista amb totes les desconegudes de l'equació
	for edge in listEdgesFormula:
		if(edge != out):
			if not(edge in equacio.listConegudes):
				if not(edge in equacio.listCheckOut):
					grau=grau+1#Si la variable no tiene valor aumentamos el grado
					listGrau.append(edge)
				else:
					checkOut=True
	#Si grau es mes gran que 0 vol dir que no es pot resoldre
	if((grau==0) and (not checkOut) and (not out in equacio.listNovesVariablesFuncions)):#Si tenim grau = 0 vol dir que podem resoldre
		return resoltEquacio(posCami,out)#Metode per resoldre l'equació
	else:
		if(not checkOut):
			if not((posCami,grau,listGrau) in equacio.listFormulesGrau):
				equacio.listFormulesGrau.append((posCami,grau,listGrau))#Afegim a la llista el grau amb la formula i les desconegudes
	return False#Perque no hem resolt l'equació

#Metode que troba les formules en comú de les variables que desconeixem
def miremFormulesComu(posCami,grau,listGrau,out):
	equacio.calcularMesFormules = True #Posem que ja ho hem calculat per no tenir un bucle infinit
	listEdgesFinals = []#Llista on guardarem les formules on apareixen les variables desconegudes
	listEdgesFirstVar = equacio.G.neighbors(listGrau[0])#Formules de la primera variable
	for var in listGrau[1:len(listGrau)]:#Del segon fins al final
		listEdgesVar=equacio.G.neighbors(var)#Agafem les formules de la variable var
		for edge in listEdgesVar:
			if(edge in listEdgesFirstVar):#Si es troben en les dos llistes es una formula final
				if not(edge in listEdgesFinals):
					listEdgesFinals.append(edge)
	#un cop tenim les formules, al ser una canònica l'hem de girar els signes perquè pot tenir dos opcions
	listExtra=[]
	for edge in listEdgesFinals:
		edge2=canonicaEdge(edge)
		listExtra.append(edge2)
	for edgeExtra in listExtra:#Afegim els extres a la llista final
		listEdgesFinals.append(edgeExtra)
	return creemNovesFormules(listEdgesFinals,grau,listGrau,out)

def reiniciarValorsPasAPas():
	nodelistVarDesOutPutPas=[]
	nodelistVarDesNoOutPutPas=[]
	equacio.nodelistVarConPas=[]
	equacio.nodelistVarConPasOut=[]
	equacio.nodelistFormulesPas=[]
	equacio.edgelistPas=[]
	equacio.labelsPas={}


#Metode que resolt l'equació posCami amb sortida a out
def resoltEquacio(posCami, out):
	dibuixarGrafComplertValors()
	posCamiNoModificat=posCami#Doblem la variable perque a la posCami la modificarem donant valor a les variables que coneixem
	if out in equacio.listNovesVariablesFuncions: return False#Si es una funcio no es pot solucionar!

	#Graf pas a pas->Afegim l'output i la formula
	reiniciarValorsPasAPas()
	if(out in equacio.listCheckOutFixa):
		if not (out in equacio.nodelistVarDesOutPutPas):equacio.nodelistVarDesOutPutPas.append(out)
	else:
		if not (out in equacio.nodelistVarDesNoOutPutPas):equacio.nodelistVarDesNoOutPutPas.append(out)
	if not (posCami in equacio.nodelistFormulesPas):equacio.nodelistFormulesPas.append(posCamiNoModificat)


	equacio.edgeListVariablesUnica=[]#Reiniciem valors
	equacio.edgeListVariablesUnica.append((out,posCamiNoModificat))#Afegim el edge que anirà discontinu al G Previ
	listVariables=equacio.G.neighbors(posCami)#Agafem els enllaços de la equacio, és a dir, les variables
	cont=0
	for var in equacio.listConegudesTotalsValor:#Recorrem els valors
		if(equacio.listConegudesTotalsValor[cont][0] in listVariables):
			#Canviem la variable pel seu valor
			valor=equacio.listConegudesTotalsValor[cont][1]
			if(valor<0):#Si es un valor negatiu ho fiquem entre parèntesi perquè no afecti el signe de davant
				valor="("+valor+")"
				posCami = string.replace(posCami, equacio.listConegudesTotalsValor[cont][0], valor)
				if not (equacio.listConegudesTotalsValor[cont][0] in equacio.nodelistVarConPas):
					if(equacio.listConegudesTotalsValor[cont][0] in equacio.listCheckOutFixa):
						if not (equacio.listConegudesTotalsValor[cont][0] in equacio.nodelistVarConPasOut):equacio.nodelistVarConPasOut.append(equacio.listConegudesTotalsValor[cont][0])#Graf pas a pas
					else:
						if not (equacio.listConegudesTotalsValor[cont][0] in equacio.nodelistVarConPas):equacio.nodelistVarConPas.append(equacio.listConegudesTotalsValor[cont][0])
					equacio.GF.add_node(equacio.listConegudesTotalsValor[cont][0])
					equacio.GF.add_edge(posCamiNoModificat,equacio.listConegudesTotalsValor[cont][0])
					equacio.labelsPas[equacio.listConegudesTotalsValor[cont][0]]=equacio.listConegudesTotalsValor[cont][0]
				equacio.edgelistPas.append((equacio.listConegudesTotalsValor[cont][0],posCamiNoModificat))
			
				equacio.edgeListVariablesUnica.append((equacio.listConegudesTotalsValor[cont][0],posCamiNoModificat))#Afegim el edge que anirà discontinu al GF Previ
				
				#Graf pas a pas->Afegim la variable i el seu enllaç
				#equacio.edgelistPas.append((equacio.listConegudesTotalsValor[cont][0],posCamiNoModificat))#Graf pas a pas
				

				#Graf			
				outUni=unicode(equacio.listConegudesTotalsValor[cont][0])
				if not(equacio.listConegudesTotalsValor[cont][0] in equacio.nodelistVarConFinal):
					if not(equacio.listConegudesTotalsValor[cont][0] in equacio.nodelistVarDesFinal):
						if not(equacio.listConegudesTotalsValor[cont][0] in equacio.nodelistVarOutputsFinal):
							equacio.GF.add_node(equacio.listConegudesTotalsValor[cont][0])#Afegim la variable i l'enllaç al graf
							equacio.GF.add_edge(posCamiNoModificat,equacio.listConegudesTotalsValor[cont][0])
							equacio.nodelistVarConFinal.append(equacio.listConegudesTotalsValor[cont][0])#Afegim l'equació coneguda a utilitzada
							equacio.labelsFinal[equacio.listConegudesTotalsValor[cont][0]]=equacio.listConegudesTotalsValor[cont][0]
				if (equacio.listConegudesTotalsValor[cont][0] in equacio.nodelistVarDesFinal):
					equacio.edgelistCamiFinal.append((equacio.listConegudesTotalsValor[cont][0],posCamiNoModificat))#Afegim l'enllaç
				else:
					equacio.edgelistFinal.append((equacio.listConegudesTotalsValor[cont][0],posCamiNoModificat))#Afegim l'enllaç
			else:
				posCami = string.replace(posCami, equacio.listConegudesTotalsValor[cont][0], valor)
				if not (equacio.listConegudesTotalsValor[cont][0] in equacio.nodelistVarConPas):
					if(equacio.listConegudesTotalsValor[cont][0] in equacio.listCheckOutFixa):
						if not (equacio.listConegudesTotalsValor[cont][0] in equacio.nodelistVarConPasOut):equacio.nodelistVarConPasOut.append(equacio.listConegudesTotalsValor[cont][0])#Graf pas a pas
					else:
						if not (equacio.listConegudesTotalsValor[cont][0] in equacio.nodelistVarConPas):equacio.nodelistVarConPas.append(equacio.listConegudesTotalsValor[cont][0])
					equacio.GF.add_node(equacio.listConegudesTotalsValor[cont][0])
					equacio.GF.add_edge(posCamiNoModificat,equacio.listConegudesTotalsValor[cont][0])
					equacio.labelsPas[equacio.listConegudesTotalsValor[cont][0]]=equacio.listConegudesTotalsValor[cont][0]
				equacio.edgelistPas.append((equacio.listConegudesTotalsValor[cont][0],posCamiNoModificat))
				equacio.edgeListVariablesUnica.append((equacio.listConegudesTotalsValor[cont][0],posCamiNoModificat))#Afegim el edge que anirà discontinu al GF Previ				

				#Graf
				outUni=unicode(equacio.listConegudesTotalsValor[cont][0])
				if not(equacio.listConegudesTotalsValor[cont][0] in equacio.nodelistVarConFinal):
					if not(equacio.listConegudesTotalsValor[cont][0] in equacio.nodelistVarDesFinal):
						if not(equacio.listConegudesTotalsValor[cont][0] in equacio.nodelistVarOutputsFinal):
							equacio.GF.add_node(equacio.listConegudesTotalsValor[cont][0])#Afegim la variable i l'enllaç al graf
							equacio.GF.add_edge(posCamiNoModificat,equacio.listConegudesTotalsValor[cont][0])
							equacio.nodelistVarConFinal.append(equacio.listConegudesTotalsValor[cont][0])#Afegim la variable coneguda a utilitzada
							equacio.labelsFinal[equacio.listConegudesTotalsValor[cont][0]]=equacio.listConegudesTotalsValor[cont][0]
							#equacio.labelsPas[equacio.listConegudesTotalsValor[cont][0]]=equacio.listConegudesTotalsValor[cont][0]
							if not (equacio.listConegudesTotalsValor[cont][0] in equacio.nodelistVarConPas):
								if(equacio.listConegudesTotalsValor[cont][0] in equacio.listCheckOutFixa):
									if not (equacio.listConegudesTotalsValor[cont][0] in equacio.nodelistVarConPasOut):equacio.nodelistVarConPasOut.append(equacio.listConegudesTotalsValor[cont][0])#Graf pas a pas
								else:
									if not (equacio.listConegudesTotalsValor[cont][0] in equacio.nodelistVarConPas):equacio.nodelistVarConPas.append(equacio.listConegudesTotalsValor[cont][0])
								#equacio.nodelistVarConPas.append(equacio.listConegudesTotalsValor[cont][0])
								equacio.GF.add_node(equacio.listConegudesTotalsValor[cont][0])
								equacio.GF.add_edge(posCamiNoModificat,equacio.listConegudesTotalsValor[cont][0])
				if (equacio.listConegudesTotalsValor[cont][0] in equacio.nodelistVarDesFinal):
					equacio.edgelistCamiFinal.append((equacio.listConegudesTotalsValor[cont][0],posCamiNoModificat))#Afegim l'enllaç
				else:
					equacio.edgelistFinal.append((equacio.listConegudesTotalsValor[cont][0],posCamiNoModificat))#Afegim l'enllaç
		cont=cont+1
	d=solve(posCami,out)#Fem el càlcul de la fòrmula
	equacio.calcularMesFormules=False#Posem la variable a False perquè es puguin tornar a crear més fórmules

	#Dibuixar graf Unica
	if(out in equacio.listCheckOutFixa):equacio.listConegudesOutput.append(out)
	#dibuixarGrafIntermig(len(equacio.listCheckOutValor)+1)
	equacio.edgeListVariablesNoUnica=[x[:] for x in equacio.edgelist]#Dupliquem la llista

	for edge in equacio.edgeListVariablesUnica:
		exist=True
		while (exist):
			if edge in equacio.edgeListVariablesNoUnica:
				equacio.edgeListVariablesNoUnica.remove(edge)
			else:
				exist=False


	llarg=len(equacio.listPath2)+1
	numOpe = str(len(equacio.listCheckOutValor)+1)
	numFor=str(equacio.nodelistFormules.index(posCamiNoModificat)+1)
	
	#Graf anterior al pas
	#Primer el dibuixem
	#Després modifiquem les llistes, posant la variable trobada a conegudes.
	dibuixarGrafUnica(llarg,numOpe)
	if(out in equacio.nodelistCheckOutUnica):equacio.nodelistCheckOutUnica.remove(out)
	if(out in equacio.nodelistDesconegudesUnica):equacio.nodelistDesconegudesUnica.remove(out)
	if not (out in equacio.nodelistConegudesUnica):equacio.nodelistConegudesUnica.append(out)

	#Graf pas a pas
	equacio.nodelistFormulesFinal.append(posCamiNoModificat)#Afegim l'equació coneguda a utilitzada
	equacio.labelsFinal[posCamiNoModificat]=numFor#Posem el número de fórmula al graf
	equacio.GF.add_node(out)#Afegim la variable i l'enllaç al graf
	equacio.GF.add_edge(posCamiNoModificat,out)
	equacio.edgelistPas.append((out,posCamiNoModificat))#Graf pas a pas
	equacio.labelsPas[posCamiNoModificat]=numFor

	#No es necessari pero posem el signe negatiu entre parèntesi per facilitar l'entesa del funcionament del resultat
	if(d[0]<0):#Si es un valor negatiu ho fiquem entre parèntesi perquè no afecti el signe de davant
		d="("+unicode(d[0])+")"
	else:
		d=unicode(d[0])

	x=str(equacio.nodelistFormules.index(posCamiNoModificat)+1)

	equacio.listCheckOutValor.append(resultat(out,d,posCami,numOpe,posCamiNoModificat,x))#Afegim la variable,valor,operació feta, número d'operació i quina equació és
	equacio.listCheckInValor.append((out,d))#Afegim la variable amb el seu valor
	equacio.listConegudesTotalsValor.append((out,d))#Afegim la variable amb el seu valor
	equacio.listConegudes.append(out)
	if(out in equacio.listCheckOut):
		equacio.listCheckOut.remove(out)#Eliminem de la llista de checkOut el valor trobat
		#Graf
		equacio.nodelistVarOutputsFinal.append(out)#Afegim el output a la llista pel graf final
		equacio.edgelistCamiFinal.append((out,posCamiNoModificat))#Afegim l'enllaç
		equacio.labelsFinal[out]=out
		equacio.labelsPas[out]=out
	else:
		#Graf
		equacio.nodelistVarDesFinal.append(out)#Afegim desconeguda resolta a la llista pel graf final
		equacio.edgelistCamiFinal.append((out,posCamiNoModificat))#Afegim l'enllaç
		equacio.labelsFinal[out]=out
		equacio.labelsPas[out]=out

	#Dibuixar graf intermitg i reiniciar-lo pel seguent pas
	dibuixarGrafIntermig(llarg+1,numOpe)
	equacio.GF = equacio.nx.Graph()

	if(out in equacio.nodelistVarDesFinal):equacio.nodelistVarDesFinal.remove(out)
	if(out in equacio.nodelistVarOutputsFinal):equacio.nodelistVarOutputsFinal.remove(out)
	if not (out in equacio.nodelistVarConFinal):equacio.nodelistVarConFinal.append(out)
	for edge in equacio.edgelistCamiFinal:
		equacio.edgelistFinal.append(edge)
		equacio.edgelistCamiFinal.remove(edge)

	return True#Retornem true perque ho hem calculat


#Metode que torna a crear el graf complert ja que al passar de pàgina html es neteja
def reanudarGraf():
	for var in equacio.nodelistVariables:
		equacio.G.add_node(var)
		equacio.GI.add_node(var)
	for equ in equacio.nodelistFormules:
		equacio.G.add_node(equ)
		equacio.GI.add_node(equ)
	cont=0
	for edge in equacio.edgelist:
		#Afegim cada variable amb la seva formula corresponent
		equacio.G.add_edge(equacio.edgelist[cont][0],equacio.edgelist[cont][1])
		equacio.GI.add_edge(equacio.edgelist[cont][0],equacio.edgelist[cont][1])
		cont=cont+1

#Mètode que separa la part esquera de la dreta de l'equacio
def separacio():
	i = 0
	for x in equacio.equacioInicial:
		if(x!='='):
			i=i+1
		else:
			equacio.partEsq=equacio.equacioInicial[0:i]
			equacio.partDre=equacio.equacioInicial[i+1:len(equacio.equacioInicial)]
			return True#Hi ha =
	#Control en cas que no hi hagi un =
	equacio.partEsq=""
	equacio.partDre=equacio.equacioInicial
	return False#No te =

#Mètode que crea l'equació canònica
def canonica():
	if(equacio.partEsq!=''):
		can = ""
		if((equacio.equacioInicial[0:1]!= '+') | (equacio.equacioInicial[0:1]!= '-')):
			can = '-'
		for x in equacio.partEsq:
			if(x=='+'):
				can = can+'-'
			elif(x=='-'):
				can = can+'+'
			else:
				can = can+x
		equacio.equacioCanonica = equacio.partDre + can
	return

#mètode que crea l'equació canònica d'un enllaç, que es una equacio
def canonicaEdge(edge):
	can=""
	d=edge[0]
	if (d!='+') & (d!='-'):edge="+"+edge
	for x in edge:
		if(x=='+'):
			can = can+'-'
		elif(x=='-'):
			can = can+'+'
		else:
			can = can+x
	return can

#mètode que crea l'equació canònica d'un enllaç, que es una equacio
def invertida(edge):
	can=""
	d=edge[0]
	if (d=='-'):
		edge=edge[1:len(edge)]
	for x in edge:
		if(x=='+'):
			can = can+'-'
		elif(x=='-'):
			can = can+'+'
		else:
			can = can+x
	return can

#Mètode que retorna el signe contrari
def canviarSigne(signe):
	if('+' in signe):
		return "-"
	elif('-' in signe):
		return "+"
	elif('*' in signe):
		return "/"
	elif('/' in signe):
		return "*"
	else:return "0"#perque vol dir que no te re

#metode que crear noves formules per igualació
def creemNovesFormules(listEdgesFinals,grau,listGrau,out):
	siTenimMesFormules = False
	import networkx as nx
	import matplotlib.pyplot as plt
	GNF = nx.Graph()#Graf complert local de les noves fórmules
	listGlobal=[]#Llista on guardarem las variables amb els seus simbols per fer les possibles combinacions
	listGlobalValor=[]
	listPrimera=[]#Llista on guardarem les variables primera, que ens serviran per fer tria de quines si i quines no.
	listDretes=[]#Llista on guardarem les dretes a igualar
	booleanPrimer=True
	for edge in listEdgesFinals[0:len(listEdgesFinals)]:#Del primer fins al final
		esquerra=""
		dreta=""
		var=""#Guardaremos la variable
		varAlter=""
		simbolo=""#Guardaremos el simbolo
		listAfegir=[]
		booleanoNum=False
		primer=edge[0]
		for x in edge:
			if (x!='*') & (x!='/') & (x!='+') & (x!='-') & (x!='^') & (x!='(') & (x!=')') & (not x.isdigit()):
				var=var+x
				varAlter=""
			elif(x.isdigit()):
				varAlter=varAlter+x
				booleanoNum=True
			else:
				if(booleanoNum):
					dreta=dreta+simbolo+varAlter
					booleanoNum=False
				else:
					if(len(var)>0):#Si var te valor
						if(var in listGrau):#Si es troba a la listGrau, passa a l'esquerra
							simbolo=canviarSigne(simbolo)
							if(len(esquerra)==0) & (simbolo=="0"):simbolo="-"
							esquerra=esquerra+simbolo+var
							if(simbolo+var in listPrimera):
								listGlobal.append(simbolo+var)
								listAfegir.append(simbolo+var)
							simbolo=""
						else:
							if(len(var)>0):
								dreta=dreta+simbolo+var
								simbolo=""
							else:
								dreta=dreta
								simbolo=""

					else:
						dreta=dreta+varAlter
					simbolo=simbolo+x#Per la seguent variable
					var=""
					varAlter=""
		if(len(var)>0):#Si var te valor
			if(var in listGrau):#Si es troba a la listGrau, passa a l'esquerra
				simbolo=canviarSigne(simbolo)
				if(len(esquerra)==0) & (simbolo=="0"):simbolo="-"
				esquerra=esquerra+simbolo+var
				if(simbolo+var in listPrimera):
					listGlobal.append(simbolo+var)
					listGlobalValor.append((simbolo+var,edge))
				simbolo=""
			else:
				dreta=dreta+simbolo+var
				simbolo=""
		for var in listAfegir:
			listGlobalValor.append((var,edge,dreta))
			if not(dreta in listDretes):listDretes.append(dreta)
		#Guardem d'on provenen les esquerres i les dretes
		equacio.listRelacioEdgesNovesFormules.append(relacio(esquerra,edge))
		equacio.listRelacioEdgesNovesFormules.append(relacio(dreta,edge))
		GNF.add_edge(esquerra,dreta)
		if not(esquerra in listGlobal):listGlobal.append(esquerra)
	for node in listGlobal:#Per cadascun dels nous nodes
		if(len(GNF.neighbors(node))>0):#Si te més d'una dreta
			llista1 = GNF.neighbors(node)#Primera llista que igualarem amb la segona
			llista2 = GNF.neighbors(node)
			for dreta1 in llista1:
				for dreta2 in llista2:
					if(dreta1 != dreta2):
						siTenimMesFormules = True
						equacio.equacioInicial=dreta1+"="+dreta2
						#Extreiem els valors per la taula
						valor1=""
						valor2=""
						valor1Ca=""
						valor2Ca=""
						numEqua1=""
						numEqua2=""
						for edge in equacio.listRelacioEdgesNovesFormules:#Per cadascuna de les relacions
							if(dreta1==edge.valor):#Si es la dreta 1
								edgeInvertit=invertida(edge.canonica)#Edge invertit per poder fer la comparació
								for equa in equacio.llistatEquacions:#mirem del llista d'equacions
									if(equa.canonica==edge.canonica):#si coincideixen les canoniques
										valor1=equa.equacio
										valor1Ca=equa.canonica
										numEqua1=equa.num
									elif(equa.canonica==edgeInvertit):#si coincideixen les canoniques
										valor1=equa.equacio
										valor1Ca=equa.canonica
										numEqua1=equa.num
							if(dreta2==edge.valor):#Si es la dreta 2
								edgeInvertit=invertida(edge.canonica)
								for equa in equacio.llistatEquacions:#mirem del llista d'equacions
									if(equa.canonica==edge.canonica):#si coincideixen les canoniques
										valor2=equa.equacio
										valor2Ca=equa.canonica
										numEqua2=equa.num
									elif(equa.canonica==edgeInvertit):#si coincideixen les canoniques
										valor2=equa.equacio
										valor2Ca=equa.canonica
										numEqua2=equa.num
						equacio.listNovesFormules.append(igualacio(equacio.equacioInicial,len(equacio.nodelistFormules)+1,valor1,numEqua1,valor2,numEqua2))
						if(valor1Ca!="") & (valor2Ca!=""):
							modificarVariablesIgualacio(node,valor1Ca,valor2Ca)
							trobat=True
						if(equacio.nodeInicialIgualacioDibuixat==False):
							dibuixarGrafInicialIgualacioValors()
						equacio.equacioCanonica=""
						equacio.partEsq=dreta1
						equacio.partDre=dreta2
						equacio.num=str(len(equacio.listFormulesGrau))
						canonica()
						variablesIndividualsNoves(equacio.equacioInicial)
				llista2.remove(dreta1)#Borrem de la llista 2 la variable que ja hem igualat amb totes les possibles opcions
	if siTenimMesFormules:#Si es true dibuixem el graf perque vol dir que em afegit mes formules
		return siTenimMesFormules
	else:#sino false i no podem fer res mes
		return siTenimMesFormules

#Metode que crea la variable nova funció que englobarà les variables desconegudes
def modificarVariablesIgualacio(node,valor1Ca,valor2Ca):
	variables=[]
	var=""
	varFinal=""
	for x in node:
		if (x!='*') & (x!='/') & (x!='+') & (x!='-') & (x!='^') & (x!='=') & (x!='(') & (x!=')') & (not x.isdigit()):
			var=var+x
			varAlter=""
		else:
			if(len(var)!=0):
				variables.append(var)
				if(len(varFinal)==0):varFinal=var
				else: varFinal=varFinal+","+var
				var=""
	if(len(var)!=0):
		variables.append(var)
		if(len(varFinal)==0):varFinal=var
		else: varFinal=varFinal+","+var
	varFinal="f("+varFinal+")"
	equacio.listNovesVariablesFuncions.append(varFinal)
	modificarGraf(variables,valor1Ca,valor2Ca,varFinal)

#Eliminem les variables que fan igualacio
def modificarGraf(variables,valor1Ca,valor2Ca,varFinal):
	valor1Ca= unicode(valor1Ca)
	valor2Ca= unicode(valor2Ca)
	varFinal= unicode(varFinal)
	for var in variables:
		if(var in equacio.labels):
			del equacio.labels[var]
		var = unicode(var)
		edge1="("+unicode(valor1Ca)+","+unicode(var)+")"
		edge2="("+unicode(valor2Ca)+","+unicode(var)+")"
		edge3="("+unicode(var)+","+unicode(valor1Ca)+")"
		edge4="("+unicode(var)+","+unicode(valor2Ca)+")"
		nodes=equacio.G.nodes()
		if var in nodes:
			try:
				equacio.G.remove_edge(valor1Ca,var)
				equacio.G.remove_edge(valor2Ca,var)
				equacio.G.remove_node(var)
			except Exception, e:
				raise


		#if(len(equacio.G.neighbors(var))==2):
		if( var in equacio.llistat):equacio.llistat.remove(var)#Nomes esta enllaçat amb les equacions d'igualacio
		if( var in equacio.nodelistVariables):equacio.nodelistVariables.remove(var)
		if( var in equacio.listDesconegudes):equacio.listDesconegudes.remove(var)
		if( var in equacio.nodelistVarDesFinal):equacio.nodelistVarDesFinal.remove(var)
		if( var in equacio.nodelistDesconegudesUnica):equacio.nodelistDesconegudesUnica.remove(var)

		list2=[x[:] for x in equacio.edgelist]#Dupliquem la llista
		for edgeLi in list2:
			booleano=False
			if edgeLi[0]==var:
				if(edgeLi[1]==valor1Ca):booleano=True
				elif(edgeLi[1]==valor2Ca):booleano=True
			if(booleano):
				booleano=False
				equacio.edgelist.remove(edgeLi)

		if( edge1 in equacio.edgelist):equacio.edgelist.remove(edge1)
		if( edge2 in equacio.edgelist):equacio.edgelist.remove(edge1)
		if( edge1 in equacio.edgelistFinal):equacio.edgelistFinal.remove(edge1)
		if( edge2 in equacio.edgelistFinal):equacio.edgelistFinal.remove(edge2)
		if( edge1 in equacio.edgelistCamiFinal):equacio.edgelistCamiFinal.remove(edge1)
		if( edge2 in equacio.edgelistCamiFinal):equacio.edgelistCamiFinal.remove(edge2)
		if( edge1 in equacio.edgeListVariablesUnica):equacio.edgeListVariablesUnica.remove(edge1)
		if( edge2 in equacio.edgeListVariablesUnica):equacio.edgeListVariablesUnica.remove(edge2)
		if( edge1 in equacio.edgeListVariablesNoUnica):equacio.edgeListVariablesNoUnica.remove(edge1)
		if( edge2 in equacio.edgeListVariablesNoUnica):equacio.edgeListVariablesNoUnica.remove(edge2)
		if( edge3 in equacio.edgelist):equacio.edgelist.remove(edge3)
		if( edge4 in equacio.edgelist):equacio.edgelist.remove(edge4)
		if( edge3 in equacio.edgelistFinal):equacio.edgelistFinal.remove(edge3)
		if( edge4 in equacio.edgelistFinal):equacio.edgelistFinal.remove(edge4)
		if( edge3 in equacio.edgelistCamiFinal):equacio.edgelistCamiFinal.remove(edge3)
		if( edge4 in equacio.edgelistCamiFinal):equacio.edgelistCamiFinal.remove(edge4)
		if( edge3 in equacio.edgeListVariablesUnica):equacio.edgeListVariablesUnica.remove(edge3)
		if( edge4 in equacio.edgeListVariablesUnica):equacio.edgeListVariablesUnica.remove(edge4)
		if( edge3 in equacio.edgeListVariablesNoUnica):equacio.edgeListVariablesNoUnica.remove(edge3)
		if( edge4 in equacio.edgeListVariablesNoUnica):equacio.edgeListVariablesNoUnica.remove(edge4)


	equacio.G.add_node(varFinal)
	equacio.G.add_edge(valor1Ca,varFinal)
	equacio.G.add_edge(valor2Ca,varFinal)
	equacio.labels[varFinal]=varFinal

	if not( varFinal in equacio.llistat):equacio.llistat.append(varFinal)#Nomes esta enllaçat amb les equacions d'igualacio
	if not( varFinal in equacio.nodelistVariables):equacio.nodelistVariables.append(varFinal)
	if not( varFinal in equacio.listDesconegudes):equacio.listDesconegudes.append(varFinal)
	if not( var in equacio.nodelistDesconegudesUnica):equacio.nodelistDesconegudesUnica.append(varFinal)
	if not( edge1 in equacio.edgelist):equacio.edgelist.append((varFinal,valor1Ca))
	if not( edge2 in equacio.edgelist):equacio.edgelist.append((varFinal,valor2Ca))




#Mètode que crea variables segons les variables que desconeixem
def variablesIndividualsNoves(s):
	#variables individuals
	equacio.G.add_node(equacio.equacioCanonica)
	variables=[]
	var=""
	varAlter=""
	for x in equacio.equacioCanonica:
		if (x!='*') & (x!='/') & (x!='+') & (x!='-') & (x!='^') & (x!='=') & (x!='(') & (x!=')') & (not x.isdigit()):
			var=var+x
			varAlter=""
		else:
			varAlter=varAlter+x
			if(len(var)!=0):
				if not(var in equacio.nodelistVariables):#Si no existeix dins la llista
					equacio.nodelistVariables.append(var)
				equacio.G.add_node(var)
				equacio.GV.add_node(var)
				equacio.G.add_edge(equacio.equacioCanonica,var)
				equacio.labels[var]=var
				equacio.edgelist.append((var,equacio.equacioCanonica))
				variables.append(var)
				var=""
	if(len(var)!=0):
		variables.append(var)
		equacio.G.add_node(var)
		equacio.GV.add_node(var)
		equacio.G.add_edge(equacio.equacioCanonica,var)
		equacio.labels[var]=var
		if not(var in equacio.nodelistVariables):
			equacio.nodelistVariables.append(var)
		equacio.edgelist.append((var,equacio.equacioCanonica))
	else:
		if(len(variables)>0):
			var=variables.pop()
			variables.append(var[0:len(var)])
			equacio.G.add_node(var[0:len(var)])
			equacio.GV.add_node(var[0:len(var)])
			equacio.G.add_edge(equacio.equacioCanonica,var[0:len(var)])
			valor=var[0:len(var)]
			equacio.labels[valor]=valor
			if not(var in equacio.nodelistVariables):
				equacio.nodelistVariables.append(var[0:len(var)])
			equacio.edgelist.append((var[0:len(var)],equacio.equacioCanonica))
		else:
			variables.append(var)
			equacio.G.add_node(var)
			equacio.GV.add_node(var)
			equacio.G.add_edge(equacio.equacioCanonica,var)
			valor=var
			equacio.labels[valor]=valor
			if not(var in equacio.nodelistVariables):
				equacio.nodelistVariables.append(var)
			equacio.edgelist.append((var,equacio.equacioCanonica))

	#Afegim les variables i la fórmula
	if not(equacio.equacioCanonica in equacio.nodelistFormules):#si encara no hem afegit la formula
		equacio.nodelistFormules.append(equacio.equacioCanonica)
		equacio.num=str(len(equacio.nodelistFormules))#Donem el valor al num
		equacio.labels[equacio.equacioCanonica]=str(len(equacio.nodelistFormules))#+1 perque encara no he afegit la formula
		equacio.llistatEquacions.append(equacioCompleta(equacio.equacioInicial,equacio.equacioCanonica,equacio.num,"Igualació"))
	equacio.llistat.append(variables)#Afegim les variables
	return

#Mètode que controla que si l’usuari no posar el símbol *, 
#la fórmula sigui modificada amb el símbol * dins la fórmula. 
#Això es degut a que la llibreria Simpy no ho detecta com una multiplicació i així evitem errors.
def multiplicacions(equa):
	novaEquacio=""
	num=""
	numero=False#Indica si l'anterior valor es numero
	for x in equa:
		if(x.isdigit()):
			numero=True
			num=num+x
		else:
			if(numero):
				if(x!='*') & (x!='/') & (x!='+') & (x!='-') & (x!='^') & (x!='=') & (x!='(') & (x!=')'):
					novaEquacio=novaEquacio+num+"*"+x#part anterior + numero * variable
					numero=False
					num=""
				else:
					novaEquacio=novaEquacio+num+x
					numero=False
					num=""	
			else:
				novaEquacio=novaEquacio+x
	if(numero):#Si s'acaba amb numero l'afegim perque no s'afegeix al for fins que te una variable davant
		novaEquacio=novaEquacio+num
	return novaEquacio

#Té la mateixa funció que l’anterior però en aquest cas el número es troba després de la variable
def multiplicacionsInvertida(equa):
	novaEquacio=""
	var=""
	variable=False
	x=equa[0]
	if (x!='*') & (x!='/') & (x!='+') & (x!='-') & (x!='^') & (x!='=') & (x!='(') & (x!=')') & (not x.isdigit()):
		var=x
		variable=True
	else:
		novaEquacio=novaEquacio+x
	for x in equa[1:len(equa)]:
		if(x.isdigit()):
			if(variable):
				novaEquacio=novaEquacio+var+"*"+x
				var=""
				variable=False
			else:
				novaEquacio=novaEquacio+x
				variable=False
		else:
			if(x!='*') & (x!='/') & (x!='+') & (x!='-') & (x!='^') & (x!='=') & (x!='(') & (x!=')'):
				var=var+x
				variable=True
			else:
				variable=False
				novaEquacio=novaEquacio+var+x
				var=""
	if(len(var)!=0):#afegim la variable final
		novaEquacio=novaEquacio+var
	return novaEquacio



#Mètode que extreu les variables de les fórmules introduïdes per l’usuari
def variablesIndividuals():
	#variables individuals
	equacio.nodelistFormules.append(equacio.equacioCanonica)
	equacio.G.add_node(equacio.equacioCanonica)
	equacio.GI.add_node(equacio.equacioCanonica)
	equacio.labels[equacio.equacioCanonica]=str(len(equacio.nodelistFormules))
	equacio.num=str(len(equacio.nodelistFormules))#Donem el valor al num
	variables=[]
	var=""
	cont=0
	for x in equacio.equacioCanonica:
		if (x!='*') & (x!='/') & (x!='+') & (x!='-') & (x!='^') & (x!='=') & (x!='(') & (x!=')') & (not x.isdigit()):
			var=var+x
		else:
			if(len(var)!=0):
				if not(var in equacio.nodelistVariables):#Si no existeix dins la llista
					equacio.nodelistVariables.append(var)
				equacio.G.add_node(var)
				equacio.GI.add_node(var)
				equacio.GV.add_node(var)
				equacio.labels[var]=var
				equacio.edgelist.append((var,equacio.equacioCanonica))
				variables.append(var)
				var=""
	if(len(var)!=0):
		variables.append(var)
		equacio.G.add_node(var)
		equacio.GI.add_node(var)
		equacio.GV.add_node(var)
		equacio.labels[var]=var
		if not(var in equacio.nodelistVariables):
			equacio.nodelistVariables.append(var)
		equacio.edgelist.append((var,equacio.equacioCanonica))
	else:
		if(len(variables)>0):
			var=variables.pop()
			variables.append(var[0:len(var)])
			equacio.G.add_node(var[0:len(var)])
			equacio.GI.add_node(var[0:len(var)])
			equacio.GV.add_node(var[0:len(var)])
			valor=var[0:len(var)]
			equacio.labels[valor]=valor
			if not(var in equacio.nodelistVariables):
				equacio.nodelistVariables.append(var[0:len(var)])
			equacio.edgelist.append((var[0:len(var)],equacio.equacioCanonica))
	#Afegim les variables
	equacio.llistatEquacions.append(equacioCompleta(equacio.equacioInicial,equacio.equacioCanonica,equacio.num,"Equació inicial"))
	equacio.llistat.append(variables)#Afegim les variables
	return

def variablesDobles():
	#Variables dobles
	variablesDobles=[]
	var=""
	doble=False
	for x in s:
		if((x=='(')):
			doble=True
		elif((x==')')):
			doble=False
			var=var+x
			variablesDobles.append(var)
			equacio.G.add_node(var)
			equacio.GI.add_node(var)
			var=""
		if(doble):
			var=var+x
	equacio.llistat.append(variablesDobles)
	return

class equacio:
	import networkx as nx
	import matplotlib.pyplot as plt
	#Variables necessaries pel tractament de les dades
	equacioCanonica = ""#equacio canònica
	equacioInicial=""#Equacio inicial
	partEsq = ""#part del canto esquerre de l'equacio
	partDre = ""#part del canto dret de l'equacio
	num=""#Número que identificarà l'equació al graf
	pathFoto = None #Path foto graf complert
	pathFotoFinal = None #Path foto graf resolt
	pathFotoInicial = None
	pathFotoValors = None
	pathFotoInicialIgualacio = None
	pathFotoInicialIgualacioValors = None
	nodeInicialDibuixat=False
	nodeInicialIgualacioDibuixat=False

	#Llistats per els templates
	llistat=[]#Llistat on guardem totes les variables
	llistatEquacions=[]#Llista amb totes les equacions vistes, amb el número de label i la seva canònica#ARRAY

	#Grafs
	GI = nx.Graph()#Graf inicial que contindrà les equacions introduides per l'usuari
	G = nx.Graph()#Graf complert
	GV = nx.Graph()#Graf unicament amb variables per a tractarles
	GF = nx.Graph()#Graf pas a pas

	#GIGUAL=nx.Graph()#Graf amb les funcions d'igualacio

	#Graf unic
	edgeListVariablesUnica=[]
	edgeListVariablesNoUnica=[]

	#Llistes i diccionaris per crear el Graf complert (G) i graf inicial (GI)
	nodelistVariables=[]#Aqui guardarem tots els nodes variable
	nodelistFormules=[]#Aquí guardarem tots els nodes formula en format canònica

	nodelistVariablesInicial=[]
	nodelistFormulesInicial=[]

	edgelist=[]#Aquí guardarem tots els enllaços dels nodes variables als nodes formules
	labels={}

	#Llistes i diccionaris per crear el Graf final GF
	nodelistVarConFinal=[]#Aqui guardarem tots els nodes inputs utilitzats
	nodelistVarDesFinal=[]#Aqui guardarem tots els nodes que hem trobat solució que eren desconeguts
	nodelistVarOutputsFinal=[]#Aqui guardarem tots els nodes outputs trobats
	nodelistFormulesFinal=[]#Aquí guardarem tots els nodes formula utilitzats
	edgelistFinal=[]#Aquí guardarem tots els enllaços dels nodes variables als nodes formules
	edgelistCamiFinal=[]#Aquí guardarem els enllaços per seguir el camí
	labelsFinal={}#Valor que posarem als nodes

	listPath=[]#llista on guardarem els path de les imatges a mostrar. llista fixa
	listPath2=[]#Llista no fixa on guardarem els path
	#listPath.extend([image("0","0","Graf inicial"), image("1","1","Graf 1"),image("2","2","Graf 2"),image("3","3","Graf 3")])

	#LListes per anar creant el graf de la imatge única
	nodelistConegudesUnica=[]
	nodelistCheckOutUnica=[]
	nodelistDesconegudesUnica=[]
	#nodelistFormulesUnica=[]

	#Llistes per el graf quan fem igualacio
	listRelacioEdgesNovesFormules=[]
	listNovesFormules=[]#Per comprovar
	listNovesVariablesFuncions=[]


	#Llistes per mostrar el graf pas a pas
	nodelistVarDesOutPutPas=[]
	nodelistVarDesNoOutPutPas=[]
	nodelistVarConPas=[]
	nodelistVarConPasOut=[]
	nodelistFormulesPas=[]
	edgelistPas=[]
	labelsPas={}



	#LListes per resoldre els problemes
	listCheckInValor=[]#Llista on guardarem les variables INPUTS amb els seus valors
	listCheckOut=[]#Llista on guardarem quines variables son OUTPUTS no fixa
	listCheckOutFixa=[]
	listCheckOutValor=[]#Llista on guardarem les variables OUTPUTS amb els seus valors#ARRAY
	listDesconegudes=[]#LLista on guardarem les variables que desconeixem
	listConegudes=[]#Llista de conegudes
	listConegudesOutput=[]#Llista de conegudes
	listConegudesTotalsValor=[]#Llista on guardarem totes les variables que en sabem els valors
	listFormulesGrau=[]#Llista on guardarem el grau de les formules, el terme grau es les variables que desconeixem el valor
	grau=0#Grau en que ens trobarem per resoldre les equacions
	llargadaCheckOut=0#Variable per finalitzar la recursivitat
	calcularMesFormules = False#Booleano que ens permetrà calcular més fòrmules o no