import datetime
import csv


def calculate_schedule(routes, time, intervals):
    time_schedule = {}
    for route in routes:
        for stations in routes[route]:
            if stations not in time_schedule:
                time_schedule.update({stations: []})
    for route in routes:
        interval = intervals[route]
        flag = time[route][0]
        end = time[route][1]
        for stations in routes[route]:
            destanation = stations
        while flag <= end:
            train = flag
            for stations in routes[route]:
                destanation = stations
            for stations in routes[route]:
                train += routes[route][stations][0]
                time_schedule[stations].append({str(train): [route, destanation]})
            flag += interval
    for route in routes:
        interval = intervals[route]
        flag = time[route][0]
        end = time[route][1]
        for stations in reversed(routes[route]):
            destanation = stations
        while flag <= end:
            train = flag
            for stations in reversed(routes[route]):
                destanation = stations
            for stations in reversed(routes[route]):
                train += routes[route][stations][1]
                time_schedule[stations].append({str(train): [route, destanation]})
            flag += interval
    return time_schedule


def search_for_train(time_schedule, station, time):
    output = {}
    for stations in time_schedule:
        for schedule in time_schedule[stations]:
            deference = int(next(iter(schedule))) - time
            destination = str(list(schedule.values())[0][1])
            route = str(list(schedule.values())[0][0])
            if ((time <= int(next(iter(schedule)))) and (abs(deference) <= 10) and (station == stations) and (
                    destination != stations)):
                if (destination not in output) or (output[destination][1] > deference):
                    output.update({destination: [route, deference]})
    if len(output) == 0:
        print("No trains at this time!")
    else:
        final_output = {}
        for destinations in output:
            final_output.update({output.get(destinations)[1]: [output.get(destinations)[0], destinations]})
        for time in sorted(final_output):
            print(f'{final_output[time][0]} route,'
                  f' destination {final_output[time][1]}, {time} min')


def get_current_time():
    date_and_time = str(datetime.datetime.now())
    time = date_and_time.split(" ", 1)[1]
    hours = time.split(":")[0]
    minutes = time.split(":")[1]
    print(f"Current time: {hours}:{minutes}")
    return time


def convert_time(time):
    time = time.split(":")
    if (int(time[1]) > 59):
        print("The wrong time is founded.")
        exit()
    final_time = (int(time[0])*60) + int(time[1])
    return final_time


def get_station(time_schedule):
    station = input("Enter station: ").upper()
    if station == '':
        exit()
    elif (station not in time_schedule):
        print("No such station!")
        return get_station(time_schedule)
    else:
        return station


def load_base():
    try:
        routes = {}
        times = {}
        intervals = {}
        with open('routes.csv', 'rt') as f:
            data = csv.reader(f)
            next(data)
            for row in data:
                if len(row[0]) != 0:
                    routes.update({str(row[0]): {}})
                    times.update({str(row[0]): []})
                    intervals.update({str(row[0]): None})
                    start = convert_time(row[1])
                    finish = convert_time(row[2])
                    if (start > finish):
                        time = row[2].split(':')
                        finish = convert_time(f"{int(time[0]) + 24}:{time[1]}")
                    times[row[0]] = [start, finish]
                    intervals[row[0]] = int(row[3])
                    for i in range(4, len(row)):
                        if len(row[i]) != 0:
                            station = row[i].split(',')[0]
                            start = int(row[i].split(',')[1])
                            finish = int(row[i].split(',')[2])
                            routes[row[0]].update({station: [start, finish]})
            f.close()
        return intervals, routes, times
    except:
        print("Error on loading base! Make sure that .csv file is ok!")
        exit()

def analyse_time(time):
    try:
        time = time.split(':')
        if (int(time[1]) > 59):
            print("The wrong time is founded.")
            return get_time()
        suggested_time = (int(time[0]) * 60) + int(time[1])
        print(suggested_time)
        if (int(time[0]) < 10):
            start = 0
            for route in times:
                if (start == 0) or (times[route][0] < start):
                    start = times[route][0]
                # print(f'{times[route][1]} and {times[route][0]}')
            for route in times:
                if (times[route][1] > suggested_time) and (start > suggested_time):
                    return convert_time(f"{int(time[0]) + 24}:{time[1]}")
        return suggested_time
    except:
        print("Wrong time!")
        return get_time()

def get_time():
    time = input("Current time: ")
    # time = get_current_time()
    time = analyse_time(time)
    return time

def main():
    time_schedule = calculate_schedule(routes, times, intervals)
    station = get_station(time_schedule)
    time = get_time()
    search_for_train(time_schedule, station, time)


if __name__ == "__main__":
    intervals, routes, times = load_base()
    while True:
        main()
