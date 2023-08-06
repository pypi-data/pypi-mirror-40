#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json, time, urllib2
from .. import ilog, es, dataDispose
from hot import *

def startUpdate(isTest, configFileName):
	cycleUpdateHotList(configFileName, isTest)

def cycleUpdateHotList(configFileName, isTest):
	subjectHistory = dataDispose.getSubjectHistory()
	worksHistory = dataDispose.getWorksHistory()
	endTime = worksHistory.values()[0]['time']
	while True:
		try:
			start = time.time()
			ilog.info('start:' + str(start) + '(' + time.strftime(es.esTimeFormatNoMs, time.localtime(start)) + ')')
			
			endTime = onceUpdateHotList(subjectHistory, worksHistory, dataDispose.getWorksList(), endTime, configFileName, isTest)

			cost = time.time() - start
			ilog.info('-------------------------cost: ' + str(cost) + '---------------------------------')

			maxInterval = 60 if isTest else 600
			if cost < maxInterval:
				time.sleep(maxInterval - cost)
		except Exception as error:
			ilog.info('Error: ' + str(error))
			time.sleep(60)

def onceUpdateHotList(subjectHistory, worksHistory, worksList, startTime, configFileName, isTest):
	endTime = updateHotList(subjectHistory, worksHistory, worksList, startTime, readConfig(configFileName))
	#10秒后通知后台更新
	time.sleep(10)
	noticeServer(isTest)
	saveHotTopList()
	return endTime

def updateHotList(subjectHistory, worksHistory, worksList, startTime, config):
	start = time.time()
	#data.update()
	#subjectDict, worksDict = data.getSubWorksList(config['aid']['white'], config['vid']['black'])
	endTime = int(time.time())

	worksDict = {}
	for works in worksList:
		worksDict[works.vid] = works

	newHits = es.searchStatisticsDataByBody("works_actions", {"query": {"bool": {"must": [{"range": {"createTime": {"gte": startTime, "lt": endTime}}}, {"terms": {"action": [1, 2, 12, 13, 14, 15, 16, 17]}}]}}})
	for hit in newHits:
		action = hit['_source']
		vid = action['vid']
		if worksDict.has_key(vid):
			worksDict[vid].updateAction(action)

	ilog.info('add new actions finished:' + str(time.time() - start))

	updateWeight(config['weight'])
	
	#dauFactor = data.getDauFactor()
	#newShowMax = data.getNewShowMax()
	#ilog.info('dauFactor:' + str(dauFactor) + ' newShowMax:' + str(newShowMax))
	#worksHots = calHot(dauFactor, newShowMax, subjectDict, worksDict)

	worksHots = calHotV2(subjectHistory, worksHistory, worksList, dataDispose.getDauFactor(), es.searchDbConfig(), config['aid']['half'])

	ilog.info('got hot list:' + str(time.time() - start))

	ilog.info('update works hot: ' + ('success ' if es.coverStatisticsData('works_hot', worksHots) else 'fail ') + str(time.time() - start))
	#ilog.info('update redis works hot: ' + ('success ' if es.updateRedisWorksHots(getRedisWorksHots(worksHots)) else 'fail ') + str(time.time() - start))

	return endTime

def getRedisWorksHots(worksHots):
	redisWorksHots = {}
	aids = []
	for vid, works in worksHots.items():
		aid = works['aid']
		if aid not in aids:
			aids.append(aid)
			redisWorksHots[vid] = works['hot']
	return redisWorksHots

def readConfig(configFileName):
	with open(configFileName, 'r') as f:
		config = json.loads(f.read())
	ilog.info('config: ' + str(config))
	return config

def noticeServer(isTest):
	try:
		noticeUpdate(1, isTest)
		noticeUpdate(2, isTest)
	except urllib2.HTTPError as error:
		ilog.info('urllib2.HTTPError: ' + str(error))

def noticeUpdate(listType, isTest):
	url = 'http://nttest.iduoliao.cn:8080' if isTest else 'https://micro.mitao.iduoliao.cn'
	data = {
		"head":{
     		"@type":"type.googleapis.com/ja.common.proto.AutReqHead",
  			"ver": 1,
  			"platform": 999,
  			"seqid": long(time.time() * 1000)
    	},
    	"type": listType
	}
	headers = {'Content-Type': 'application/json'}
	request = urllib2.Request(url=url+'/recommend/IRecommend/UpdateDataNotice', headers=headers, data=json.dumps(data))
	infoInfo = urllib2.urlopen(request).read()
	ilog.info('notice ' + ('hot' if listType == 1 else 'new') + ' list update resp: ' + str(infoInfo))
	return json.loads(infoInfo)['head']['status'] == 1

def saveHotTopList():
	body = {"sort": [{"ranking": {"order": "asc"}}],"size": 50}
	now = time.strftime('%Y-%m-%dT%H:%M:%S+0800', time.localtime(time.time()))
	print(now)
	topList = {}
	for index, hit in enumerate(es.searchStatisticsDataByBody('works_hot', body, False)):
		info = hit['_source']
		info['time'] = now
		topList[hit['_id'] + '$' + str(now)] = info
	es.updateStatisticsData('works_hot_tops', topList)








