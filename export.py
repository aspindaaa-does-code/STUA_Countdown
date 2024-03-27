"""
Ravindra Mangar
Last Updated: 2023-12-19
Project: STUA Countdown Board

export.py
----------------------------------------
This file is used to organize transit data from stua.py and format it into a JSON string for the front-end to use.
MTA and BusTime keys can be found on the MTA Developer Portal and BusTime Developer Portal respectively.
----------------------------------------
"""

import stua, time

# Input API Keys here
stua.keyMTA("nVSXwNVJi45sBz1O6mDEE2adIk3VeP9t1qbgETSf") 
stua.keyBUSTIME("6f064d4d-ed7d-415a-9d4a-c01204897506")

# This is the minimum countdown time for a train to be displayed on the board, organized by line
# The order is: Seventh Avenue Lines, Eighth Avenue Lines, Broadway Lines, Nassau Ave Lines, Lexington Avenue Lines
CRIT_RATE = [6, 7, 9, 12, 12]

# This is for the front-end JSON homepage
def refresh():
    json_string = {
        "access": "Welcome to the StuyTransit Departure Board API!",
    }
    return json_string

# This is for the front-end JSON homepage, and simply grabs data from stua.py without any modifications to the format
def subway():

    global CRIT_RATE

    seventh_ave_crit = CRIT_RATE[0]
    eighth_avenue_crit = CRIT_RATE[1]
    broadway_crit = CRIT_RATE[2]
    nassau_crit = CRIT_RATE[3]
    lexington_avenue_crit = CRIT_RATE[4]

    masterlistSUBWAY = stua.gtfsSubwayBATCHED([("137", "N", 1, seventh_ave_crit, []), ("137", "N", 2, seventh_ave_crit, []), ("137", "N", 3, seventh_ave_crit, []), ("137", "N", 4, seventh_ave_crit, []), ("137", "N", 5, seventh_ave_crit, []), #0-4
                                        ("137", "S", 1, seventh_ave_crit, []), ("137", "S", 2, seventh_ave_crit, []), ("137", "S", 3, seventh_ave_crit, []), ("137", "S", 4, seventh_ave_crit, []), ("137", "S", 5, seventh_ave_crit, []), #5-9
                                        ("A34", "N", 1, eighth_avenue_crit, []), ("A34", "N", 2, eighth_avenue_crit, []), ("A34", "N", 3, eighth_avenue_crit, []), ("A34", "N", 4, eighth_avenue_crit, []), ("A34", "N", 5, eighth_avenue_crit, []), #10-14
                                        ("A36", "S", 1, eighth_avenue_crit, []), ("A36", "S", 2, eighth_avenue_crit, []), ("A36", "S", 3, eighth_avenue_crit, []), ("A36", "S", 4, eighth_avenue_crit, []), ("A36", "S", 5, eighth_avenue_crit, []), #15-19
                                        ("R24", "S", 1, broadway_crit, []), ("R24", "S", 2, broadway_crit, []), ("R24", "S", 3, broadway_crit, []), ("R24", "S", 4, broadway_crit, []), ("R24", "S", 5, broadway_crit, []), #20-24
                                        ("640", "N", 1, lexington_avenue_crit, []), ("640", "N", 2, lexington_avenue_crit, []), ("640", "N", 3, lexington_avenue_crit, []), ("640", "N", 4, lexington_avenue_crit, []), ("640", "N", 5, lexington_avenue_crit, []), #25-29
                                        ("M21", "N", 1, nassau_crit, ["J", "Z"]), ("M21", "N", 2, nassau_crit, ["J", "Z"]), ("M21", "N", 3, nassau_crit, ["J", "Z"]), ("M21", "N", 4, nassau_crit, ["J", "Z"]), ("M21", "N", 5, nassau_crit, ["J", "Z"]), #30-34
                                        ("M21", "S", 1, nassau_crit, ["M"]), ("M21", "S", 2, nassau_crit, ["M"]), ("M21", "S", 3, nassau_crit, ["M"]), ("M21", "S", 4, nassau_crit, ["M"]), ("M21", "S", 5, nassau_crit, ["M"]) #35-39
    ])

    return masterlistSUBWAY

# This is for the front-end JSON homepage, and simply grabs data from stua.py without any modifications to the format
def bus():

    masterlistBUS = stua.gtfsBusBATCHED([
            ("404969", 1, 3, "M22"), ("404969", 2, 3, "M22"), ("803147", 1, 5, "M9"), ("803147", 2, 5, "M9"),
            ("404186", 1, 9, "X27"), ("404186", 2, 9, "X27"), ("404186", 1, 9, "X28"), ("404186", 2, 9, "X28"),
            ("404224", 1, 9, "SIM1"), ("404224", 2, 9, "SIM1"), ("903013", 1, 6, "SIM7"), ("903013", 2, 6, "SIM7"),
            ("404238", 1, 11, "SIM4"), ("404238", 2, 11, "SIM4"), ("404238", 1, 11, "SIM4X"), ("404238", 2, 11, "SIM4X"),
            ("903013", 1, 11, "SIM33"), ("903013", 2, 11, "SIM33"), ("404219", 1, 9, "SIM34"), ("404219", 2, 9, "SIM34"),
            ("903013", 1, 1, "SIM9"), ("903013", 2, 1, "SIM9"), ("450402", 1, 15, "SIM15"), ("450402", 2, 15, "SIM15")
    ])
    return masterlistBUS

# This is for the front-end JSON homepage, and simply grabs data from stua.py without any modifications to the format
def lirr():
    masterlistLIRR = stua.gtfsLIRRBATCHED([("237", "0", 1, 20, ["Port Washington", "Hempstead"]), ("241", "0", 1, 20, []), ("349", "0", 1, 20, ["Port Washington", "Hempstead"])])
    return masterlistLIRR

# Converts a datetime object into a string in the format of "HH:MM AM/PM"
def modlirrTIME(input):
    if type(input) == str:
        return "00:00"
    t = input.strftime("%I:%M %p")
    if t[0] == "0":
        t = t[1:]
    return t

# Takes raw return from lirr() and formats it into a JSON string for the front-end to use
def export_lirr():
    t1 = time.time()
    masterlistLIRR = lirr()
    json_string = {
        "lirr": {
            "crit": [f"{masterlistLIRR[0].time}", f"{masterlistLIRR[1].time}", f"{masterlistLIRR[2].time}"],
            "time": [f"{modlirrTIME(masterlistLIRR[0].core_time)}", f"{modlirrTIME(masterlistLIRR[1].core_time)}", f"{modlirrTIME(masterlistLIRR[2].core_time)}"],
            "color": [f"#{masterlistLIRR[0].color}", f"#{masterlistLIRR[1].color}", f"#{masterlistLIRR[2].color}"],
            "branch": [f"{masterlistLIRR[0].route_id}", f"{masterlistLIRR[1].route_id}", f"{masterlistLIRR[2].route_id}"],
            "dest": [masterlistLIRR[0].terminus, masterlistLIRR[1].terminus, masterlistLIRR[2].terminus],
            "stops": [f"{' - '.join(masterlistLIRR[0].station_name_list)}", f"{' - '.join(masterlistLIRR[1].station_name_list)}", f"{' - '.join(masterlistLIRR[2].station_name_list)}"],
            "vehicle": [f"{masterlistLIRR[0].vehicle}", f"{masterlistLIRR[1].vehicle}", f"{masterlistLIRR[2].vehicle}"]
        }
    }
    print("LIRR: " + str(time.time() - t1))

    return json_string

# Takes raw return from subway() and bus(), along with a stua.gtfsFerry() call, and formats it into a JSON string for the front-end to use
def export():

    t1 = time.time()

    masterlistSUBWAY = subway()
    masterlistBUS = bus()

    bbch = masterlistSUBWAY[25:40]

    # Because Nassau Ave and Lexington Ave lines use different GTFS links, this complies both lists into one and sorts the trains by time

    stua.sort(bbch)
    bbch = bbch[:5]

    for i in bbch:
        if i.route_id == "5X":
            i.route_id = "5"
    
    for i in masterlistSUBWAY:
        if i.route_id == "5X":
            i.route_id = "5"

    ferry = stua.gtfsFerry()
    ferry.get("136", "137", 1)

    bus_sim17 = masterlistBUS[8:10]
    stua.sort(bus_sim17)
    bus_sim44x = masterlistBUS[10:12]
    stua.sort(bus_sim44x)
    bus_sim3344 = masterlistBUS[12:14]
    stua.sort(bus_sim3344)
    bus_sim915 = masterlistBUS[14:16]
    stua.sort(bus_sim915)

    json_string = {
        "uptown_seventh": {
            "1": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[0].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[0].time}",
                "terminus": [f"To: {masterlistSUBWAY[0].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[0].terminus_id}",
                "borough": f"{masterlistSUBWAY[0].terminus_borough}"
            },
            "2": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[1].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[1].time}",
                "terminus": [f"To: {masterlistSUBWAY[1].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[1].terminus_id}",
                "borough": f"{masterlistSUBWAY[1].terminus_borough}"
            },
            "3": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[2].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[2].time}",
                "terminus": [f"To: {masterlistSUBWAY[2].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[2].terminus_id}",
                "borough": f"{masterlistSUBWAY[2].terminus_borough}"
            },
            "4": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[3].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[3].time}",
                "terminus": [f"To: {masterlistSUBWAY[3].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[3].terminus_id}",
                "borough": f"{masterlistSUBWAY[3].terminus_borough}"
            },
            "5": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[4].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[4].time}",
                "terminus": [f"To: {masterlistSUBWAY[4].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[4].terminus_id}",
                "borough": f"{masterlistSUBWAY[4].terminus_borough}"
            }
        },
        "uptown_eighth": {
            "1": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[10].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[10].time}",
                "terminus": [f"To: {masterlistSUBWAY[10].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[10].terminus_id}",
                "borough": f"{masterlistSUBWAY[10].terminus_borough}"
            },
            "2": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[11].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[11].time}",
                "terminus": [f"To: {masterlistSUBWAY[11].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[11].terminus_id}",
                "borough": f"{masterlistSUBWAY[11].terminus_borough}"
            },
            "3": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[12].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[12].time}",
                "terminus": [f"To: {masterlistSUBWAY[12].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[12].terminus_id}",
                "borough": f"{masterlistSUBWAY[12].terminus_borough}"
            },
            "4": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[13].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[13].time}",
                "terminus": [f"To: {masterlistSUBWAY[13].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[13].terminus_id}",
                "borough": f"{masterlistSUBWAY[13].terminus_borough}"
            },
            "5": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[14].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[14].time}",
                "terminus": [f"To: {masterlistSUBWAY[14].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[14].terminus_id}",
                "borough": f"{masterlistSUBWAY[14].terminus_borough}"
            }
        },
        "uptown_bbch": {
            "1": {
                "emblem": f"/static/svg/{(bbch[0].route_id).lower()}.svg",
                "time": f"{bbch[0].time}",
                "terminus": [f"To: {bbch[0].terminus}"],
                "terminus_id": f"{bbch[0].terminus_id}",
                "borough": f"{bbch[0].terminus_borough}"
            },
            "2": {
                "emblem": f"/static/svg/{(bbch[1].route_id).lower()}.svg",
                "time": f"{bbch[1].time}",
                "terminus": [f"To: {bbch[1].terminus}"],
                "terminus_id": f"{bbch[1].terminus_id}",
                "borough": f"{bbch[1].terminus_borough}"
            },
            "3": {
                "emblem": f"/static/svg/{(bbch[2].route_id).lower()}.svg",
                "time": f"{bbch[2].time}",
                "terminus": [f"To: {bbch[2].terminus}"],
                "terminus_id": f"{bbch[2].terminus_id}",
                "borough": f"{bbch[2].terminus_borough}"
            },
            "4": {
                "emblem": f"/static/svg/{(bbch[3].route_id).lower()}.svg",
                "time": f"{bbch[3].time}",
                "terminus": [f"To: {bbch[3].terminus}"],
                "terminus_id": f"{bbch[3].terminus_id}",
                "borough": f"{bbch[3].terminus_borough}"
            },
            "5": {
                "emblem": f"/static/svg/{(bbch[4].route_id).lower()}.svg",
                "time": f"{bbch[4].time}",
                "terminus": [f"To: {bbch[4].terminus}"],
                "terminus_id": f"{bbch[4].terminus_id}",
                "borough": f"{bbch[4].terminus_borough}"
            },
        },
        "downtown_seventh": {
            "1": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[5].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[5].time}",
                "terminus": [f"To: {masterlistSUBWAY[5].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[5].terminus_id}",
                "borough": f"{masterlistSUBWAY[5].terminus_borough}"
            },
            "2": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[6].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[6].time}",
                "terminus": [f"To: {masterlistSUBWAY[6].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[6].terminus_id}",
                "borough": f"{masterlistSUBWAY[6].terminus_borough}"
            },
            "3": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[7].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[7].time}",
                "terminus": [f"To: {masterlistSUBWAY[7].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[7].terminus_id}",
                "borough": f"{masterlistSUBWAY[7].terminus_borough}"
            },
            "4": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[8].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[8].time}",
                "terminus": [f"To: {masterlistSUBWAY[8].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[8].terminus_id}",
                "borough": f"{masterlistSUBWAY[8].terminus_borough}"
            },
            "5": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[9].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[9].time}",
                "terminus": [f"To: {masterlistSUBWAY[9].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[9].terminus_id}",
                "borough": f"{masterlistSUBWAY[9].terminus_borough}"
            },
        },
        "downtown_eighth": {
            "1": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[15].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[15].time}",
                "terminus": [f"To: {masterlistSUBWAY[15].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[15].terminus_id}",
                "borough": f"{masterlistSUBWAY[15].terminus_borough}"
            },
            "2": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[16].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[16].time}",
                "terminus": [f"To: {masterlistSUBWAY[16].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[16].terminus_id}",
                "borough": f"{masterlistSUBWAY[16].terminus_borough}"
            },
            "3": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[17].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[17].time}",
                "terminus": [f"To: {masterlistSUBWAY[17].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[17].terminus_id}",
                "borough": f"{masterlistSUBWAY[17].terminus_borough}"
            },
            "4": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[18].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[18].time}",
                "terminus": [f"To: {masterlistSUBWAY[18].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[18].terminus_id}",
                "borough": f"{masterlistSUBWAY[18].terminus_borough}"
            },
            "5": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[19].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[19].time}",
                "terminus": [f"To: {masterlistSUBWAY[19].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[19].terminus_id}",
                "borough": f"{masterlistSUBWAY[19].terminus_borough}"
            },
        },
        "downtown_broadway": {
            "1": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[20].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[20].time}",
                "terminus": [f"To: {masterlistSUBWAY[20].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[20].terminus_id}",
                "borough": f"{masterlistSUBWAY[20].terminus_borough}"
            },
            "2": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[21].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[21].time}",
                "terminus": [f"To: {masterlistSUBWAY[21].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[21].terminus_id}",
                "borough": f"{masterlistSUBWAY[21].terminus_borough}"
            },
            "3": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[22].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[22].time}",
                "terminus": [f"To: {masterlistSUBWAY[22].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[22].terminus_id}",
                "borough": f"{masterlistSUBWAY[22].terminus_borough}"
            },
            "4": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[23].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[23].time}",
                "terminus": [f"To: {masterlistSUBWAY[23].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[23].terminus_id}",
                "borough": f"{masterlistSUBWAY[23].terminus_borough}"
            },
            "5": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[24].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[24].time}",
                "terminus": [f"To: {masterlistSUBWAY[24].terminus}"],
                "terminus_id": f"{masterlistSUBWAY[24].terminus_id}",
                "borough": f"{masterlistSUBWAY[24].terminus_borough}"
            },
        },
        "bus": {
            "M22": {
                "route": f"{masterlistBUS[0].route_id}",
                "time": f"{masterlistBUS[0].time}",
                "stop": f"{masterlistBUS[0].stop}",
                "terminus": f"{masterlistBUS[0].terminus}"
            },
            "M9": {
                "route": f"{masterlistBUS[2].route_id}",
                "time": f"{masterlistBUS[2].time}",
                "stop": f"{masterlistBUS[2].stop}",
                "terminus": f"{masterlistBUS[2].terminus}"
            },
            "X27": {
                "route": f"{masterlistBUS[4].route_id}",
                "time": f"{masterlistBUS[4].time}",
                "stop": f"{masterlistBUS[4].stop}",
                "terminus": f"{masterlistBUS[4].terminus}"
            },
            "X28": {
                "route": f"{masterlistBUS[6].route_id}",
                "time": f"{masterlistBUS[6].time}",
                "stop": f"{masterlistBUS[6].stop}",
                "terminus": f"{masterlistBUS[6].terminus}"
            },
            "SIM17": {
                "route": f"{bus_sim17[0].route_id}",
                "time": f"{bus_sim17[0].time}",
                "stop": f"{bus_sim17[0].stop}",
                "terminus": f"{bus_sim17[0].terminus}"
            },
            "SIM44X": {
                "route": f"{bus_sim44x[0].route_id}",
                "time": f"{bus_sim44x[0].time}",
                "stop": f"{bus_sim44x[0].stop}",
                "terminus": f"{bus_sim44x[0].terminus}"
            },
            "SIM3334": {
                "route": f"{bus_sim3344[0].route_id}",
                "time": f"{bus_sim3344[0].time}",
                "stop": f"{bus_sim3344[0].stop}",
                "terminus": f"{bus_sim3344[0].terminus}"
            },
            "SIM915": {
                "route": f"{bus_sim915[0].route_id}",
                "time": f"{bus_sim915[0].time}",
                "stop": f"{bus_sim915[0].stop}",
                "terminus": f"{bus_sim915[0].terminus}"
            }

        },
        "ferry": {
            "time": f"{ferry.time}"
        }
    }

    print("SUBWAY/BUS: " + str(time.time() - t1))

    return json_string