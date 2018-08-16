from itertools import repeat

import json
import requests

from multiprocessing.dummy import Pool as ThreadPool


def get_constituency_data(ac_no):
    ac_payload = {'ac_code': ac_no}

    try:

        ac_data = request_data_from_election_portal(
            "http://kgis.ksrsac.in/electionportal/Election.asmx/GetAssemblyDetails",
            ac_payload)

        polling_data = get_polling_data(ac_payload)

        candidates_data = request_data_from_election_portal(
            "https://kgis.ksrsac.in/electionportal/Election.asmx/GetAssemblyContestantsDetails", ac_payload)[0]

        winner_details = request_data_from_election_portal(
            "http://kgis.ksrsac.in/electionportal/Election.asmx/GetAssembly2018WinnersDetails", ac_payload)

        voting_perc = request_data_from_election_portal(
            "https://kgis.ksrsac.in/electionportal/Election.asmx/VotingPercentageByAC", ac_payload)[0]

        assembly_candidate_votes = request_data_from_election_portal(
            "https://kgis.ksrsac.in/electionportal/Election.asmx/GetAssembly2018CandidateVotes", ac_payload)[0]
        assembly_candidate_votes.pop("Candidate_Photo", None)

        candidates_basic_details = request_data_from_election_portal(
            "http://kgis.ksrsac.in/electionportal/Election.asmx/GetCandidateBasicDetails", ac_payload)

        for candidate in candidates_basic_details:
            candidate.pop("Candidate_Photo", None)

        present_data = ac_data[0]
        data = {
            2018: {**present_data, **candidates_data, **voting_perc, **assembly_candidate_votes,
                   "winner_details": winner_details, "candidates_basic_details": candidates_basic_details},
            2013: ac_data[1],
            2008: ac_data[2],
            "pollbooth_data": polling_data,

        }

        json.dump(data, open(str(ac_no) + ".json", "w"))


    except:
        print("fetching details failed for constituency" + str(ac_no))
        return
    return data


def get_booth_details(booth_no, ac_no):
    return request_data_from_election_portal(
        "https://kgis.ksrsac.in/electionportal/Election.asmx/GetIdentifierDeatils",
        {"ps_code": str(ac_no) + "-" + str(booth_no)})


def get_polling_data(ac_payload):
    polling_data = request_data_from_election_portal(
        "https://kgis.ksrsac.in/electionportal/Election.asmx/GetAssemblyTotalBoothDetails", ac_payload
    )[0]

    pool = ThreadPool(6)
    booth_details = pool.starmap(get_booth_details,
                                 zip(range(1, polling_data["POLLING_BOOTH"] + 1), repeat(ac_payload["ac_code"])))
    # for booth in range(1, polling_data["POLLING_BOOTH"] + 1):
    #     booth_details.append(request_data_from_election_portal(
    #         "https://kgis.ksrsac.in/electionportal/Election.asmx/GetIdentifierDeatils",
    #         {"ps_code": str(ac_payload["ac_code"]) + "-" + str(booth)}))
    pool.close()

    polling_data["booth_details"] = booth_details
    return polling_data


def request_data_from_election_portal(url, json_payload):
    r = requests.post(url,
                      json=json_payload)
    return json.loads(json.loads(r.text)['d'])


def scrape_ac_data():
    # urban_thd_pool = ThreadPool(2)
    # urban_ac_details = urban_thd_pool.map(get_constituency_data, range(150, 178))  # Bengaluru urban constituency range
    #
    # json.dump(urban_ac_details, open("urban_ac_details.json", "w"))
    # urban_thd_pool.close()
    rural_thd_pool = ThreadPool(2)
    rural_ac_details = rural_thd_pool.map(get_constituency_data, range(178, 182))  # Bengaluru rural constituency range

    json.dump(rural_ac_details, open("rural_ac_details.json", "w"))
    rural_thd_pool.close()


scrape_ac_data()

# print({154: get_constituency_data(154)})
# get_polling_data({"ac_code": 162})
