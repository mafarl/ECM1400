import csv
import os
from datetime import datetime, timedelta
import utils


def data_implementation() -> dict:
    """
    Unpacks the pollution data in data folder of the project
    
    Returns: 
        Dictionary: with three keys that are the names of the three files that contain data for each station, 
        the value of each pair is a list with 8760 dictionaries for each hour of each day.
    """
    # Value to return
    pollution_storage = {}

    list_of_pollution_data = []

    # Needed to specify the index of the list in which a day information is appended e.g., if it's 2021-01-01 then append to i = 0
    # Then once appended, increase i by 1
    i = 0

    # Get the currect working directory path
    current = os.getcwd()

    # Create a path to the extract the files from the 'data' folder
    directory = f'{current}/data/'

    # Iterate over each file in data directory
    # If the file extension is .csv then open the file and apppend the data into pollution_storage to be returned
    for file in os.listdir('data'):
        if file.endswith('.csv'):
            with open(f'{directory}/{file}', 'r') as f:
                csv_reader = csv.DictReader(f)
                list_of_pollution_data.append([])
                for row in csv_reader:
                    list_of_pollution_data[i].append(row)
            
            pollution_storage.update({str(file): list_of_pollution_data[i]})
            i += 1
        else:
            continue

    return pollution_storage


def daily_average(data, monitoring_station: str, pollutant: str) -> list:
    """
    Calculates average value for a specified pollutant and monitoring station in each day of the year.

    Returns:
        List: with 365 values each corresponding to the daily average for a particular pollutant and monitoring station.

    Keyword arguments:
    ------------------
    data -- dict
        Dictionary with implemented pollution data

    monitoring_station -- str
        Name of a monitoring station which data will be used

    pollutant -- str
        Name of the pollutant which daily average should be calculated
    """ 
    data = data_implementation()

    # Finding the pollution data of a desired monitoring station from the passed data variable
    station_data = []
    for station in data:
        if monitoring_station.lower() in station.lower():
            station_data = data[station]
    
    # Variable with the resultant values
    data_for_pollutant = []
    # Variables to get the date and time of the first day which will be used to check the date of each day in station_data
    current_date = station_data[0]["date"]
    current_time = station_data[0]["time"]
    # Variable to store the values of pollutions for a current_day
    temporary_variable_for_day = []

    # Iterate over each day in station_data
    for day in station_data:

        # Check if the day's date equals to the stored in current_day, so that we always compare with the same day
        if day["date"] == current_date:
            # If the day contains data - add this daat to a temporary variable for the day
            if day[pollutant] != 'No data':
                temporary_variable_for_day.append(day[pollutant])
            
            # Check if it's the last day in the station_data
            # If yes - calculate the average and the loop will stop itself since the day was the last in the list
            if station_data.index(day) == len(station_data)-1:
                if not temporary_variable_for_day:
                    data_for_pollutant.append('No data')
                else:
                    average = utils.meannvalue(temporary_variable_for_day)
                    data_for_pollutant.append(average)
        
        # If we are already on day where date is not the same as stored in current_date
        # The problem is that every time we will do this when the day's date is current_date + 1 AND time = 01:00:00
        # So, unless we add the pollutant value to the temporary storage here, we'll miss the day{date:x, time:01:00:00} every time
        else:
            # Check if the storage for hour variables for the day is empty
            # If it is, we don't need to calculate average since there was no data
            # So, we change date by 1 and again add the day{date:x, time:01:00:00} pollutant value into the storage unless it is 'No data'
            # Also, add 'No data' value to the daily average list (data_for_pollutant) to indicate that this day there was no data at all
            if not temporary_variable_for_day:
                temp_for_date_change = datetime.strptime(f'{current_date} {current_time}', "%Y-%m-%d %H:%M:%S")
                temp_for_date_change = temp_for_date_change + timedelta(days=1)
                current_date = temp_for_date_change.strftime("%Y-%m-%d")
                data_for_pollutant.append('No data')
                if day[pollutant] != 'No data':
                    temporary_variable_for_day.append(day[pollutant])
            # If the storage for hour variables for the day is NOT empty
            else:
                # Calculate average in temporary_variable_for_day list
                average = utils.meannvalue(temporary_variable_for_day)
                data_for_pollutant.append(average)

                # Change the current_date by 1 day and clear temporary_variable_for_day
                temp_for_date_change = datetime.strptime(f'{current_date} {current_time}', "%Y-%m-%d %H:%M:%S")
                temp_for_date_change = temp_for_date_change + timedelta(days=1)
                current_date = temp_for_date_change.strftime("%Y-%m-%d")
                temporary_variable_for_day.clear()
                # Add the day{date:x, time:01:00:00} pollutant value into the storage unless it is 'No data'
                if day[pollutant] != 'No data':
                    temporary_variable_for_day.append(day[pollutant])
    
    return data_for_pollutant
            

def daily_median(data, monitoring_station:str, pollutant:str) -> list:
    """
    Calculates median value for a specified pollutant and monitoring station in each day of the year.
    
    Returns:
        List: with 365 values each corresponding to the daily median for a particular pollutant and monitoring station.

    Keyword arguments:
    ------------------
    data -- dict
        Dictionary with implemented pollution data

    monitoring_station -- str
        Name of a monitoring station which data will be used

    pollutant -- str
        Name of the pollutant which daily average should be calculated
    """
    data = data_implementation()

    # Finding the pollution data of a desired monitoring station from the passed data variable
    station_data = []
    for station in data:
        if monitoring_station.lower() in station.lower():
            station_data = data[station]
    
    # Variable with the resultant values
    data_daily_median = []
    # Variables to get the date and time of the first day which will be used to check the date of each day in station_data
    current_date = station_data[0]["date"]
    current_time = station_data[0]["time"]
    # Variable to store the values of pollutions for a current_day
    temporary_variable_for_day = []

    # Iterate over each day in station_data
    for day in station_data:

        # Check if the day's date equals to the stored in current_day, so that we always compare with the same day
        if day["date"] == current_date:

            # If the day contains data - add this daat to a temporary variable for the day
            if day[pollutant] != 'No data':
                temporary_variable_for_day.append(day[pollutant])
            
            # Check if it's the last day in the station_data
            # If yes - calculate the median and the loop will stop itself since the day was the last in the list
            if station_data.index(day) == len(station_data)-1:

                # Create a list of floats from the temporary_variable_for_day which stores the daily pollutant values
                temporary_variable_for_day = list(map(float, temporary_variable_for_day))
                # Sort the list
                temporary_variable_for_day.sort()
                # Determine the number of pollutant values for the current_day
                length = utils.length_of_list(temporary_variable_for_day)

                # The way to calculate median if the length is odd
                if length % 2 == 1:
                    data_daily_median.append(temporary_variable_for_day[int(length/2)])
                    # Clear the temporary_variable_for_day to use for the next day
                    temporary_variable_for_day.clear()
                
                # The way to calculate median if the length is even and more than 0
                elif length != 0:
                    values_in_the_middle = []
                    values_in_the_middle.append(temporary_variable_for_day[int(length/2)])
                    values_in_the_middle.append(temporary_variable_for_day[int((length/2) - 1)])
                    data_daily_median.append(utils.meannvalue(values_in_the_middle))
                    # Clear the temporary_variable_for_day to use for the next day
                    temporary_variable_for_day.clear()
                
                # Else if the temporary_variable_for_day is empty i.e., there's no data for that day - append 'No data' into the data_daily_median to be returned
                else:
                    data_daily_median.append('No data')

        # If we are already on day where date is not the same as stored in current_date
        # The problem is that every time we will do this when the day's date is current_date + 1 AND time = 01:00:00
        # So, unless we add the pollutant value to the temporary storage here, we'll miss the day{date:x, time:01:00:00} every time
        else:
            # Check if the storage for hour variables for the day is empty
            # If it is, we don't need to calculate median since there was no data      
            if not temporary_variable_for_day:
                # Change the date by 1 day
                temp_for_date_change = datetime.strptime(f'{current_date} {current_time}', "%Y-%m-%d %H:%M:%S")
                temp_for_date_change = temp_for_date_change + timedelta(days=1)
                current_date = temp_for_date_change.strftime("%Y-%m-%d")
                # Also, add 'No data' value to the data_daily_median list (data_for_pollutant) to indicate that this day there was no data at all
                data_daily_median.append('No data')
                # Add the day{date:x, time:01:00:00} pollutant value into the storage unless it is 'No data'
                if day[pollutant] != 'No data':
                    temporary_variable_for_day.append(day[pollutant])
            
            # If the storage for hour variables for the day is NOT empty
            else:
                # Create a list of floats from the temporary_variable_for_day which stores the daily pollutant values
                temporary_variable_for_day = list(map(float, temporary_variable_for_day))
                # Sort the list
                temporary_variable_for_day.sort()
                # Determine the number of pollutant values for the current_day
                length = utils.length_of_list(temporary_variable_for_day)

                # The way to calculate median if the length is odd
                if length % 2 == 1:
                    data_daily_median.append(temporary_variable_for_day[int(length/2)])
                
                # The way to calculate median if the length is even
                else:
                    values_in_the_middle = []
                    values_in_the_middle.append(temporary_variable_for_day[int(length/2)])
                    values_in_the_middle.append(temporary_variable_for_day[int((length/2) - 1)])
                    data_daily_median.append(utils.meannvalue(values_in_the_middle))

                 # Change the current_date by 1 day and clear temporary_variable_for_day
                temp_for_date_change = datetime.strptime(f'{current_date} {current_time}', "%Y-%m-%d %H:%M:%S")
                temp_for_date_change = temp_for_date_change + timedelta(days=1)
                current_date = temp_for_date_change.strftime("%Y-%m-%d")
                # Clear the temporary_variable_for_day to use for the next day
                temporary_variable_for_day.clear()

                # Add the day{date:x, time:01:00:00} pollutant value into the storage unless it is 'No data'
                if day[pollutant] != 'No data':
                    temporary_variable_for_day.append(day[pollutant])
        
    return data_daily_median


def hourly_average(data, monitoring_station:str, pollutant:str) -> list:
    """
    Calculates average pollution value for each hour of all days in the year for a specified monitoring station and pollutant.
    
    Returns:
        List: with 24 values each corresponding to the hourly average for a particular pollutant and monitoring station.

    Keyword arguments:
    ------------------
    data -- dict
        Dictionary with implemented pollution data

    monitoring_station -- str
        Name of a monitoring station which data will be used

    pollutant -- str
        Name of the pollutant which daily average should be calculated
    """
    data = data_implementation()

    # Finding the pollution data of a desired monitoring station from the passed data variable
    station_data = []
    for station in data:
        if monitoring_station.lower() in station.lower():
            station_data = data[station]

    # Dictionary where key is an hour and its value is a list of the pollution values during each day at this particular hour
    hourly_pollutant_data_dict = {}
    
    # Iterate over each day in station_data
    for day in station_data:
        
        # Check if the current hour key is already in the dictionary
        # If not - add a new key-value pair where value is an empty list
        if day["time"] not in hourly_pollutant_data_dict:
            hourly_pollutant_data_dict[day["time"]] = []

        # If the day contains data - add this data to the list of values in the dictionary where key is the hour of the currect day 
        if day[pollutant] != 'No data':
            hourly_pollutant_data_dict[day["time"]].append(day[pollutant])

    # Create the list to be returned
    hourly_pollutant_data = []
    # Iterate over each key-value pair and calculate the mean of the pollution values for each hour/key and append into hourly_pollutant_data
    for hour in hourly_pollutant_data_dict:
        # If there are no values for any of the keys i.e., the list of values is empty - add 'No data' to the list to be returned
        if len(hourly_pollutant_data_dict[hour]) == 0:
            hourly_pollutant_data.append('No data')
        # If there are values in the list for the current key - calculate their mean and add to the list to be returned
        else:
            average = utils.meannvalue(hourly_pollutant_data_dict[hour])
            hourly_pollutant_data.append(average)
        
    return hourly_pollutant_data


def monthly_average(data, monitoring_station, pollutant):
    """
    Calculates monthly average pollution value for each month in the year for a specified monitoring station and pollutant.
    
    Returns:
        List: with 12 values each corresponding to the monthly average for a particular pollutant and monitoring station.

    Keyword arguments:
    ------------------
    data -- dict
        Dictionary with implemented pollution data

    monitoring_station -- str
        Name of a monitoring station which data will be used

    pollutant -- str
        Name of the pollutant which daily average should be calculated
    """
    data = data_implementation()

    # Finding the pollution data of a desired monitoring station from the passed data variable
    station_data = []
    for station in data:
        if monitoring_station.lower() in station.lower():
            station_data = data[station]

    # Dictionary where key is a month number and its value is a list of the pollution values during each day of this month
    monthly_pollutant_data_dict = {}

    # Iterate over each day in station_data
    for day in station_data:

        # Get the number of the month of the current day
        day_month = datetime.strptime(day["date"], "%Y-%m-%d").month
        # Check if the current month key is already in the dictionary
        # If not - add a new key-value pair where value is an empty list
        if day_month not in monthly_pollutant_data_dict:
            monthly_pollutant_data_dict[day_month] = []

        # If the day contains data - add this data to the list of values in the dictionary where key is the month of the currect day 
        if day[pollutant] != 'No data':
            monthly_pollutant_data_dict[day_month].append(day[pollutant])

    # Create the list to be returned
    monthly_pollutant_data = []
    # Iterate over each key-value pair and calculate the mean of the pollution values for each month/key and append into monthly_pollutant_data
    for month in monthly_pollutant_data_dict:
        # If there are no values for any of the keys i.e., the list of values is empty - add 'No data' to the list to be returned
        if len(monthly_pollutant_data_dict[month]) == 0:
            monthly_pollutant_data.append('No data')
        # If there are values in the list for the current key - calculate their mean and add to the list to be returned
        else:
            average = utils.meannvalue(monthly_pollutant_data_dict[month])
            monthly_pollutant_data.append(average)

    return monthly_pollutant_data


def peak_hour_date(data, date:str, monitoring_station:str,pollutant:str):
    """
    Calculates peak pollution value for each day in the year for a specified monitoring station and pollutant.
    
    Returns:
        Tuple: with the hour of the day with the highest pollution level and its corresponding value.

    Keyword arguments:
    ------------------
    data -- dict
        Dictionary with implemented pollution data

    date -- str
        Date for which the highest pollution level to be returned

    monitoring_station -- str
        Name of a monitoring station which data will be used

    pollutant -- str
        Name of the pollutant which daily average should be calculated
    """
    data = data_implementation()

    # Finding the pollution data of a desired monitoring station from the passed data variable
    station_data = []
    for station in data:
        if monitoring_station.lower() in station.lower():
            station_data = data[station]

    # Variables to get the date and time of the first day which will be used to check the date of each day in station_data
    current_date = station_data[0]["date"]
    current_time = station_data[0]["time"]

    # Dictionary to store keys - dates, and values - list (if more than one maximum) or tuple (if there's one maximum value in a day)
    data_for_all_days = {}
    # Variable to store values of pollution at different hours for each day
    temp_day_storage = []

    # Iterate over each day in station_data
    for day in station_data:

        # Check if the day's date equals to the stored in current_day, so that we always compare with the same day
        if day["date"] == current_date:

            # If the day contains data - add this daat to a temporary variable for the day
            if day[pollutant] != 'No data':
                # Append a tuple that contains the value of pollution and its hour
                temp_day_storage.append((day[pollutant], day["time"]))

            # Check if it's the last day in the station_data
            if station_data.index(day) == len(station_data)-1:
                # If the temporary storage for that day is empty - append tuple with 'No data' variable to the key that corresponds to that day
                if not temp_day_storage:
                    data_for_all_days[current_date] = ('No data')
                # If the temporary storage is not empty
                else:
                    storage_to_calculate_max = []
                    # Add pollution values of each hour in the temporary storage variable
                    for hour in temp_day_storage:
                        storage_to_calculate_max.append(hour[0])

                    # Calculate maximum value in the list with the pollution values
                    # Returns a list of values/or with a single value where value(-s) correspond to the index of the maximums in the list
                    maximum = utils.maxvalue(storage_to_calculate_max)

                    # Add value to the key-values pair where key is the current_date
                    data_for_all_days[current_date] = temp_day_storage[maximum]

        # If we are already on day where date is not the same as stored in current_date
        else:
            # Check if the storage for hour variables for the day is empty
            if not temp_day_storage:
                # Append a tuple with 'No data' variable
                data_for_all_days[current_date] = ('No data')
                # Change the current_date by 1 day and clear temporary_variable_for_day
                temp_for_date_change = datetime.strptime(f'{current_date} {current_time}', "%Y-%m-%d %H:%M:%S")
                temp_for_date_change = temp_for_date_change + timedelta(days=1)
                current_date = temp_for_date_change.strftime("%Y-%m-%d")
                # Add the day{date:x, time:01:00:00} pollutant value and the corresponding hour (01:00:00) into the storage unless it is 'No data'
                if day[pollutant] != 'No data':
                        temp_day_storage.append((day[pollutant], day["time"]))
            
            # If the temp_day_storage is NOT empty
            else:
                storage_to_calculate_max = []
                # Add pollution values of each hour in the temporary storage variable
                for hour in temp_day_storage:
                    storage_to_calculate_max.append(hour[0])

                # Calculate maximum value in the list with the pollution values
                # Returns a list of values/or with a single value where value(-s) correspond to the index of the maximums in the list
                maximum = utils.maxvalue(storage_to_calculate_max)

                # Add maximum to the key-values pair where key is the current_date
                data_for_all_days[current_date] = temp_day_storage[maximum]

                # Clear temp_day_storage to use for the next day
                temp_day_storage.clear()
                # Change the current_date by 1 day
                temp_for_date_change = datetime.strptime(f'{current_date} {current_time}', "%Y-%m-%d %H:%M:%S")
                temp_for_date_change = temp_for_date_change + timedelta(days=1)
                current_date = temp_for_date_change.strftime("%Y-%m-%d")

                # Add the day{date:x, time:01:00:00} pollutant value and the corresponding hour (01:00:00) into the storage unless it is 'No data'
                if day[pollutant] != 'No data':
                        temp_day_storage.append((day[pollutant], day["time"]))

    return data_for_all_days[date]


def count_missing_data(data,  monitoring_station:str,pollutant:str) -> int:
    """
    Calculates how many hours miss data in a particular monitoring station and pollutant data.

    Returns:
        Int: the number of 'No data' entries are there in the data for a given monitoring station and pollutant.

    Keyword arguments:
    ------------------
    data -- dict
        Dictionary with implemented pollution data
    
    monitoring_station -- str
        Name of a monitoring station which data will be used

    pollutant -- str
        Name of the pollutant which daily average should be calculated
    """
    data = data_implementation()

    # Finding the pollution data of a desired monitoring station from the passed data variable
    station_data = []
    for station in data:
        if monitoring_station.lower() in station.lower():
            station_data = data[station]

    # Append all the values of pollution levels for a specified pollutant from station_data
    pollutant_data = []
    for date in station_data: 
        pollutant_data.append(date[pollutant])

    # Using the written function which calculates the number a specified value is encountered, calculate how many time 'No data' is in the pollutant_data list
    counter_of_no_data_entries = utils.countvalue(pollutant_data, 'No data')

    return counter_of_no_data_entries


def fill_missing_data(data, new_value,  monitoring_station:str,pollutant:str) -> list:
    """
    Creates a copy of the data of a specified monitoring station but changing 'No data' values by a specified new value.

    Returns:
        List: a copy of the data with the missing values 'No data' replaced by the value in the parameter new value for a given monitoring station and pollutant.

    Keyword arguments:
    ------------------
    data -- dict
        Dictionary with implemented pollution data
    
    new_value -- Any data type
        The value to replace 'No data' with
    
    monitoring_station -- str
        Name of a monitoring station which data will be used

    pollutant -- str
        Name of the pollutant which daily average should be calculated
    """
    data = data_implementation()
       
    # Finding the pollution data of a desired monitoring station from the passed data variable
    station_data = []
    for station in data:
        if monitoring_station.lower() in station.lower():
            station_data = data[station]

    # Iterate over each day
    for day in station_data:

        # If 'No data' is encountered - replace it with new value
        if day[pollutant] == 'No data':
            day[pollutant] = new_value
    
    return station_data