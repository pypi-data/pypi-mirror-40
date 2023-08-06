#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time, random
from .. import es
from bftWorks import BftWorks

PoolCountKey = {1: 'flowFirstCount', 2: 'flowSecondCount', 3: 'flowThirdCount', 4: 'successCount', 5: 'failCount'}

def updateWorks():
	#endTime = int(time.time())
	endTime = 1547568000
	vids = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29']
	worksDict = getWorksDict(vids, endTime)

	while True:
		if random.randint(1, 2) == 1:
			vids.append(str(time.time()))
		worksDict = updateWorksDict(worksDict, vids, endTime)
		endTime = update(worksDict, endTime)
		saveWorksToEs(worksDict)

		Pools = BftWorks.Pools
		record = {'time': es.timeToEsLocalTime(endTime), 'flowFirstCount': 0, 'flowSecondCount': 0, 'flowThirdCount': 0, 'successCount': 0, 'failCount': 0}
		show = {Pools['FlowFirst']: 0, Pools['FlowSecond']: 0, Pools['FlowThird']: 0}
		for works in worksDict.values():
			record[PoolCountKey[works.pool]] += 1
			if works.pool in [Pools['FlowFirst'], Pools['FlowSecond'], Pools['FlowThird']]:
				show[works.pool] += works.getCount('show')
		record['flowFirstShowAvg'] = 0 if record['flowFirstCount'] == 0 else show[Pools['FlowFirst']] / record['flowFirstCount']
		record['flowSecondShowAvg'] = 0 if record['flowSecondCount'] == 0 else show[Pools['FlowSecond']] / record['flowSecondCount']
		record['flowThirdShowAvg'] = 0 if record['flowThirdCount'] == 0 else show[Pools['FlowThird']] / record['flowThirdCount']
		es.updateStatisticsData('works_filter_pool_record', {int(endTime): record})
		time.sleep(2)

def update(worksDict, startTime):
	#endTime = int(time.time() - 90)
	endTime = startTime + 10 * 60
	for hit in es.searchStatisticsDataByBody("works_actions", {"query": {"bool": {"must": [{"range": {"time": {"gte": startTime * 1000, "lt": endTime * 1000}}}, {"terms": {"action": [2, 3, 5, 12, 13, 16]}}]}}, "size": 10000}):
		action = hit['_source']
		vid = action['vid']
		if random.randint(1, 5) == 1:
			vid = random.sample(worksDict.keys(), 1)[0]
		if worksDict.has_key(vid):
			worksDict[vid].updateAction(action)

	for works in worksDict.values():
		works.updateStatus()

	return endTime

def updateWorksDict(worksDict, vids, endTime):
	newWorksDict = {}
	for vid in vids:
		if worksDict.has_key(vid):
			newWorksDict[vid] = worksDict[vid]
		else:
			works = BftWorks(vid)
			works.init(es.timeToEsLocalTime(endTime))
			newWorksDict[vid] = works
	return newWorksDict

def getWorksDict(vids, endTime):
	worksDict = {}
	for vid in vids:
		worksDict[vid] = BftWorks(vid)
	syncEsWorks(worksDict)
	for works in worksDict.values():
		works.init(es.timeToEsLocalTime(endTime))
	return worksDict

def syncEsWorks(worksDict):
	for hit in es.searchStatisticsData('works_filter_pool'):
		vid = hit['_id']
		if worksDict.has_key(vid):
			worksDict[vid].syncEsData(hit['_source'])

def saveWorksToEs(worksDict):
	worksData = {}
	for vid, works in worksDict.items():
		worksData[vid] = works.toSaveEsData()
	es.updateStatisticsData('works_filter_pool', worksData)

	