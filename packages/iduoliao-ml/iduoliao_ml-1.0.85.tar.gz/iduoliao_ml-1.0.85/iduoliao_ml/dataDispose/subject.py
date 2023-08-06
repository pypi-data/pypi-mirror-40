#! /usr/bin/env python
# -*- coding: utf-8 -*-

import gc, time
from .. import es

class Subject(object):

	def __init__(self, aid):
		self.aid = aid
		self.startTime = 0
		self.endTime = 0
		self.count = 0
		self.play = 0
		self.replay = 0
		self.conv = 1

	def toSaveEsData(self):
		return {"aid": self.aid, "score": self.score, "time": self.endTime}

	def updateActions(self, endTime, startTime=1546099200):
		self.startTime = min(self.startTime, startTime)
		self.endTime = max(self.endTime, endTime)
		count, play, replay, conv = self.getDataByAid(self.aid, startTime, endTime)
		self.count += count
		self.play += play
		self.replay += replay
		self.conv = (self.conv + conv) / 2.0 if self.conv != 0 else conv
		gc.collect()

	def getDataByAid(self, aid, startTime, endTime):
		hits = es.searchStatisticsDataByBody("works_actions", {"query": {"bool": {"must": [{"range": {"createTime": {"gte": startTime, "lt": endTime}}}, {"term": {"aid": aid}}, {"terms": {"action": [3, 5]}}]}}}, True, True)
		count = 0
		playUids = []
		replayUids = set()
		recShow = 0
		recShowPlay = 0
		for hit in hits:
			action = hit['_source']
			actionId = action['action']
			uid = action['uid']
			if actionId == 1:
				if uid in playUids:
					replayUids.add(uid)
				else:
					playUids.append(uid)
			elif actionId == 3:
				recShow += 1
			elif actionId == 4:
				count += 1
			elif actionId == 5:
				recShowPlay += 5
		return count, len(playUids), len(replayUids), recShowPlay * 1.0 / recShow if recShow != 0 else 0


