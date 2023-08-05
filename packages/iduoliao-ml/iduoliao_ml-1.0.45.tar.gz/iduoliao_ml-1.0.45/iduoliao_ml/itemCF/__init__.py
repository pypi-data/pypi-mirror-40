#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .. import es

def cf():
	worksInfos = {}

	uidWorks = {}
	hits = es.searchStatisticsDataByBody('works_actions', {"query": {"match": {"action": 2}},"size": 10000})
	for hit in hits:
		source = hit['_source']
		uid = source['uid']
		vid = source['vid']
		if uidWorks.has_key(uid):
			vids = uidWorks[uid]
			if vids.count(vid) != 0:
				continue
		else:
			vids = uidWorks[uid] = []

		if worksInfos.has_key(vid):
			worksInfo = worksInfos[vid]
		else:
			worksInfo = worksInfos[vid] = {'count': 0, 'similars': {}}
		worksInfo['count'] += 1
		for bVid in vids:
			similars = worksInfo['similars']
			if similars.has_key(bVid):
				similars[bVid] += 1
			else:
				similars[bVid] = 1

		vids.append(vid)

	for vid, info in worksInfos.items():
		pass


	print(worksInfos)




