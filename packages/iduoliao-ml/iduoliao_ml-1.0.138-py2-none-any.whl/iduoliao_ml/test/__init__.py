#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .. import es

def test():
	values = []
	for key, value in {'a': 1, 'b': 2}.items():
		values += [key, value]
	testArgs(**{'a': 1, 'b': 2})
	'''
	es.setEnv(False)
	hits = es.searchStatisticsDataByBody('works_actions', {"query": {"term": {"vid": "ecbf3aa1599e140896e0f6c241d93681"}}, "size": 10000})
	
	dataDict = {}
	for hit in hits:
		dataDict[hit['_id']] = hit['_source']

	es.setEnv(True)
	es.updateStatisticsData('works_actions', dataDict)
	'''

def testArgs(*args, **kwargs):
	print(args)
	print(kwargs)