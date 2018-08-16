# !/usr/bin/env python
import sys
import traceback

import json
import requests
import sqlite3 as lite
from bs4 import BeautifulSoup
import pandas as pd

final_page_number = 111
start_page_number = 1

try:
    start_page_number = int(sys.argv[1])
except:
    print("Running from page 1")

url = "http://www.mybmtc.com/service/timings/gns/General%20Services"
db = 'bmtc.sqlite'


def load_routes(start, end):
    con = lite.connect(db)
    cur = con.cursor()
    for page_number in range(start, end):
        print("=========================" + str(page_number) + "==========================================")
        html_url = ""
        if page_number == 1:
            html_url = "http://www.mybmtc.com/service/timings/gns/General%20Services"
        else:
            html_url = "http://www.mybmtc.com/service/timings/gns/General%20Services?page=" + str(page_number)

        html_src = requests.get(html_url)

        soup = BeautifulSoup(html_src.content)
        tables = soup.findAll("table")
        listing_table = tables[0]
        # print(listing_table)
        first = True
        for i in listing_table.findAll('tr'):
            if first:
                row = i.text
                first = False
            else:
                route = i.find("p", {"id": "routeno"})
                route_text = route.text.replace("Route NO:", "")

                origin = i.find("p", {"id": "origin"})
                origin_text = origin.text.replace("Origin :", "")

                destination = i.findAll("p", {"id": "destination"})
                destination_text = destination[0].text.replace("Destination :", "")
                destination_time_text = destination[1].text.replace("Journey Time :", "")
                destination_distance_text = destination[2].text.replace("Journey Distance :", "")

                viewbusstop = i.find("p", {"id": "viewbusstop"})
                viewbusstop_anchor = viewbusstop.findAll("a")
                buststop_list = viewbusstop_anchor[0]['href']
                buststop_map = viewbusstop_anchor[1]['href']

                # "departure_from_origin", "arrival_at_destination", "departure_from_destination", "arrival_at_origin"

                departure_from_origin = i.find("td", {"id": "Origin_Start_time"})
                departure_from_origin_text = departure_from_origin.text

                departure_from_origin_all = i.findAll("td", {"id": "Departure_Start_time"})
                arrival_at_destination_text = departure_from_origin_all[0].text
                departure_from_destination_text = departure_from_origin_all[1].text
                arrival_at_origin_text = departure_from_origin_all[2].text

                document = {"route_no": route_text, "origin": origin_text, "destination": destination_text,
                            "map_link": buststop_map, "busstops_link": buststop_list, "time": destination_time_text,
                            "distance": destination_distance_text, "departure_from_origin": departure_from_origin_text,
                            "arrival_at_destination": arrival_at_destination_text,
                            "departure_from_destination": departure_from_destination_text,
                            "arrival_at_origin": arrival_at_origin_text}

                cur.execute(
                    'INSERT INTO routes (route_no, origin, destination, map_link, busstops_link, time, distance, '
                    'departure_from_origin, arrival_at_destination, departure_from_destination, arrival_at_origin) '
                    'VALUES (:route_no, :origin, :destination, :map_link, :busstops_link, :time, :distance, '
                    ':departure_from_origin, :arrival_at_destination, :departure_from_destination, '
                    ':arrival_at_origin)',
                    document)
                print(document)
                con.commit()
    con.close()


def load_bus_stop_map_json():
    con = lite.connect(db)
    cur = con.cursor()
    cur.execute("select map_link, route_no  FROM routes where map_json_content is null")
    rows = cur.fetchall()
    cur2 = con.cursor()
    print(rows.__len__())
    for row in rows[8:]:
        try:
            document = get_json_content(row)
            cur2.execute("update routes set map_json_content=:map_json_content where route_no=:route_no", document)
            con.commit()
        except:
            pass
    con.close()


def get_json_content(row):
    url = row[0]
    route_no = row[1]
    print(url)
    html_src = requests.get(url)
    soup = BeautifulSoup(html_src.content)
    scripts = soup.findAll("script")
    our_script = scripts[6]
    script_text = our_script.text
    script_text = script_text.replace("jQuery.extend(Drupal.settings, ", "")
    script_text = script_text[:-2]
    # print(script_text
    data = json.loads(script_text)
    print(data['busstops'])
    document = {"map_json_content": json.dumps(data['busstops']), "route_no": route_no}
    return document


def load_bus_stop():
    con = lite.connect(db)
    cur = con.cursor()
    cur.execute("select map_json_content, route_no  FROM routes where map_json_content is not null")
    rows = cur.fetchall()
    cur2 = con.cursor()
    for row in rows:
        try:
            map_json_content = row[0]
            route_no = row[1]
            # print(map_json_content
            order = 0
            data = json.loads(map_json_content)
            for stop in data:
                # print(stop
                order = order + 1
                print(order)
                print(route_no)
                # document ={"name": stop['busstop'], "lat": stop['latlons'][0], "lng": stop['latlons'][1]}
                # cur2.execute('INSERT INTO busstop (name,lat,lng) VALUES (:name, :lat, :lng)', document)

                document_2 = {"busstop": stop['busstop'], "route_no": route_no, "serial": str(order)}
                cur2.execute('INSERT INTO bus_route (route_no,busstop,serial) VALUES (:route_no, :busstop, :serial)',
                             document_2)
                print("Done")
                con.commit()

        except:
            print("Exception in user code:")
            print('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)

    con.close()


def load_timings():
    con = lite.connect(db)
    cur = con.cursor()
    cur.execute(
        "select route_no, departure_from_origin, arrival_at_destination, departure_from_destination, "
        "arrival_at_origin  FROM routes ")
    rows = cur.fetchall()
    cur2 = con.cursor()
    for row in rows:
        try:
            route_no = row[0]
            departure_from_origin = (row[1]).split(",")
            arrival_at_destination = (row[2]).split(",")
            departure_from_destination = (row[3]).split(",")
            arrival_at_origin = (row[4]).split(",")

            for i in range(len(departure_from_origin)):
                start = (departure_from_origin[i]).strip()
                end = (arrival_at_destination[i]).strip()
                document_2 = {"route_no": route_no, "start": start, "end": end, "up": 1}
                cur2.execute(
                    'INSERT INTO timings (route_no , start , end , up) VALUES (:route_no , :start , :end , :up)',
                    document_2)
                print("up")
                con.commit()

            for j in range(len(departure_from_destination)):
                start = (departure_from_destination[j]).strip()
                end = (arrival_at_origin[j]).strip()
                document_2 = {"route_no": route_no, "start": start, "end": end, "up": 0}
                cur2.execute(
                    'INSERT INTO timings (route_no , start , end , up) VALUES (:route_no , :start , :end , :up)',
                    document_2)
                print("down")
                con.commit()

        except:
            print("Exception in user code:")
            print('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)

    con.close()


def clear_db():
    con = lite.connect(db)
    cur = con.cursor()
    cur.execute('DELETE from routes')
    con.commit()
    cur.execute('DELETE from bus_route')
    con.commit()
    cur.execute('DELETE from timings')
    con.commit()
    con.close()


def export_to_csv():
    # Open the file
    routes_file = open('routes.csv', 'w')
    bus_route_file = open('bus_route.csv', 'w')
    timings_file = open('timings.csv', 'w')

    connection = lite.connect(db)
    cursor1 = connection.cursor()
    cursor1.execute('select * from routes')
    write_to_file(cursor1, routes_file)
    routes_file.close()
    cursor1.close()
    cursor2 = connection.cursor()
    cursor2.execute('select * from bus_route')
    write_to_file(cursor2, bus_route_file)
    cursor2.close()
    bus_route_file.close()
    cursor3 = connection.cursor()
    cursor3.execute('select * from timings')
    write_to_file(cursor3, timings_file)
    timings_file.close()
    cursor3.close()
    connection.close()


def write_to_file(cursor, file):
    add_header = True
    while True:
        df = pd.DataFrame(cursor.fetchmany(1000))
        if len(df) == 0:
            break
        else:
            df.to_csv(file, mode="a", header=add_header)
            add_header = False


# clear_db()

# load_routes(start_page_number, final_page_number)
# loadBusstopMapJSON()
# loadBusStop()
# load_timings()
export_to_csv()
