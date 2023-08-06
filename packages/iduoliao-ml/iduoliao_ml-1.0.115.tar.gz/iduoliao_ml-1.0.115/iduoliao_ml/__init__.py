#! /usr/bin/env python
# -*- coding: utf-8 -*-

import hot, es, dataDispose, itemCF, test, db

def startUpdateHot(isTest):
	es.setEnv(isTest)
	hot.startUpdate(isTest, 'config.ini')

def disposeData(isTest):
	es.setEnv(isTest)
	dataDispose.cycleDisposePersonas()

def cfItem(isTest):
	es.setEnv(isTest)
	itemCF.cf()

def updateHistoryActions(isTest):
	es.setEnv(isTest)
	dataDispose.updateHistoryActions()

def testFunc():
	es.setEnv(True)
	es.updateRedisWorksHots({})
	#print(es.searchDbConfig())
