# waybackeasy - v01

import requests, json, random

def get_wayback(target_site, target_date):
	""" simple function to get Waybackmachine snapshot of target site on particular target day """
	data_point = "timestamp"
	wbm_api = "http://web.archive.org/cdx/search/cdx?url={}&fl={}&output=json".format(target_site, data_point)
	resp = requests.get(wbm_api)
	timestamps = json.loads(resp.text)
	# print(timestamps)

	date = target_date.split("-")
	day, month, year = date[0], date[1], date[2]
	wbm_date = year + month + day
	# print(wbm_date)

	relevant_timestamps = []
	for each in timestamps:
		if each[0].startswith(wbm_date):
			relevant_timestamps.append(each[0])
	# print(relevant_timestamps)

	chosen_timestamp = random.choice(relevant_timestamps)

	res = requests.get("http://web.archive.org/web/{}/{}".format(chosen_timestamp, target_site))
	return res.text.encode('utf-8')
	# print(chosen_timestamp)

# get_wayback('http://www.spiegel.de/', '05-10-2017')



"""
follow tutorial on pypi page itself ...
stp by stp, then see ...
"""
