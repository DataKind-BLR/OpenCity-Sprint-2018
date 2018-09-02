import json


def aggregate_ps_count():
    with open("Rural.json", encoding='utf-8') as data_file:
        rural_data = json.loads(data_file.read())
    with open("Urban.json", encoding='utf-8') as data_file:
        urban_data = json.loads(data_file.read())
    ps_split = {}
    aggfregate_split(ps_split, rural_data)
    aggfregate_split(ps_split, urban_data)

    return ps_split


def aggfregate_split(ps_split, rural_data):
    for constituency in rural_data["constituencies"]:
        for candidate in constituency["candidates"]:
            for ps in candidate["vote_split"]:
                code = ps["PSCode"]
                if code not in ps_split.keys():
                    ps_split[code] = 0
                total = ps.get("Total", 0)
                total = 0 if total is None else total
                ps_split[code] = ps_split.get(code) + int(total)


json.dump(aggregate_ps_count(), open("ps_vote_split.json", 'w'))
