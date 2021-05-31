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


def get_current_time() -> int:
    date_and_time = str(datetime.datetime.now())
    time = date_and_time.split(" ", 1)[1]
    hours = int(time.split(":")[0])
    minutes = int(time.split(":")[1])
    print(f"Current time: {hours}:{minutes}")
    from_midnight_minutes = hours * 60 + minutes
    return from_midnight_minutes


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
            data = csv.DictReader(f, delimiter=',')
            for lines in data:
                if len(lines['Route']) != 0:
                    routes.update({lines['Route']: {}})
                    times.update({lines['Route']: []})
                    intervals.update({lines['Route']: None})
            f.close()
        with open('routes.csv', 'rt') as f:
            data = csv.reader(f)
            next(data)
            for row in data:
                if len(row[0]) != 0:
                    start = convert_time(row[1])
                    finish = convert_time(row[2])
                    if (start > finish):
                        finish = (24 * 60) + finish
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


def main():
    time_schedule = calculate_schedule(routes, times, intervals)
    station = get_station(time_schedule)
    time = convert_time(input("Current time: "))
    # time = get_current_time()
    search_for_train(time_schedule, station, time)


if __name__ == "__main__":
    intervals, routes, times = load_base()
    while True:
        main()
