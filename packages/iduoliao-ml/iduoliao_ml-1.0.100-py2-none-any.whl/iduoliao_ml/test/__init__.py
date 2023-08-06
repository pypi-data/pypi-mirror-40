#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .. import es

def test():
	es.setEnv(True)
	hits = es.searchStatisticsDataByBody('works_actions', {"query": {"term": {"vid": "9c0754f99506b42fdff83ac54d32508e"}, "size": 10000}
	
	dataDict = {}
	for hit in hits:
		dataDict[hit['_id']] = hit['_source']

	es.setEnv(False)
	es.updateStatisticsData('works_actions', dataDict)
})