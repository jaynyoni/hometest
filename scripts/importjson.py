import json


def loadjson_func(file_url):
    #define variables
    source_file_url =file_url
    target_file_url ="../Data/output/events_summary.json"

    journeyjson = {}
    journeyjson['Type'] = {}
    journeyjson['Data'] = []
    timetablejson = {}
    timetablejson['Type'] = {}
    timetablejson['Data'] = []
    stopsjson = {}
    stopsjson['Type'] = {}
    stopsjson['Data'] = []
    #open the file to load for logic checking
    with open(source_file_url,'r') as json_data:
        classlist = json.load(json_data)
        i = 0
        while i < len(classlist):
            #load only succesful journey posts (statuscode = 201)
            if classlist[i].get("requestMethod") == 'POST' and 'journey' in classlist[i].get("requestUri"):
                if classlist[i]['responseStatusCode'] == 201:

                    journeyrequestid = classlist[i].get("requestId")
                    journeydict = json.loads(classlist[i]['responseContentBody'])
                    journeyorigin = journeydict['geometry']['coordinates'][0]
                    journeydestination = journeydict['geometry']['coordinates'][1]

                    requestContentBody = classlist[i]['requestContentBody']
                    requestTimestamp = classlist[i]['requestTimestamp']
                    responseContentBody = classlist[i].get("responseContentBody")
                    responseContentBodydict = json.loads(classlist[i]['responseContentBody'])
                    journeymodes = responseContentBodydict['only']['modes']
                    try:
                        total_travel_time = responseContentBodydict['itineraries'][0]['duration']
                    except IndexError:
                        total_travel_time = ''
                    requestQueryString = classlist[i].get("requestQueryString")
                    response = classlist[i]['responseStatusCode']
                    journeyjson['Type'] = "journey"
                    journeyjson['Data'].append({
                    "Origin": journeyorigin,
                    "Destination": journeydestination,
                    "Modes_Used": journeymodes,
                    "Total_Travel_Time": total_travel_time,
                    "Timestamp": requestTimestamp
                    })



            #load timetable calls and only successful ones, also logic to exclude lines calls as the uri in some cases was similar to the timetable one
            elif 'timetables' in classlist[i].get("requestUri") and '/api/lines' not in classlist[i].get("requestUri"):
                if classlist[i]['responseStatusCode'] == 200:
                    responseContentBody = classlist[i].get("responseContentBody")
                    requestQueryString = classlist[i].get("requestQueryString")
                    response = classlist[i]['responseStatusCode']
                    requestUri = classlist[i].get("requestUri")
                    requestTimestamp = classlist[i]['requestTimestamp']
                    timtabledict = json.loads(classlist[i]['responseContentBody'])
                    try:
                        agency_id = timtabledict[0]['line']['agency']['id']
                    except IndexError:
                        agency_id = ''
                    try:
                        agency_name = timtabledict[0]['line']['agency']['name']
                    except IndexError:
                        agency_name = ''
                    timetablejson['Type'] = "timetable"
                    timetablejson['Data'].append({
                    "AgencyName": agency_name,
                    "AgencyID": agency_id,
                    "Timestamp": requestTimestamp
                    })

            # load stops calls and only succesful ones statuscode = 200
            elif '/api/stops' in classlist[i].get("requestUri"):
                if classlist[i]['responseStatusCode'] == 200:
                    requestContentBody = classlist[i].get("requestContentBody")
                    responseContentBody = classlist[i].get("responseContentBody")
                    requestQueryString = classlist[i].get("requestQueryString")
                    requestUri = classlist[i].get("requestUri")
                    requestTimestamp = classlist[i]['requestTimestamp']
                    if not responseContentBody:
                        stopsdict = json.loads(responseContentBody)
                        try:
                            stops_agency_name = stopsdict['agency']['name']
                        except IndexError:
                            stops_agency_name = ''
                        try:
                            stops_agency_id = stopsdict['agency']['id']
                        except IndexError:
                            stops_agency_id = ''
                        response = classlist[i]['responseStatusCode']
                        stopsjson['Type'] = "stops"
                        stopsjson['Data'].append({
                            "AgencyName": stops_agency_name,
                            "AgencyID": stops_agency_id,
                            "count": 1,
                            "Timestamp": requestTimestamp
                        })



            i=i+1
        jsonfinal  = [journeyjson, timetablejson, stopsjson]
        prettyjsonfinal = json.dumps(jsonfinal, indent=4)



    with open(target_file_url, 'a') as targetfile:
        targetfile.write(prettyjsonfinal)
    #return the count of json files loaded
    c = len(prettyjsonfinal)
    return(c)





