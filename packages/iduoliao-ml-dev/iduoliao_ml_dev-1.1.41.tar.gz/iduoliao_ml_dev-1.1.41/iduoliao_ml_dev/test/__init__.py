#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time, json
from .. import es, dataDispose

class T(object):

	A = 1

	def __init__(self):
		print(T.A)

def test():
	saveFile()
	#a = T()
	#statisticsRecConv()

def saveFile():
	lines = []
	count = 0
	for hit in es.scrollSearch('clientlog_read', 'watch', {"size": 10000, "query": {"bool": {"must": [{"range": {"endtime": {"lt": 1547827200000}}}, {"term": {"type": {"value": "avplay"}}}]}}}):
		body = hit['_source']['body'].encode('utf-8').replace('\t', ' ')
		for item in body.split('\n'):
			start = item.find('{')
			if start == -1:
				continue
			try:
				data = json.loads(item[start:])
			except Exception as error:
				print(item[start:], error)
				count += 1
			lines.append('\t'.join([data['uid'], data['vid'], data['ym_version'], data['wx_version'], data['model'], data['networktype'], data['platform'], data['sdkversion'], str(data['width'] if data.has_key('width') else -1), str(data['height'] if data.has_key('height') else -1), data['errmsg']]))
	print(len(lines), count)
	with open('avplay', 'a') as f:
		f.write('\n'.join(lines))

def statisticsRecConv():
	convTotal = 0
	uids = []
	for hit in es.searchStatisticsDataByBody('works_actions', {"query": {"bool": {"must": [{"range": {"time": {"gte": 1547049600000, "lt": 1547136000000}}}, {"term": {"action": {"value": 3}}}]}}, "size":10000}):
		uid = hit["_source"]["uid"]
		if uid in uids:
			continue
		uids.append(uid)
		body = {"query": {"bool": {"must": [{"term": {"uid": uid}}, {"terms": {"action": [3, 5]}}, {"range": {"time": {"gte": 1547049600000, "lt": 1547136000000}}}]}}, "size": 0, "aggs": {}}
		body['aggs']['vid_diff'] = {"terms": {"field": "action", "size": 2}, "aggs": {"count": {"cardinality": {"field": "vid"}}}}
		aggs = es.searchStatisticsAggs('works_actions', body)
		recShow = 0
		recShowPlay = 0
		for bucket in aggs['vid_diff']['buckets']:
			if bucket['key'] == 3:
				recShow = bucket['count']['value']
			elif bucket['key'] == 5:
				recShowPlay = bucket['count']['value']
		convTotal += (0 if recShow == 0 else recShowPlay * 1.0 / recShow)
		count = len(uids)
		print(count, uid, recShow, recShowPlay, convTotal, convTotal * 1.0 / count)
		time.sleep(1)



def testA():
	worksList = dataDispose.getWorksList()
	data = {}
	for index, works in enumerate(worksList):
		print(index, works.vid)
		body = {"query": {"bool": {"must": [{"term": {"vid": works.vid}}, {"terms": {"action": [3, 5]}}]}}, "size": 0, "aggs": {}}
		body['aggs']['uid_diff'] = {"terms": {"field": "action", "size": 2}, "aggs": {"count": {"cardinality": {"field": "uid"}}}}
		aggs = es.searchStatisticsAggs('works_actions', body)
		data[works.vid] = {'vid': works.vid, 'aid': works.aid, 'title': works.title, 'resShow': 0, 'resShowPlay': 0}
		for bucket in aggs['uid_diff']['buckets']:
			if bucket['key'] == 3:
				data[works.vid]['resShow'] = bucket['count']['value']
			elif bucket['key'] == 5:
				data[works.vid]['resShowPlay'] = bucket['count']['value']

	#print(data)
	es.updateStatisticsData('works_info', data)


	'''
	values = []
	for key, value in {'a': 1, 'b': 2}.items():
		values += [key, value]
	testArgs(**{'a': 1, 'b': 2})
	'''
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