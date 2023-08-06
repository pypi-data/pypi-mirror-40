#! /usr/bin/env python
# -*- coding: utf-8 -*-

from btfWorks import BtfWorks

def updateWorks(vids):
	pass

def syncEsWorks(worksList):
	for hit in es.searchStatisticsData('works_filter_pool'):
		#worksList[hit['_id']] = BtfWorks.createByEs(hit['_source'])
	#return worksList

def saveWorksToEs(worksList):
	saveData = {}
	for vid, works in worksList.items():
		saveData[vid] = works.toSaveEsData()
	es.coverStatisticsDataReal('works_filter_pool', saveData)