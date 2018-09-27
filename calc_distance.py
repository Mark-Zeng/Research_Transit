import math
import csv
R = 6371

def distance(lat1, lon1, lat2, lon2):
    diff_lat = deg2rad(abs(lat1 - lat2))
    diff_lon = deg2rad(abs(lon1 - lon2))
    herver = math.sin(diff_lat / 2) ** 2 + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(diff_lon / 2) * math.sin(diff_lon / 2)
    c = 2 * math.atan2(math.sqrt(herver), math.sqrt(1-herver))
    d = R * c
    return d




def deg2rad(num):
    return num * math.pi / 180


class Error(Exception):
    pass



def main():
    # la1 = 40.645845  #stop_id 303345 initial stop
    # lo1 = -73.902462
    # la2 = 40.637137 #stop_id 303351
    # lo2 = -73.893562
    # la3 = 40.635176 #stop_id 303352
    # lo3 = -73.891378
    # la4 = 40.631428 #stop_id 306405 last stop
    # lo4 = -73.887285

    # print("The distance between the first stop and the last stop:\n{:.3f} KM".format(distance(la1, lo1, la4, lo4)))
    # print("The distance between two consecutive stops:\n{:.3f} KM".format(distance(la2, lo2, la3, lo3)))
    with open("mta_bk/stops.csv") as file:
        reader = csv.DictReader(file)
        stopid_map= {}
        for row in reader:
            to_add = (float(row["stop_lat"]), float(row["stop_lon"]))
            stopid_map[row["stop_id"]] = to_add
    stopid_map_copy = stopid_map.copy()
    print("length of the stops:", len(stopid_map_copy))
    alpha = 0.1 #assume if distance is within 200m then they belong to the same node
    closures = [] #a list to hold clossure ids
    replace = {} #match a stop_id to the one that it will eventually combined to

    while stopid_map_copy != {}:
        k, v = stopid_map_copy.popitem()
        closures.append(k)
        copy_map = stopid_map_copy.copy()
        for k1, v1 in copy_map.items():
            if distance(*v, *v1) <= alpha:
                replace[k1] = k
                del stopid_map_copy[k1]
    # for k, v in replace.items():
    #     print("replace {} with {}".format(k, v))
    print("length of the closures:", len(closures))
    # print(closures)


    with open('stops2.txt', 'w') as csvfile:
        with open('mta_bk/stops.csv') as infile:
            reader = csv.DictReader(infile)
            fieldnames = ['stop_id', 'stop_name', 'stop_desc', 'stop_lat', 'stop_lon', 'zone_id', 'stop_url', 'location_type', 'parent_station']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in reader:
                if row['stop_id'] in closures:
                    writer.writerow(row)


    with open('stop_times2.txt', 'w') as csvfile:
        with open('mta_bk/stop_times.txt') as infile:
            reader = csv.DictReader(infile)
            fieldnames = ['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence', 'pickup_type', 'drop_off_type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                if row['stop_id'] not in closures:
                    row['stop_id'] = replace.get(row['stop_id'], -1)
                    if row['stop_id'] == -1:
                        raise Error("Did not find replacement")
                writer.writerow(row)





if __name__ == "__main__":
    main()