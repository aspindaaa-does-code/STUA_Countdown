import stua, time

stua.keyMTA("<INSERT MTA KEY HERE>") 
stua.keyBUSTIME("<INSERT BUSTIME KEY HERE>")

CRIT_RATE = [6, 7, 9, 12, 12]

def refresh():
    json_string = {
        "access": "Welcome to the StuyTransit Departure Board API!",
    }
    return json_string

def subway():

    global CRIT_RATE

    seventh_ave_crit = CRIT_RATE[0]
    eighth_avenue_crit = CRIT_RATE[1]
    broadway_crit = CRIT_RATE[2]
    nassau_crit = CRIT_RATE[3]
    lexington_avenue_crit = CRIT_RATE[4]

    masterlistSUBWAY = stua.gtfsSubwayBATCHED([("137", "N", 1, seventh_ave_crit, "NONE"), ("137", "N", 2, seventh_ave_crit, "NONE"), ("137", "N", 3, seventh_ave_crit, "NONE"), ("137", "N", 4, seventh_ave_crit, "NONE"), ("137", "N", 5, seventh_ave_crit, "NONE"), #0-4
                                        ("137", "S", 1, seventh_ave_crit, "NONE"), ("137", "S", 2, seventh_ave_crit, "NONE"), ("137", "S", 3, seventh_ave_crit, "NONE"), ("137", "S", 4, seventh_ave_crit, "NONE"), ("137", "S", 5, seventh_ave_crit, "NONE"), #5-9
                                        ("A34", "N", 1, eighth_avenue_crit, "NONE"), ("A34", "N", 2, eighth_avenue_crit, "NONE"), ("A34", "N", 3, eighth_avenue_crit, "NONE"), ("A34", "N", 4, eighth_avenue_crit, "NONE"), ("A34", "N", 5, eighth_avenue_crit, "NONE"), #10-14
                                        ("A36", "S", 1, eighth_avenue_crit, "NONE"), ("A36", "S", 2, eighth_avenue_crit, "NONE"), ("A36", "S", 3, eighth_avenue_crit, "NONE"), ("A36", "S", 4, eighth_avenue_crit, "NONE"), ("A36", "S", 5, eighth_avenue_crit, "NONE"), #15-19
                                        ("R24", "S", 1, broadway_crit, "NONE"), ("R24", "S", 2, broadway_crit, "NONE"), ("R24", "S", 3, broadway_crit, "NONE"), ("R24", "S", 4, broadway_crit, "NONE"), ("R24", "S", 5, broadway_crit, "NONE"), #20-24
                                        ("640", "N", 1, lexington_avenue_crit, "NONE"), ("640", "N", 2, lexington_avenue_crit, "NONE"), ("640", "N", 3, lexington_avenue_crit, "NONE"), ("640", "N", 4, lexington_avenue_crit, "NONE"), ("640", "N", 5, lexington_avenue_crit, "NONE"), #25-29
                                        ("M21", "N", 1, nassau_crit, "NONE"), ("M21", "N", 2, nassau_crit, "NONE"), ("M21", "N", 3, nassau_crit, "NONE"), ("M21", "N", 4, nassau_crit, "NONE"), ("M21", "N", 5, nassau_crit, "NONE") #30-34
    ])

    return masterlistSUBWAY

def bus():

    masterlistBUS = stua.gtfsBusBATCHED([("404969", 0, 1, 1, "NONE"), ("404969", 0, 2, 1, "NONE"), #0-1
                                        ("803147", 0, 1, 2, "NONE"), ("803147", 0, 2, 2, "NONE"), #2-3
                                        ("404238", 1, 1, 7, "SIM1"), ("404238", 1, 2, 7, "SIM1"), ("404238", 1, 1, 7, "SIM2"), ("404238", 1, 2, 7, "SIM2"), #4-7
                                        ("404225", 1, 1, 7, "X27"), ("404225", 1, 2, 7, "X27"), ("404225", 1, 1, 7, "X28"), ("404225", 1, 2, 7, "X28"), ("405065", 0, 1, 1, "M20"), ("405065", 0, 2, 1, "M20"), ("903013", 1, 1, 6, "SIM7"), ("903013", 1, 2, 6, "SIM7"), #8-15
                                        ("903013", 1, 1, 6, "SIM33"), ("903013", 1, 2, 6, "SIM33"), ("404219", 1, 1, 7, "SIM34"), ("404219", 1, 2, 7, "SIM34")]) #16-19

  
    return masterlistBUS

def lirr():
    masterlistLIRR = stua.gtfsLIRRBATCHED([("237", "0", 1, 20, ["Port Washington", "Hempstead"]), ("241", "0", 1, 20, []), ("349", "0", 1, 20, ["Port Washington", "Hempstead"])])
    return masterlistLIRR

def modlirrTIME(input):
    if type(input) == str:
        return "00:00"
    t = input.strftime("%I:%M %p")
    if t[0] == "0":
        t = t[1:]
    return t

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

def export():

    t1 = time.time()

    masterlistSUBWAY = subway()
    masterlistBUS = bus()

    bbch = masterlistSUBWAY[25:35]

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

    json_string = {
        "uptown_seventh": {
            "1": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[0].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[0].time}",
                "terminus": [f"To: {masterlistSUBWAY[0].terminus}"],
                "borough": f"{masterlistSUBWAY[0].terminus_borough}"
            },
            "2": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[1].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[1].time}",
                "terminus": [f"To: {masterlistSUBWAY[1].terminus}"],
                "borough": f"{masterlistSUBWAY[1].terminus_borough}"
            },
            "3": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[2].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[2].time}",
                "terminus": [f"To: {masterlistSUBWAY[2].terminus}"],
                "borough": f"{masterlistSUBWAY[2].terminus_borough}"
            },
            "4": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[3].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[3].time}",
                "terminus": [f"To: {masterlistSUBWAY[3].terminus}"],
                "borough": f"{masterlistSUBWAY[3].terminus_borough}"
            },
            "5": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[4].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[4].time}",
                "terminus": [f"To: {masterlistSUBWAY[4].terminus}"],
                "borough": f"{masterlistSUBWAY[4].terminus_borough}"
            }
        },
        "uptown_eighth": {
            "1": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[10].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[10].time}",
                "terminus": [f"To: {masterlistSUBWAY[10].terminus}"],
                "borough": f"{masterlistSUBWAY[10].terminus_borough}"
            },
            "2": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[11].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[11].time}",
                "terminus": [f"To: {masterlistSUBWAY[11].terminus}"],
                "borough": f"{masterlistSUBWAY[11].terminus_borough}"
            },
            "3": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[12].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[12].time}",
                "terminus": [f"To: {masterlistSUBWAY[12].terminus}"],
                "borough": f"{masterlistSUBWAY[12].terminus_borough}"
            },
            "4": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[13].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[13].time}",
                "terminus": [f"To: {masterlistSUBWAY[13].terminus}"],
                "borough": f"{masterlistSUBWAY[13].terminus_borough}"
            },
            "5": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[14].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[14].time}",
                "terminus": [f"To: {masterlistSUBWAY[14].terminus}"],
                "borough": f"{masterlistSUBWAY[14].terminus_borough}"
            }
        },
        "uptown_bbch": {
            "1": {
                "emblem": f"/static/svg/{(bbch[0].route_id).lower()}.svg",
                "time": f"{bbch[0].time}",
                "terminus": [f"To: {bbch[0].terminus}"],
                "borough": f"{bbch[0].terminus_borough}"
            },
            "2": {
                "emblem": f"/static/svg/{(bbch[1].route_id).lower()}.svg",
                "time": f"{bbch[1].time}",
                "terminus": [f"To: {bbch[1].terminus}"],
                "borough": f"{bbch[1].terminus_borough}"
            },
            "3": {
                "emblem": f"/static/svg/{(bbch[2].route_id).lower()}.svg",
                "time": f"{bbch[2].time}",
                "terminus": [f"To: {bbch[2].terminus}"],
                "borough": f"{bbch[2].terminus_borough}"
            },
            "4": {
                "emblem": f"/static/svg/{(bbch[3].route_id).lower()}.svg",
                "time": f"{bbch[3].time}",
                "terminus": [f"To: {bbch[3].terminus}"],
                "borough": f"{bbch[3].terminus_borough}"
            },
            "5": {
                "emblem": f"/static/svg/{(bbch[4].route_id).lower()}.svg",
                "time": f"{bbch[4].time}",
                "terminus": [f"To: {bbch[4].terminus}"],
                "borough": f"{bbch[4].terminus_borough}"
            },
        },
        "downtown_seventh": {
            "1": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[5].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[5].time}",
                "terminus": [f"To: {masterlistSUBWAY[5].terminus}"],
                "borough": f"{masterlistSUBWAY[5].terminus_borough}"
            },
            "2": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[6].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[6].time}",
                "terminus": [f"To: {masterlistSUBWAY[6].terminus}"],
                "borough": f"{masterlistSUBWAY[6].terminus_borough}"
            },
            "3": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[7].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[7].time}",
                "terminus": [f"To: {masterlistSUBWAY[7].terminus}"],
                "borough": f"{masterlistSUBWAY[7].terminus_borough}"
            },
            "4": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[8].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[8].time}",
                "terminus": [f"To: {masterlistSUBWAY[8].terminus}"],
                "borough": f"{masterlistSUBWAY[8].terminus_borough}"
            },
            "5": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[9].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[9].time}",
                "terminus": [f"To: {masterlistSUBWAY[9].terminus}"],
                "borough": f"{masterlistSUBWAY[9].terminus_borough}"
            },
        },
        "downtown_eighth": {
            "1": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[15].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[15].time}",
                "terminus": [f"To: {masterlistSUBWAY[15].terminus}"],
                "borough": f"{masterlistSUBWAY[15].terminus_borough}"
            },
            "2": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[16].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[16].time}",
                "terminus": [f"To: {masterlistSUBWAY[16].terminus}"],
                "borough": f"{masterlistSUBWAY[16].terminus_borough}"
            },
            "3": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[17].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[17].time}",
                "terminus": [f"To: {masterlistSUBWAY[17].terminus}"],
                "borough": f"{masterlistSUBWAY[17].terminus_borough}"
            },
            "4": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[18].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[18].time}",
                "terminus": [f"To: {masterlistSUBWAY[18].terminus}"],
                "borough": f"{masterlistSUBWAY[18].terminus_borough}"
            },
            "5": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[19].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[19].time}",
                "terminus": [f"To: {masterlistSUBWAY[19].terminus}"],
                "borough": f"{masterlistSUBWAY[19].terminus_borough}"
            },
        },
        "downtown_broadway": {
            "1": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[20].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[20].time}",
                "terminus": [f"To: {masterlistSUBWAY[20].terminus}"],
                "borough": f"{masterlistSUBWAY[20].terminus_borough}"
            },
            "2": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[21].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[21].time}",
                "terminus": [f"To: {masterlistSUBWAY[21].terminus}"],
                "borough": f"{masterlistSUBWAY[21].terminus_borough}"
            },
            "3": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[22].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[22].time}",
                "terminus": [f"To: {masterlistSUBWAY[22].terminus}"],
                "borough": f"{masterlistSUBWAY[22].terminus_borough}"
            },
            "4": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[23].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[23].time}",
                "terminus": [f"To: {masterlistSUBWAY[23].terminus}"],
                "borough": f"{masterlistSUBWAY[23].terminus_borough}"
            },
            "5": {
                "emblem": f"/static/svg/{(masterlistSUBWAY[24].route_id).lower()}.svg",
                "time": f"{masterlistSUBWAY[24].time}",
                "terminus": [f"To: {masterlistSUBWAY[24].terminus}"],
                "borough": f"{masterlistSUBWAY[24].terminus_borough}"
            },
        },
        "bus": {
            "M20": {
                "route": f"{masterlistBUS[12].route_id}",
                "time": f"{masterlistBUS[12].time}"
            },
            "SIM7": {
                "route": f"{masterlistBUS[14].route_id}",
                "time": f"{masterlistBUS[14].time}"
            },
            "SIM33": {
                "route": f"{masterlistBUS[16].route_id}",
                "time": f"{masterlistBUS[16].time}"
            },
            "SIM34": {
                "route": f"{masterlistBUS[18].route_id}",
                "time": f"{masterlistBUS[18].time}"
            }
        },
        "ferry": {
            "time": f"{ferry.time}"
        }
    }

    print("SUBWAY/BUS: " + str(time.time() - t1))

    return json_string