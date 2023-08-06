#! /usr/bin/env python
# -*- coding: utf-8 -*-

#pool: 1 一层流量池 2 二层流量池 3 三层流量池 4 晋级池 5 淘汰池
class BftWorks(object):

	def __init__(self, vid, pool, timeEnter):
		self.vid = vid
		self.pool = pool
		self.timeEnter = timeEnter

	