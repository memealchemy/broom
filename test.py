import json
from pytrends.request import TrendReq
from pandas import DataFrame


def chunkify(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


trend = TrendReq()
data = list(chunkify(json.load(open("output.json")), 5))[:5]
e = []

for d in data:
    trend.build_payload(
        [l["title"].lower() for l in d], timeframe="today 1-m", cat=0, geo="US"
    )
    search = trend.interest_over_time()

    df = DataFrame(search)
    df.reset_index(inplace=True, drop=True)
    res = df.to_dict()

    e.append(res)

print(e)
