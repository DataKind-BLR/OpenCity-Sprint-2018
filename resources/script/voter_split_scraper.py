import json
import requests

from multiprocessing.dummy import Pool as ThreadPool


def get_candidate_data(candidate, ac_code):
    name = candidate['CandidateName']
    code = candidate['CandidateCode']
    r = requests.post("https://kgis.ksrsac.in/electionportal/Election.asmx/Polled_votes_classbreak",
                      json={'ac_code': ac_code, 'candidatecode': code})
    ps_split = json.loads(json.loads(r.text)['d'])
    return {"name": name, "code": code, "vote_split": ps_split}


def get_candidates_data(constituency):
    ac_name = constituency['ASBLY_CSTNY_NAME']
    ac_code = constituency['ASBLY_CSTNY_ID']

    r = requests.post("https://kgis.ksrsac.in/electionportal/Election.asmx/Get_ddlCandidateslist",
                      json={'ac_code': ac_code})

    candidates = json.loads(json.loads(r.text)['d'])
    data = {"ac_name": ac_name, "ac_code": ac_code, "candidates": []}

    for candidate in candidates:
        data["candidates"].append(get_candidate_data(candidate, ac_code))
    return data


def get_constiuency_data(district_code, district_name):
    r = requests.post("https://kgis.ksrsac.in/electionportal/Election.asmx/Getassembly",
                      json={'selectedAOICode': 'ECD03',
                            'selectedval': district_code})

    constituencies = json.loads(json.loads(r.text)['d'])
    data = {"district_name": district_name, "district_code": district_code, "constituencies": []}
    pool = ThreadPool(6)
    data["constituencies"] = pool.map(get_candidates_data, constituencies)
    # for constituency in constituencies:
    #     data["constituencies"].append(get_candidates_data(constituency))
    return data


json.dump(get_constiuency_data(20, "Bangalore Urban"), open("Urban.json", 'w'))
json.dump(get_constiuency_data(21, "Bangalore Rural"), open("Rural.json", 'w'))
# get_constiuency_data(21, "Bangalore Rural")
