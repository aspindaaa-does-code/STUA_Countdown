"""
Ravindra Mangar
Last Updated: 2023-12-19
Project: STUA Countdown Board

stua.py
----------------------------------------
This file is used to retrieve real-time transit data from the MTA and LIRR.
It is also used to receive real-time alerts from the MTA and LIRR.
For ferry data at Vesey Street, this file pulls real-time data from the NYC Ferry API.
----------------------------------------
"""

# Imports
import aiohttp, asyncio, traceback, concurrent.futures, multiprocessing # for optimizations
import requests, csv, datetime, math, os, json, calendar, traceback # for data retrieval and cleaning
import time as te
from xml.etree.ElementTree import fromstring, ElementTree as ET # for data retrieval and cleaning

# Google Transit Feed Imports
import gtfs_realtime_pb2
import nyct_subway_pb2

APIMTA = ""
APIBUSTIME = ""

# Classes for each transit type
class gtfsSubway():
    def __init__(self):
        self.route_id = ""
        self.terminus = ""
        self.terminus_id = ""
        self.station = ""
        self.station_id = ""
        self.direction = ""
        self.time = 0
        self.service_pattern = ""
        self.service_description = ""
        self.trip_id = ""

    def set(self, route_id, terminus, terminus_id, station, station_id, direction, time, pattern, description, trip_id, current_id, terminus_borough):
        self.route_id = route_id
        self.terminus = terminus
        self.terminus_id = terminus_id
        self.station = station
        self.station_id = station_id
        self.direction = direction
        self.time = time
        self.service_pattern = pattern
        self.service_description = description
        self.trip_id = trip_id
        self.current_id = current_id
        self.terminus_borough = terminus_borough

class gtfsBus():
    def __init__(self):
        self.route_id = ""
        self.terminus = ""
        self.terminus_id = ""
        self.stop = ""
        self.stop_id = ""
        self.time = ""
        self.service_pattern = ""
        self.direction = 0
        self.trip_id = ""
        self.vehicle = ""

    def set(self, route_id, terminus, terminus_id, stop, stop_id, time, service_pattern, direction, trip_id, vehicle):
        self.route_id = route_id
        self.terminus = terminus
        self.terminus_id = terminus_id
        self.stop = stop
        self.stop_id = stop_id
        self.time = time
        self.service_pattern = service_pattern
        self.direction = direction
        self.trip_id = trip_id
        self.vehicle = vehicle

class gtfsLIRR():
    def __init__(self):
        self.route_id = ""
        self.terminus = ""
        self.terminus_id = ""
        self.station = ""
        self.station_id = ""
        self.direction = ""
        self.time = 0
        self.service_pattern = ""
        self.service_description = ""
        self.station_id_list = ""
        self.station_name_list = ""
        self.trip_id = ""
        self.vehicle = ""
        self.core_time = ""
        self.color = ""

    def set(self, route_id, terminus_id, station_id, direction, time, pattern, description, trip_id, station_id_list, vehicle, core_time, color):
        self.route_id = route_id
        self.terminus = convertLIRR(terminus_id)
        self.terminus_id = terminus_id
        self.station = convertLIRR(station_id)
        self.station_id = station_id
        self.direction = direction
        self.time = time
        self.service_pattern = pattern
        self.service_description = description
        self.station_id_list = station_id_list
        self.station_name_list = [convertLIRR(i) for i in station_id_list]
        self.trip_id = trip_id
        self.vehicle = vehicle
        self.core_time = core_time
        self.color = color

class gtfsFerry():
    def __init__(self):
        self.route_id_SN = ""
        self.route_id_LN = ""
        self.terminus = ""
        self.terminus_id = ""
        self.stop = ""
        self.stop_id = ""
        self.time = 0
        self.trip_id = ""
        self.vehicle = ""
        self.stop_list = ""
        self.stop_id_list = ""

    def get(self, stop, target, responses):
        _responseIndex(responses)
        output = _transitFerry(stop, target, responses)
        if (output == "NO FERRIES"):
            self.route_id_SN = "NO FERRIES"
            self.route_id_LN = "NO FERRIES"
            self.terminus = "NO FERRIES"
            self.terminus_id = "NO FERRIES"
            self.stop = convertFerry(stop)
            self.stop_id = stop
            self.time = "X"
            self.trip_id = "NO FERRIES"
            self.vehicle = "NO FERRIES"
            self.stop_list = "NO FERRIES"
            self.stop_id_list = "NO FERRIES"
        else:
            self.route_id_SN = output[7]
            self.route_id_LN = output[8]
            self.terminus = convertFerry(output[1])
            self.terminus_id = output[1]
            self.stop = convertFerry(output[2])
            self.stop_id = output[2]
            self.time = output[0]
            self.trip_id = output[3]
            self.vehicle = output[6]
            self.stop_list = output[9]
            self.stop_id_list = output[10]

    def set(self, route_id_SN, route_id_LN, terminus_id, stop_id, time, trip_id, vehicle, stop_list, stop_id_list):
        self.route_id_SN = route_id_SN
        self.route_id_LN = route_id_LN
        self.terminus = convertFerry(terminus_id)
        self.terminus_id = terminus_id
        self.stop = convertFerry(stop_id)
        self.stop_id = stop_id
        self.time = time
        self.trip_id = trip_id
        self.vehicle = vehicle
        self.stop_list = stop_list
        self.stop_id_list = stop_id_list

# Creates an event loop if one does not exist
def _get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            except:
                pass
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

def _responseIndex(index):
    if (index <= 0):
        raise Exception("INVALID RESPONSES INDEX, MUST BE > 0")

# Sorts the list of objects by time
def sort(objects):
    if (objects == []):
        return False
    for i in objects:
        if (hasattr(i, "time") == False):
            return False
        if (i.time == "X"):
            i.time = 999
        
    objects.sort(key = lambda x: x.time)
    for i in objects:
        if (i.time == 999):
            i.time = "X"
    return True

def keyMTA(string):
    global APIMTA
    _validkeySubway(string)
    APIMTA = string

def keyBUSTIME(string):
    global APIBUSTIME
    _validkeyBus(string)
    APIBUSTIME = string

def _getAPIMTA():
    return APIMTA

def _getAPIBUSTIME():
    return APIBUSTIME

def _timeconvert(input):
    out = datetime.datetime.now() + datetime.timedelta(minutes=input)
    return out.strftime('%H:%M')

def _validkeySubway(key):
    if (str(requests.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs", headers={'x-api-key' : key}))) != "<Response [200]>":
        raise Exception("INVALID KEY")

def _validkeyBus(key):
    if (str(requests.get(f'http://bustime.mta.info/api/where/stop/MTA_550320.xml?key={key}'))) != "<Response [200]>":
        raise Exception("INVALID KEY")

# Converts a bus stop ID to a bus stop name
def convertBus(input):
    if type(input) != type("") and type(input) != type(0):
        raise Exception("INVALID CLASS: This method requires a String or an Integer")
    if (type(input) == type(0)):
        input = str(input)
    responsestop = requests.get(f'http://bustime.mta.info/api/where/stop/MTA_{input}.xml?key={_getAPIBUSTIME()}')
    tree = ET(fromstring(responsestop.content))
    root = tree.getroot()
    stop_name = root[4][4].text
    return stop_name

# Converts a subway stop ID to a subway stop name
def convertSubway(input):
    if type(input) != type(""):
        raise Exception("INVALID CLASS: This method requires a String")
    output = []
    with open('stops.txt','r') as csv_file:
        if (len(input) == 3):
            csv_file = csv.reader(csv_file)
            for row in csv_file:
                if row[2] == input:
                    output.append(row[5])
                    output.append(row[6])
        else:

            raise Exception("INVALID ARGUMENT")
    if (len(output) == 1):
        for i in output: return i
    else:
        return output

# Converts a LIRR stop ID to a LIRR stop name
def convertLIRR(input):
    output = ""
    if type(input) != type(""):
        raise Exception("INVALID CLASS: This method requires a String")
    if (type(input) == type(0)):
        input = str(input)
    #print(input)
    f = open("lirr_gtfs.json")
    data = json.load(f)
    #print(data["gtfs"]["stops"])
    for i in data["gtfs"]["stops"]:
        if input == i["stop_id"]:
            output = i["stop_name"]
    
    return output

# Converts a LIRR route ID to a LIRR route name
def convertLIRR_route(input):
    
    db = json.load(open("lirr_routes.json"))
    
    try:
        return (db[str(input)]["branch"], db[str(input)]["color"])
    except:
        return (db["12"]["branch"], db["12"]["color"])


# Converts a ferry stop ID to a ferry stop name
def convertFerry(input):
    if type(input) != type(""):
        raise Exception("INVALID CLASS: This method requires a String")
    output = []
    with open('ferry_stops.txt','r') as csv_file:
        csv_file = csv.reader(csv_file)
        for row in csv_file:
            if row[0] == input:
                output.append(row[2])
    if (len(output) == 1):
        for i in output: return i
    else:
        return output

# Asynchronous requests to the MTA API
async def _requestMTA(session, url, API):
    async with session.get(url, headers={'x-api-key' : API}) as response:
        data = await response.read()
    return data

async def _requestFeedMTA(sites, API):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(_requestMTA(session, url, API))
            tasks.append(task)
        out = await asyncio.gather(*tasks, return_exceptions=True)
        return out

# Asynchronous requests to the BusTime API
async def _requestBustime(session, url):
    async with session.get(url) as response:
        
        data = await response.read()
    return data

async def _requestFeedBustime(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(_requestBustime(session, url))
            tasks.append(task)
        out = await asyncio.gather(*tasks, return_exceptions=True)
        return out

# List of URLs for the MTA API. Because the MTA API is split into multiple feeds, this list is used to request all of the feeds at once.
# For example, if F trains are running on the A line, those trains would only appear on the F feed. This list is used to request both the A and F feeds.
def _url():
    link = []
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-si')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs')
    return link

# Worker function for the asynchranous parsing of MTA Subway Data
def _transitSubwayWorker(stop, links, current_time, final, cur):
    try:
        times = []
        for link in links:
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(link)

            for entity in feed.entity:
                destination = []
                for update in entity.trip_update.stop_time_update:
                    if (update.stop_id == stop[0]+stop[1]):
                        station_id = update.stop_id[:-1]
                        direction = update.stop_id[-1]
                        time = update.arrival.time
                        if (time < 0):
                            time = update.departure.time
                        time = datetime.datetime.fromtimestamp(time)
                        time = math.trunc(((time - current_time).total_seconds()) / 60)
                        if (time < stop[3]):
                            continue
                        trip_id = entity.trip_update.trip.trip_id
                        route_id = entity.trip_update.trip.route_id
                        if (stop[4] != "NONE" and stop[4] != route_id):
                            continue
                        for update in entity.trip_update.stop_time_update:
                            destination.append(update.stop_id)
                        terminus_id = destination[-1][:-1]
                        current_id = destination[0][:-1]
                        train = gtfsSubway()
                        description = _routes(route_id)
                        convertStation = convertSubway(station_id)
                        convertTerminus = convertSubway(terminus_id)

                        train.set(route_id, convertTerminus[0], terminus_id, convertStation[0], station_id, direction, time, description[0], description[1], trip_id, current_id, convertTerminus[1])
                        times.append(train)

        sort(times)
        final.append([cur, times[stop[2]-1]])
    except Exception as e:

        train = gtfsSubway()
        train.set("X", "NO TRAINS", "NO TRAINS", "NO TRAINS", stop[0], stop[1], "X", "NO TRAINS", "NO TRAINS", "NO TRAINS", "NO TRAINS", "NO TRAINS")
        final.append([cur, train])

# Asynchronous parsing of MTA Subway Data
# The function is divided into two parts. The first part uses the Asyncio module to asynchronously request all links of the MTA API.
# The second part uses the Multiprocessing module to asynchronously parse the data from the MTA API.
def _transitSubway(stops, API):

    with multiprocessing.Manager() as manager:
        final = manager.list()

        current_time = datetime.datetime.now()
        links = _get_or_create_eventloop().run_until_complete(_requestFeedMTA(_url(), API))
        num = len(stops)
        cur = 0
        time0 = te.time()
        pool = concurrent.futures.ProcessPoolExecutor()
        for stop in stops:
            cur += 1
            pool.submit(_transitSubwayWorker, stop, links, current_time, final, cur)

        pool.shutdown(wait=True)
        final.sort()

        final = [i[1] for i in final]

    return final

# Synchranous parsing of MTA Bus Data
# Because the entire BusTime API can be requested at once, this function requests the entire API and then parses the data for every inputted stop.
def _transitBus(stops, API):
    final = []
    current_time = datetime.datetime.now()
    while True:
        try:
            link = requests.get(f"http://gtfsrt.prod.obanyc.com/tripUpdates?key={API}")
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(link.content)
            break
        except:
         
            te.sleep(5)
    for stop in stops:
        try:
            times = []
            destination = []

            for entity in feed.entity:
                for update in entity.trip_update.stop_time_update:

                    if ((update.stop_id == stop[0]) and (str(entity.trip_update.trip.direction_id) == str(stop[1]))):
                        time = update.arrival.time
                        if (time < 0):
                            time = update.departure.time
                        time = datetime.datetime.fromtimestamp(time)
                        time = math.trunc(((time - current_time).total_seconds()) / 60)
                        if (time < stop[3]):
                            continue
                        trip_id = entity.trip_update.trip.trip_id
                        route_id = entity.trip_update.trip.route_id
                        if (stop[4] != "NONE" and stop[4] != route_id):
                            continue
                        vehicle = entity.trip_update.vehicle.id[-4:]
                        stop_id = update.stop_id
                        for update in entity.trip_update.stop_time_update:
                            destination.append(update.stop_id)
                        terminus_id = destination[-1]
                        direction = entity.trip_update.trip.direction_id

                        bus = gtfsBus()
                        bus.set(route_id, f'http://bustime.mta.info/api/where/stop/MTA_{terminus_id}.xml?key={API}', terminus_id, f'http://bustime.mta.info/api/where/stop/MTA_{stop_id}.xml?key={API}', stop_id, time, "", direction, trip_id, vehicle)
                        times.append(bus)
            sort(times)
            final.append(times[stop[2]-1])

        except:
            bus = gtfsBus()
            bus.set("NONE", "NO BUSES", "NO BUSES", "NO BUSES", "NO BUSES", "X", "NO BUSES", "NO BUSES", "NO BUSES", "NO BUSES")
            final.append(bus)

    download = []
    for item in final:
        download.append(item.stop)

        download.append(item.terminus)
 
    download = _get_or_create_eventloop().run_until_complete(_requestFeedBustime(download))

    for num in range(0, len(final)):
        try:
        
            tree = ET(fromstring(download[num*2]))
            root = tree.getroot()
            stop_name = root[4][4].text
            for item in root[4][7]:
                if (item[1].text == route_id):
                    service_pattern = item[3].text
            final[num].stop = stop_name
            final[num].service_pattern = service_pattern

            tree = ET(fromstring(download[(num*2)+1]))
            root = tree.getroot()
            terminus_name = root[4][4].text
            final[num].terminus = terminus_name
        except:
            final[num].stop = "NO BUSES"
            final[num].service_pattern = "NO BUSES"
            final[num].terminus = "NO BUSES"

    return final

# Worker function for the asynchranous parsing of MTA LIRR Data
def _transitLIRRWorker(stop, direction, responses, minute, target_routes, lister, feed, cur):
    times = []
    current_time = datetime.datetime.now()
    
    try:
        for entity in feed.entity:
            destination = []
            for update in entity.trip_update.stop_time_update:
                if str(entity.trip_update.trip.schedule_relationship) == "3":
                    continue
           
                if ((update.stop_id == stop) and (str(entity.trip_update.trip.direction_id) == str(direction))):
                
                    station_id = update.stop_id
                    time = update.departure.time
                 
                    time = datetime.datetime.fromtimestamp(time)
                 
                    core_time = time
                    time = math.trunc(((time - current_time).total_seconds()) / 60)
                
                    if (time < 0):
                        continue
                    if (time < minute):
                        continue
               
                    try:
                        vehicle = entity.trip_update.trip.trip_id.split("_")[3]
                     
                    except:
                       
                        vehicle = "ERR"
                    trip_id = entity.trip_update.trip.trip_id
                    route = convertLIRR_route(entity.trip_update.trip.route_id)
                    route_id = route[0]
                    color = route[1]
                
                    if target_routes == []:
                        pass
                    else:
                        if route_id not in target_routes:
                            continue
                    direction = entity.trip_update.trip.direction_id
                    station_id_list = []
                    for update in entity.trip_update.stop_time_update:
                        destination.append(update.stop_id)
                        station_id_list.append(update.stop_id)
                   
                    station_stop_list = [convertLIRR(i) for i in station_id_list]
                  
                    terminus_id = destination[-1]

                    train = gtfsLIRR()
                   
                    train.set(route_id, terminus_id, stop, direction, time, "NO TRAINS", "NO TRAINS", trip_id, station_id_list, vehicle, core_time, color)
                  
                    times.append(train)
                   
        sort(times)

        times = times[responses-1]
       
        lister.append([cur, times])

    except:
        
        e = gtfsLIRR()
        #print(traceback.format_exc())
        e.set("NO TRAINS", "NO TRAINS", stop, direction, "X", "NO TRAINS", "NO TRAINS", "NO TRAINS", ["NO TRAINS"], "NO TRAINS", "00:00 XM", "NO TRAINS")
        lister.append([cur, e])

# Asynchronous parsing of MTA LIRR Data
# The function is divided into two parts. The first part requestd the entire LIRR feed from the MTA API.
# The second part uses the Multiprocessing module to asynchronously parse the data from the MTA API for each stop.
def _transitLIRR(inputt, API):
   
    while True:
        try:
            links = _get_or_create_eventloop().run_until_complete(_requestFeedMTA([f"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/lirr%2Fgtfs-lirr"], API))
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(links[0])
            break
        except:
            
            te.sleep(5)
    
    with multiprocessing.Manager() as manager:
        final = manager.list()
        
        cur = 0
        pool = concurrent.futures.ProcessPoolExecutor()
        for stop in inputt:
            cur += 1
            pool.submit(_transitLIRRWorker, stop[0], stop[1], stop[2], stop[3], stop[4], final, feed, cur)

        pool.shutdown(wait=True)
       
        final.sort()
        
        final = [i[1] for i in final]

    return final

# Retrieves real-time ferry data from the NYC Ferry API
def _transitFerry(stop, target, responses):
    try:
        current_time = datetime.datetime.now()
        times = []
        destination = []
      
        response = requests.get("http://nycferry.connexionz.net/rtt/public/utility/gtfsrealtime.aspx/tripupdate")
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)

        for entity in feed.entity:
            for update in entity.trip_update.stop_time_update:
                
                if (update.stop_id == stop):
                   
                    station_id = update.stop_id
                    time = update.arrival.time
                    if (time < 0):
                        time = update.departure.time
                    time = datetime.datetime.fromtimestamp(time)
                    time = math.trunc(((time - current_time).total_seconds()) / 60)
                
                    if (time < 0):
                        continue
                    trip_id = entity.trip_update.trip.trip_id
               
                    station_id_list = []
                    for update in entity.trip_update.stop_time_update:
                        destination.append(update.stop_id)
                        station_id_list.append(update.stop_id)
          
                    if target in station_id_list:
                        continue
                    station_stop_list = [convertFerry(i) for i in station_id_list]
                
                    terminus_id = destination[-1]
                    vehicle = entity.trip_update.vehicle.label

                    with open('ferry_trips.txt','r') as csv_file:
                        csv_file = csv.reader(csv_file)
                        for row in csv_file:
                            if row[2] == trip_id:
                                route_id_SN = row[0]

                    with open('ferry_routes.txt','r') as csv_file:
                        csv_file = csv.reader(csv_file)
                        for row in csv_file:
                            if row[0] == route_id_SN:
                                route_id_LN = row[3]


                    times.append([time, terminus_id, station_id, trip_id, station_id_list, station_stop_list, vehicle, route_id_SN, route_id_LN, station_stop_list, station_id_list])
              
        times.sort()

        times = times[responses-1]
    except:
        return "NO FERRIES"

    return times

# Gets the route description and route name for a given route ID
def _routes(service):
    with open('routes.txt','r') as csv_file:
        csv_file = csv.reader(csv_file)
        for row in csv_file:
            if row[0] == service:
                return row[3], row[4], row[6]

# Retrieves MTA Subway Service Change data
# If planned is set to False, then only unplanned service changes will be returned
def alertsSubway(planned=True):
   
    alerts = []
    response = requests.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts", headers={'x-api-key' : _getAPIMTA()})
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)


    for entity in feed.entity:
        for start in entity.alert.active_period:
            if (int(start.end) == 0) or (int(start.start) < calendar.timegm((datetime.datetime.utcnow()).utctimetuple()) < int(start.end)):
                if planned == False:
                    if "planned_work" not in entity.id:
                        if (entity.alert.header_text.translation):
                            for update in entity.alert.header_text.translation:
                                if update.language == "en-html":
                                        alerts.append([[item.route_id for item in entity.alert.informed_entity if item.route_id != ""], entity.alert.header_text.translation[0].text])
                else:
                    if (entity.alert.header_text.translation):
                        for update in entity.alert.header_text.translation:
                            if update.language == "en-html":
                                alerts.append([[item.route_id for item in entity.alert.informed_entity if item.route_id != ""], entity.alert.header_text.translation[0].text])

    delays = [i[1] for i in alerts]
    emblems = [i[0] for i in alerts]

    results_emblem = []
    results_delays = []
    for i in range(0, len(delays)):
        if delays[i] not in results_delays:
            results_delays.append(delays[i])
            results_emblem.append(emblems[i])
        else:
            for item in emblems[i]:
                index = results_delays.index(delays[i])
                results_emblem[index].append(item)

    output = []

    for i in range(0, len(results_delays)):
        output.append([results_emblem[i], results_delays[i]])

    return output

# Returns MTA LIRR Service Change data
# If planned is set to False, then only unplanned service changes will be returned
def alertsLIRR(planned=False):
    alerts = []
    response = requests.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Flirr-alerts", headers={'x-api-key' : _getAPIMTA()})
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    for entity in feed.entity:
        for start in entity.alert.active_period:
            if int(start.start) < calendar.timegm((datetime.datetime.utcnow()).utctimetuple()) < int(start.end):
                if planned == False:
                    if "planned_work" not in entity.id:
                        if (entity.alert.header_text.translation):
                            for update in entity.alert.header_text.translation:
                                if update.language == "en-html":
                                    alerts.append([[item.route_id for item in entity.alert.informed_entity if item.route_id != ""], entity.alert.header_text.translation[0].text])
                else:
                    if (entity.alert.header_text.translation):
                        for update in entity.alert.header_text.translation:
                            if update.language == "en-html":
                                alerts.append([[item.route_id for item in entity.alert.informed_entity if item.route_id != ""], entity.alert.header_text.translation[0].text])
    return alerts

# Returns MTA Bus Service Change data
# If planned is set to False, then only unplanned service changes will be returned
def alertsBus(planned=False):
    alerts = []
    response = requests.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fbus-alerts", headers={'x-api-key' : _getAPIMTA()})
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    for entity in feed.entity:
        for start in entity.alert.active_period:
            if int(start.start) < calendar.timegm((datetime.datetime.utcnow()).utctimetuple()) < int(start.end):
                if planned == False:
                    if "planned_work" not in entity.id:
                        if (entity.alert.header_text.translation):
                            for update in entity.alert.header_text.translation:
                                if update.language == "en-html":
                                    alerts.append([[item.route_id for item in entity.alert.informed_entity if item.route_id != ""], entity.alert.header_text.translation[0].text])
                else:
                    if (entity.alert.header_text.translation):
                        for update in entity.alert.header_text.translation:
                            if update.language == "en-html":
                                alerts.append([[item.route_id for item in entity.alert.informed_entity if item.route_id != ""], entity.alert.header_text.translation[0].text])
    return alerts

# Returns NYC Ferry Service Change data
def alertsFerry():
    alerts = []
    response = requests.get("http://nycferry.connexionz.net/rtt/public/utility/gtfsrealtime.aspx/alert")
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    for entity in feed.entity:
        for start in entity.alert.active_period:
            if int(start.start) < calendar.timegm((datetime.datetime.utcnow()).utctimetuple()) < int(start.end):
                if (entity.alert.header_text.translation):
                    for update in entity.alert.header_text.translation:
                        if update.language == "en-html":
                            alerts.append(entity.alert.header_text.translation[0].text)
    return alerts

# Caller functions for each transit type
def gtfsSubwayBATCHED(stops):
    output = _transitSubway(stops, _getAPIMTA())
    return output

def gtfsBusBATCHED(stops):
    output = _transitBus(stops, _getAPIBUSTIME())
    return output

def gtfsLIRRBATCHED(params):
    output = _transitLIRR(params, _getAPIMTA())
    return output