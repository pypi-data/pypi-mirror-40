#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
from .. import es

class BftWorks(object):

	RiseThreshold = 0.3

	ShowMax = {1: 50, 2: 100, 3: 500}

	Weights = {1: {"like": 1.5, "share": 1.5, "longPlay": 1, "play": 1}
	, 2: {"like": 2, "share": 2, "longPlay": 1, "play": 1}
	, 3: {"like": 2, "share": 3, "longPlay": 1, "play": 1}
	, 4: {"like": 2, "share": 3, "longPlay": 1, "play": 1}
	, 5: {"like": 2, "share": 3, "longPlay": 1, "play": 1}}

	#1 一层流量池 2 二层流量池 3 三层流量池 4 晋级池 5 淘汰池
	Pools = {'FlowFirst': 1, 'FlowSecond': 2, 'FlowThird': 3, 'Success': 4, 'Fail': 5}

	def __init__(self, vid):
		self.vid = vid
		self.score = 0
		self.enterPool(BftWorks.Pools['FlowFirst'])

	def updateAction(self, action):
		if self.pool not in [BftWorks.Pools['FlowFirst'], BftWorks.Pools['FlowSecond'], BftWorks.Pools['FlowThird']]:
			return
		actionId = action['action']
		uid = action['uid']
		if actionId == 3:
			self.uidSetDict['show'].add(uid)
		elif actionId == 16:
			self.uidSetDict['like'].add(uid)
		elif actionId == 12 or actionId == 13:
			self.uidSetDict['share'].add(uid)
		elif actionId == 2:
			self.uidSetDict['longPlay'].add(uid)
		elif actionId == 5:
			self.uidSetDict['play'].add(uid)

	def updateStatus(self):
		if self.pool not in [BftWorks.Pools['FlowFirst'], BftWorks.Pools['FlowSecond'], BftWorks.Pools['FlowThird']]:
			return
		showMax = BftWorks.ShowMax[self.pool]
		weight = BftWorks.Weights[self.pool]

		show = self.getCount('show')
		score = 0
		totalOne = 0
		for key in weight.keys():
			score += weight[key] * self.getCount(key)
			totalOne += weight[key]
		
		if score >= max(showMax, show) * totalOne * BftWorks.RiseThreshold:
			self.enterPool(self.pool + 1)
		elif show >= showMax:
			self.enterPool(BftWorks.Pools['Fail'])
		self.score = score

	def init(self, endTime):
		body = {"query": {"bool": {"must": [{"range": {"time": {"gte": self.timeEnter, "lt": endTime}}}, {"term": {"vid": self.vid}}, {"terms": {"action": [2, 3, 5, 12, 13, 16]}}]}}, "size": 0, "aggs": {}}
		body['aggs']['uid_diff'] = {"terms": {"field": "action", "size": 6}, "aggs": {"count": {"cardinality": {"field": "uid"}}}}
		aggs = es.searchStatisticsAggs('works_actions', body)
		
		counts = {2: 0, 3: 0, 5: 0, 12: 0, 13: 0, 16: 0}
		for bucket in aggs['uid_diff']['buckets']:
			counts[bucket['key']] = bucket['count']['value']

		self.initData['show'] = counts[3]
		self.initData['like'] = counts[16]
		self.initData['share'] = counts[12] + counts[13]
		self.initData['longPlay'] = counts[2]
		self.initData['play'] = counts[5]

		self.updateStatus()

	def enterPool(self, newPool):
		self.pool = newPool
		self.timeEnter = es.timeToEsLocalTime(time.time())
		self.initData = {'show': 0, 'like': 0, 'share': 0, 'longPlay': 0, 'play': 0}
		self.uidSetDict = {'show': set(), 'like': set(), 'share': set(), 'longPlay': set(), 'play': set()}

	def getCount(self, key):
		return self.initData[key] + len(self.uidSetDict[key])

	def toSaveEsData(self):
		data = {"vid": self.vid, "pool": self.pool, "timeEnter": self.timeEnter, 'score': self.score, 'show': self.getCount('show')}
		for key in BftWorks.Weights[self.pool].keys():
			data[key] = self.getCount(key)
		return data

	def syncEsData(self, source):
		self.pool = source["pool"]
		self.timeEnter = source["timeEnter"]
	


	