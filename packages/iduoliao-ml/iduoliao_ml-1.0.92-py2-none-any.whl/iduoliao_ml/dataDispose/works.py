#! /usr/bin/env python
# -*- coding: utf-8 -*-

import gc, time
from .. import es

class Works(object):

	DurationSections = [0, 30, 60, 180, 300, 600, 900, 1200, 1800, 2400, 3600, 7200]

	def __init__(self, vid, aid, title, publishTime, duration):
		self.vid = vid
		self.aid = aid
		self.title = title
		self.publishTime = int(time.time() - es.esTimeToTime(publishTime, True)) / 3600
		durationIndex = 7200
		for value in Works.DurationSections:
			if duration < value:
				durationIndex = value
				break
		self.durationIndex = durationIndex
		self.startTime = 0
		self.endTime = 0
		self.play = 0
		self.shareF = 0
		self.shareI = 0
		self.replay = 0
		self.like = 0
		self.sub = 0
		self.longPlay = 0
		self.timeAvg = 0
		self.score = 0
		self.ratio = 0

		self.playUids = []
		self.shareFUids = set()
		self.shareIUids = set()
		self.replayUids = set()
		self.timeTotal = 0
		self.timeCount = 0

	def updateAction(self, action):
		actionId = action['action']
		uid = action['uid']
		if actionId == 1:
			self.timeTotal += action['value']
			self.timeCount += 1
			self.timeAvg = self.timeTotal * 1.0 / self.timeCount
			if uid in self.playUids:
				self.replayUids.add(uid)
				self.replay = len(self.replayUids)
			else:
				self.playUids.append(uid)
				self.play = len(self.playUids)
		elif actionId == 12:
			self.shareFUids.add(uid)
			self.shareF = len(self.shareFUids)
		elif actionId == 13:
			self.shareIUids.add(uid)
			self.shareI = len(self.shareIUids)
		elif actionId == 14:
			self.like += 1
		elif actionId == 15:
			self.like -= 1
		elif actionId == 16:
			self.sub += 1
		elif actionId == 17:
			self.sub -= 1
		elif actionId == 2:
			self.longPlay += 1

	def toSaveEsData(self):
		return {"vid": self.vid, "score": self.score, "time": self.endTime, "ratio": self.ratio}

	def updateActions(self, endTime, startTime=1546099200):
		self.startTime = min(self.startTime, startTime)
		self.endTime = max(self.endTime, endTime)
		play, shareF, shareI, replay, like, sub, longPlay, timeAvg = self.getDataByVid(self.vid, startTime, endTime)
		self.play += play
		self.shareF += shareF
		self.shareI += shareI
		self.replay += replay
		self.like += like
		self.sub += sub
		self.longPlay += longPlay
		self.timeAvg = (self.timeAvg + timeAvg) / 2.0 if self.timeAvg != 0 else timeAvg
		gc.collect()

	def getDataByVid(self, vid, startTime, endTime):
		hits = es.searchStatisticsDataByBody("works_actions", {"query": {"bool": {"must": [{"range": {"createTime": {"gte": startTime, "lt": endTime}}}, {"term": {"vid": vid}}, {"terms": {"action": [1, 2, 12, 13, 14, 15, 16, 17]}}]}}}, True, True)
		playUids = []
		shareFUids = set()
		shareIUids = set()
		replayUids = set()
		like = 0
		sub = 0
		longPlay = 0
		timeTotal = 0
		timeCount = 0
		for hit in hits:
			action = hit['_source']
			actionId = action['action']
			uid = action['uid']
			if actionId == 1:
				timeTotal += action['value']
				timeCount += 1
				if uid in playUids:
					replayUids.add(uid)
				else:
					playUids.append(uid)
			elif actionId == 12:
				shareFUids.add(uid)
			elif actionId == 13:
				shareIUids.add(uid)
			elif actionId == 14:
				like += 1
			elif actionId == 15:
				like -= 1
			elif actionId == 16:
				sub += 1
			elif actionId == 17:
				sub -= 1
			elif actionId == 2:
				longPlay += 1
		return len(playUids), len(shareFUids), len(shareIUids), len(replayUids), like, sub, longPlay, timeTotal * 1.0 / timeCount if timeCount != 0 else 0


