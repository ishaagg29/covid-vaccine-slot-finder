import requests
import json
import csv
import argparse
from datetime import datetime, timedelta

output_file_state = "covid_vaccine_available_slots_your_state.csv"
output_file_district = "covid_vaccine_available_slots_your_district.csv"
output_file_pincode = "covid_vaccine_available_slots_your_pincode.csv"

def get_all_slots_for_a_state(state_name, date, minAge):
    print "Fetching vaccination slots for state : {} for the next 3 days after : {} for minimum age : {}\n".format(state_name, date, minAge)
    state_id = get_state_id(state_name)
    if(state_id != "Invalid"):
        district_list = get_all_districts_of_a_state(state_id)
        with open(output_file_state, 'a') as file:
            mywriter = csv.DictWriter(file, fieldnames=["vaccine_name", "centre_name", "available_capacity", "fees", "district", "date"])
            mywriter.writeheader()
            for i in range(3):
                for district in district_list:
                    centre_list = get_slots_by_district_id(state_name, None, district["district_id"], date)
                    slots_available = False
                    for centre in centre_list :
                        if(centre["min_age_limit"] == int(minAge) and centre["available_capacity"] > 0):
                            slots_available = True
                            centre_row = dict()
                            centre_row["vaccine_name"] = centre["vaccine"]
                            centre_row["centre_name"] = centre["name"]
                            centre_row["available_capacity"] = centre["available_capacity"]
                            centre_row["fees"] = centre["fee"]
                            centre_row["district"] = district["district_name"]
                            centre_row["date"] = date
                            mywriter.writerow(centre_row)

                    if(slots_available == False):
                        print("No slots available in district : " + str(district["district_id"]) + " for date : " + date)
                date = (datetime.strptime(date, '%d-%m-%Y') + timedelta(days=1)).strftime('%d-%m-%Y')
    else :
        print "Invalid state name : {} .. Pls try again using state name in title case!".format(state_name)



def get_all_slots_for_a_district(state_name, district_name, date, minAge):
    print "Fetching vaccination slots for state : {}, district : {} for the next 7 days after : {} for minimum age : {}\n".format(state_name, district_name, date, minAge)
    with open(output_file_district, 'a') as file:
        mywriter = csv.DictWriter(file, fieldnames=["vaccine_name", "centre_name", "available_capacity", "fees", "district", "date"])
        mywriter.writeheader()
        invalidDistrict = False
        for i in range(7):
            slots_available = False
            centre_list = get_slots_by_district_id(state_name, district_name, None, date)
            if(centre_list is not None):
                for centre in centre_list :
                    if(centre["min_age_limit"] == int(minAge) and centre["available_capacity"] > 0):
                        slots_available = True
                        centre_row = dict()
                        centre_row["vaccine_name"] = centre["vaccine"]
                        centre_row["centre_name"] = centre["name"]
                        centre_row["available_capacity"] = centre["available_capacity"]
                        centre_row["fees"] = centre["fee"]
                        centre_row["district"] = district_name
                        centre_row["date"] = date
                        mywriter.writerow(centre_row)
                if(slots_available == False):
                    print "No slots available for date : " + date
                date = (datetime.strptime(date, '%d-%m-%Y') + timedelta(days=1)).strftime('%d-%m-%Y')
            else :
                invalidDistrict = True
        if(invalidDistrict):
            print "Invalid district name : {} ..Pls try again. District names are case sensitive!".format(district_name)

def get_slots_by_pincode_and_date(pincode, date, minAge):
    print "Fetching vaccination slots for pincode : {} for the next 7 days after : {} for minimum age : {}\n".format(pincode, date, minAge)
    headers = {"accept": "application/json","Accept-Language": "hi_IN"}
    with open(output_file_pincode, 'a') as file:
        mywriter = csv.DictWriter(file, fieldnames=["vaccine_name", "centre_name", "available_capacity", "fees", "pincode", "date"])
        mywriter.writeheader()
        for i in range(7):
            response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=" + str(pincode) + "&date=" + str(date), headers = headers).text
            centre_list = json.loads(response)["sessions"]
            slots_available = False
            for centre in centre_list :
                if(centre["min_age_limit"] == int(minAge) and centre["available_capacity"] > 0):
                    slots_available = True
                    centre_row = dict()
                    centre_row["vaccine_name"] = centre["vaccine"]
                    centre_row["centre_name"] = centre["name"]
                    centre_row["available_capacity"] = centre["available_capacity"]
                    centre_row["fees"] = centre["fee"]
                    centre_row["pincode"] = pincode
                    centre_row["date"] = date
                    mywriter.writerow(centre_row)

            if(slots_available == False):
                print "No slots available for date : " + date
            date = (datetime.strptime(date, '%d-%m-%Y') + timedelta(days=1)).strftime('%d-%m-%Y')

##----------------Private methods-----

def get_slots_by_district_id(state_name, district_name, district_id, date):
    state_id = get_state_id(state_name)
    if(state_id != "Invalid"):
        if(district_id is None):
            district_id = get_district_id(state_id, district_name)
        if(district_id != "Invalid"):
            headers = {"accept": "application/json","Accept-Language": "hi_IN"}
            response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=" + str(district_id) + "&date=" + str(date), headers= headers).text
            # print json.loads(response)["sessions"]
            return json.loads(response)["sessions"]
        else :
            print "Invalid district name : {} ..Pls try again. District names are case sensitive!".format(district_name)
    else :
        print "Invalid state name : {} .. Pls try again using state name in title case!".format(state_name)


def get_district_id(state_id, district_name):
    district_list = get_all_districts_of_a_state(state_id)
    for district in district_list:
        if(district["district_name"] == district_name):
            # print district["district_id"]
            return district["district_id"]
    return "Invalid"

def get_all_districts_of_a_state(state_id):
    headers = {"accept": "application/json","Accept-Language": "hi_IN"}
    response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/" + str(state_id), headers = headers).text
    return json.loads(response)["districts"]

def get_state_id(state_name):
    headers = {"accept": "application/json","Accept-Language": "hi_IN"}
    response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/states", headers = headers).text
    state_list = json.loads(response)["states"]
    for state in state_list:
        if(state["state_name"] == state_name):
            return state["state_id"]

    return "Invalid"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pincode', help='Pincode for which you want to search vaccine availability')
    parser.add_argument('--state', help='State name for which you want to search vaccine availability [Title Case]')
    parser.add_argument('--district', help='District name for which you want to search vaccine availability [Title Case]')
    parser.add_argument('--date', help='Start date after which you want to search vaccine availability. [Format : dd-mm-yyyy]')
    parser.add_argument('--minAge', help='Minimum age (18 or 45) for which you want to search vaccine availability', choices=["18", "45"])

    args = parser.parse_args()
    if(args.date is None or args.state is None or args.minAge is None):
        print("Error! Date, State and minAge are mandatory params!")
    elif(args.pincode):
        get_slots_by_pincode_and_date(args.pincode, args.date, args.minAge)
    elif(args.district):
        get_all_slots_for_a_district(args.state.title(), args.district, args.date, args.minAge)
    else:
        get_all_slots_for_a_state(args.state.title(), args.date, args.minAge)


if __name__ == '__main__':
    main()