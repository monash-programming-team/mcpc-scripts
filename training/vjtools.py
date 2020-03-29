#!/usr/bin/env python
import requests as r
import pandas as pd
import time
from pyquery.pyquery import PyQuery as pq


def probsOverview(cid):
	url = "https://vjudge.net/contest/" + cid
	resp = r.get(url)
	page = pq(resp.content)
	res = {}
	idx = 0
	for tr in page("table#contest-problems tbody tr"):
		weight = int(pq(tr)("td.weight").text().strip(" pts"))
		pnum = pq(tr)("td.prob-num").text().strip()
		ptitle = pq(tr)("td.prob-title").text().strip()
		res[idx] = {'weight': weight, 'pnum': pnum, 'ptitle': ptitle}
		idx += 1
	return res

def get_score(cid):
	overview = probsOverview(cid)
	time.sleep(0.1)
	url = "https://vjudge.net/contest/rank/single/" + cid
	resp = r.get(url)
	data = resp.json()	
	res = {'score': {}}
	for sub in data['submissions']:
		user_id, pidx, ac = sub[:3]
		user_id = str(user_id)
		if res['score'].get(user_id, None) is None:
			res['score'][user_id] = 0
		if ac:
			res['score'][user_id] += overview[pidx]['weight']
	res['participants'] = { k: 
			{
				'nickname': v[1], 
				'username': v[0]
			} for k, v in data['participants'].items() }

	res['contest_id'] = cid
	return res

def get_all_score(cids):
	users = {}
	rows = []
	for cid in cids:
		print("get score contest#%s" % cid)
		single_round = get_score(cid)
		users.update(single_round['participants'])
		for k, v in single_round['score'].items():
			rows.append(
				dict(
					id=k, 
					username=users[k]['username'],
					nickname=users[k]['nickname'],
					contest_id=cid,
					score=v
				)
			)
		time.sleep(0.5)
	return rows


def main():
	cids = input().split()
	raw_rows = get_all_score(cids)

	exclude = ['GivAchanceee']
	rows = [i for i in raw_rows if i['username'] not in exclude]
	df = pd.DataFrame(rows)
	t = pd.pivot_table(
    df, 
    values='score', 
    index=['id', 'username', 'nickname'], 
    columns=['contest_id'], 
    fill_value=0,
    aggfunc='sum',
    margins=True,
    margins_name="total"
  )
	t = t.iloc[:-1]
	x = t.sort_values('total', ascending=False)
	with open("rank.html", "w") as f:
		f.write(x.to_html())
	with open("rank.csv", "w") as f:
		f.write(x.to_csv())
	with open("rank.json", "w") as f:
		f.write(x.to_json())
	print (x)

if __name__ == "__main__":
	main()
