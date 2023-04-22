import requests
import datetime
import utils
import pandas as pd
import json


def get_live_data_from_api(site_code='MY1',species_code='NO',start_date=None,end_date=None):
    """
    Return data from the LondonAir API using its AirQuality API. 
    
    *** This function is provided as an example of how to retrieve data from the API. ***
    It requires the `requests` library which needs to be installed. 
    In order to use this function you first have to install the `requests` library.
    This code is provided as-is. 
    """
    import requests
    import datetime
    start_date = datetime.date.today() if start_date is None else start_date
    end_date = start_date + datetime.timedelta(days=1) if end_date is None else end_date
    
    
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
   
    url = endpoint.format(
        site_code = site_code,
        species_code = species_code,
        start_date = start_date,
        end_date = end_date
    )
    
    res = requests.get(url)
    return res.json()


def find_station_code(StationName='Harlington'):
    """
    Function finds the station code for a specified pollution station.
    
    @param StationName: Name of the monitoring station which code to find
    @return: str if incorrect station code or str of station code
    """

    url = "https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName=London/Json"

    result = requests.get(url)
    result = result.json()

    # Iterate over each site and return its code once equals to StationName 
    for i in range(len(result['Sites']['Site'])):
        if StationName in result['Sites']['Site'][i]['@SiteName']:

            return result['Sites']['Site'][i]['@SiteCode']
    
    # Otherwise return 'No such station'
    return f"No such station."


def get_all_available_pollutant_names():
    """
    Function prints out all the commonly monitored pollutants names which data is available along with their codes.

    @return: 0  
    """

    url = "https://api.erg.ic.ac.uk/AirQuality/Information/Species/Json"
    
    result = requests.get(url)
    result = result.json()

    # Storage for (species name, species code)
    list_pollutants = []

    # Iterate over each species dictionary
    for pollutant in result['AirQualitySpecies']['Species']:
        list_pollutants.append((pollutant['@SpeciesName'],pollutant['@SpeciesCode']))

    # Coloured output
    output1 = f"{utils.colors.bg.orange}{utils.colors.bold}There are {len(list_pollutants)} commonly monitored pollutants available to analyse:{utils.colors.reset}"
    dashes = f"{'-'*(len(output1)-14)}"
    print(output1)
    print(dashes)
    for pollutant in list_pollutants:
        print(f"Code: {utils.colors.fg.yellow}{utils.colors.bold}{pollutant[1]} {utils.colors.reset}({pollutant[0]})\n")

    # Returns 0 if everything is correct
    return 0


def get_particular_pollutant_health_info(species_code='NO2') -> str:
    """
    Function returns the health information about an enquired pollutant

    @param species_code: Code of a pollutant which information to return
    @return: f-string containing health info
    """

    endpoint = 'https://api.erg.ic.ac.uk/AirQuality/Information/Species/SpeciesCode={SpeciesCode}/Json'

    url = endpoint.format(
        SpeciesCode = species_code
    )

    result = requests.get(url)
    result = result.json()
    
    # Try to iterate over each species to find the corresponding one
    try:
        result['AirQualitySpecies']['Species']['@HealthEffect']
        return f"{utils.colors.bold}Threats of {species_code}:{utils.colors.reset}\n"\
           f"-> {utils.colors.fg.pink}{result['AirQualitySpecies']['Species']['@HealthEffect']}{utils.colors.reset}"
    # Return f-string stating that the species code was wrong if the error is returned
    except:
        return f"You have entered a wrong species code"

    
def get_daily_for_particular_site(site_code='MY1', date=datetime.date.today()):
    """
    Function prints the day's Air Quality Index for all available pollutants for a specified day and station

    @param site_code: Code of the monitoring station (MY1 if input incorrect)
    @param date: Date which data to print
    @return: 0
    """  
    
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Daily/MonitoringIndex/SiteCode={site_code}/Date={date}/Json"

    url = endpoint.format(
        site_code = site_code,
        date = date
    )

    # Try to request the json data with the user input
    try:
        result = requests.get(url)
        result = result.json()

        pollutants_airqualityindex = []
        for pollutant in result['DailyAirQualityIndex']['LocalAuthority']['Site']['Species']:
            pollutants_airqualityindex.append((pollutant['@SpeciesCode'], pollutant['@AirQualityIndex'], pollutant['@AirQualityBand']))
    # If the user input is incorrect, use default values
    except:
        # Check the user dates are correct
        try:
            one = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            two = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        # Otherwise use default
        except:        
            start_date = datetime.date.today()
            end_date = start_date + datetime.timedelta(days=1)
            pass
        
        print(f'The input was incorrect. However, we can show you data for the default station (MY1):')
        site_code = 'MY1'
        endpoint = "https://api.erg.ic.ac.uk/AirQuality/Daily/MonitoringIndex/SiteCode={site_code}/Date={date}/Json"

        url = endpoint.format(
            site_code = site_code,
            date = date
        )

        result = requests.get(url)
        result = result.json()

        pollutants_airqualityindex = []
        for pollutant in result['DailyAirQualityIndex']['LocalAuthority']['Site']['Species']:
            pollutants_airqualityindex.append((pollutant['@SpeciesCode'], pollutant['@AirQualityIndex'], pollutant['@AirQualityBand']))

        pass
    
    # Coloured output in a 'table' format
    print('-'*35)
    print("|{:<15}|{:<15}|".format('Pollutant Code', 'Air Quality Index'))
    for pollutant in pollutants_airqualityindex:
        print('-'*35)
        output = [f"{utils.colors.fg.yellow}{utils.colors.bold}{pollutant[0]}{utils.colors.reset}", 
                  f"{utils.colors.fg.yellow}{utils.colors.bold}{pollutant[1]}{utils.colors.reset} ({pollutant[2]})"]
        print("|{:<29}|{:<31}|".format(output[0], output[1]))
    print('-'*35)

    return 0


def hourly_sitecode_dynamic(site_code='BX2', pollutant='all') -> list:
    """
    Function finds the last hour's pollutants with their Air Quality Index and Air Quality Band"

    @param site_code: Code of the monitoring station (BX2 if input incorrect)
    @param pollutant: Pollutant code which info to return
    @return: list of specified pollutant(-s) and their information
    """

    endpoint ='https://api.erg.ic.ac.uk/AirQuality/Hourly/MonitoringIndex/SiteCode={SiteCode}/Json'

    # Try to request the json format information with the user input
    try:
        url = endpoint.format(
        SiteCode = site_code
        )
        result = requests.get(url)
        result = result.json()
        if result['HourlyAirQualityIndex']['LocalAuthority']['Site']['species']['@SpeciesCode']:
            pass
    # If the user input is incorrect - use default parameters
    except: 
        print(f"The input was incorrect (or the station's data is unavailable). However, we can show you data for the default station (BX2):")
        site_code = 'BX2'
        url = endpoint.format(
        SiteCode = site_code
        )
        result = requests.get(url)
        result = result.json()

    # List to store (species code, air quality index, air quality band)
    pollutant_data = []

    for species in result['HourlyAirQualityIndex']['LocalAuthority']['Site']['species']:
        pollutant_data.append((species['@SpeciesCode'], species['@AirQualityIndex'], species['@AirQualityBand']))

    # Return the list if all pollutants info is requested
    if pollutant == 'all':
        return pollutant_data

    # If a specific pollutant is requested, return its results
    else: 
        # Check this pollutant is present in the list
        present = False
        for species in pollutant_data:
            if species[0] == pollutant:
                present = True
                position = pollutant_data.index(species)
        
        if not present:
            return f"The data for this species is not available for the last hour"
        else:
            return pollutant_data[position]


def get_live_data_for_station_species(site_code='MY1',species_code='NO2',start_date=None,end_date=None) -> tuple:
    """
    Function finds all hourly data for the specified day(-s).
    Function calculates average and peak hour (with value).

    @param site_code: Code of the monitoring station (MY1 if input incorrect)
    @param species_code: Pollutant code which info to return
    @param start_date: Get data from
    @param end_date: Get data until
    @return: list of specified pollutant(-s) and their information
    """

    start_date = datetime.date.today() if start_date is None else start_date
    end_date = start_date + datetime.timedelta(days=1) if end_date is None else end_date   
        
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
    
    # Try to request json data and check the user's input is correct
    try:
        url = endpoint.format(
            site_code = site_code,
            species_code = species_code,
            start_date = start_date,
            end_date = end_date
        )

        res = requests.get(url)
        res = res.json()

        for datum in res['RawAQData']['Data'][0]:
            pass
    
    # If the user input is incorrect - use default parameters
    except:
        print(f'The input was incorrect. However, we can show you data for the default station and species (MY1, NO2): ')
        # Check user's dates are correct
        try:
            one = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            two = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        # Otherwise - use default
        except:        
            start_date = datetime.date.today()
            end_date = start_date + datetime.timedelta(days=1)
            pass
        
        site_code = 'MY1'
        species_code = 'NO2'

        url = endpoint.format(
            site_code = site_code,
            species_code = species_code,
            start_date = start_date,
            end_date = end_date
        )

        res = requests.get(url)
        res = res.json()
        pass
    
    # Storage for columns in the output
    data = {'|': ['|'],
            'Date': [],
            'Hour': [],
            'Value': []}
    
    # Iterate over each hour's data
    for datum in res['RawAQData']['Data']:
        date_time = datum['@MeasurementDateGMT'].split(" ")
        data['Date'].append(date_time[0])
        data['Hour'].append(date_time[1])
        # If no data - append 'No data'
        if not datum['@Value']:
            data['Value'].append('No data')
        # Otherwise append the value
        else:
            data['Value'].append(datum['@Value'])

    # Create pandas DataFrame
    df = pd.DataFrame(data, index = list(" "*len(res['RawAQData']['Data'])), columns=['|', 'Date', '|', 'Hour', '|', 'Value', '|'])
    df_output = f"   +{'-'*36}+\n{df}\n   +{'-'*36}+"

    # Calculate average
    average = []
    for val in data['Value']:
        if val != 'No data':
            average.append(val) 

    average = utils.meannvalue(average)

    
    # Calculate peak hour (maximum)
    peak_hour_value = data['Value'][utils.maxvalue([val for val in data['Value'] if val != 'No data'])]
    peak_hour_index = data['Value'].index(peak_hour_value)
    peak_hour_hour = data['Hour'][peak_hour_index]
    peak_hour = (peak_hour_value, peak_hour_hour)

    return df_output, average, peak_hour
    

def peak_workday(site_code='BX2',start_date=None,end_date=None) -> dict:
    """
    Function finds the peak polluted work day at peak hours for all available pollutants for a specified period of time

    @param site_code: Code of the monitoring station (BX2 if input incorrect)
    @param start_date: Get data from
    @param end_date: Get data until
    @return: dictionary of the specified stations' pollutants and their peak workdays
    """

    start_date = (datetime.date.today() - datetime.timedelta(days=14)) if start_date is None else start_date
    end_date = datetime.date.today() + datetime.timedelta(days=1) if end_date is None else end_date

    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/Site/SiteCode={site_code}/StartDate={start_date}/EndDate={end_date}/Json"

    # Try to request json data and check the user's input is correct
    try: 
        url = endpoint.format(    
            site_code = site_code,
            start_date = start_date,
            end_date = end_date
        )
        
        res = requests.get(url)
        res = res.json()

        res['AirQualityData']['Data'][0]['@SpeciesCode']

    # If user input incorrect - use default parameters
    except: 
        print(f'The input was incorrect. However, we can show you data for the default station (BX2, last 14 days):')

        site_code = 'BX2'
        start_date = (datetime.date.today() - datetime.timedelta(days=7))
        end_date = datetime.date.today() + datetime.timedelta(days=1)

        url = endpoint.format(    
            site_code = site_code,
            start_date = start_date,
            end_date = end_date
        )
        
        res = requests.get(url)
        res = res.json()
        pass

    # Storage for species and their peak days
    list_of_all_species = {}

    # Storage for peaks workdays, that will be added to each species
    week_days_total = {0: 0,
                1: 0,
                2: 0,
                3: 0,
                4: 0}
    # Temporary storage to calculate the maximum workday value
    week_days_temp = {0: [],
                1: [],
                2: [],
                3: [],
                4: []}
    # Previous species name needed to monitor when the species is changed
    previous_species = res['AirQualityData']['Data'][0]['@SpeciesCode']

    # Check the date format is correct
    try:
        end_date = datetime.datetime.strptime(end_date, '%d %b %Y')
    except:
        pass
    end_dat = datetime.datetime.strftime(end_date, '%Y-%m-%d')
    end_dat = end_dat.split('-')
    end_dat = list(map(int, end_dat))
    end_dat = datetime.datetime(end_dat[0], end_dat[1], end_dat[2])

    # Iterate over each species hourly data
    for data in res['AirQualityData']['Data']:

        species = data['@SpeciesCode']
        # Add species key to the storage dictionary
        if species not in list_of_all_species.keys():
            list_of_all_species[species] = {None}
        # Get date of the current data
        date = data['@MeasurementDateGMT'][:11].split('-')
        date = list(map(int, date))
        date = datetime.datetime(date[0], date[1], date[2])
        # Get current week day
        week_day = date.weekday()
        # Get current time
        time = data['@MeasurementDateGMT'][11:].split(':')
        time = list(map(int, time))

        # Need to check it's not the last day of the last species in data      
        if species == previous_species and data != res['AirQualityData']['Data'][-1]:

            previous_species = species
            # Check if its the work day and the peak hour (07:00-09:00, 16:00-19:00)
            if week_day != 5 and week_day != 6 and (7 <= time[0] <= 9) or week_day != 5 and week_day != 6 and (16 <= time[0] <= 19):

                if data['@Value'] != '':
                    week_days_temp[week_day].append(data['@Value'])
            # If it's Sunday and not the last data - calculate averages for the week and add the date of the peak value to the week_days_total storage
            elif week_day == 6 and time[0] == 0:
                
                averages = {0: 0,
                                1: 0,
                                2: 0,
                                3: 0,
                                4: 0}

                for day,values in week_days_temp.items():
                    if not values:
                        averages[day] = -1
                    else:
                        average = utils.meannvalue([val for val in values])
                        averages[day] = average
                        week_days_temp[day].clear() 

                max_day_index = utils.maxvalue([val for val in averages.values()])

                if averages[max_day_index] == -1:
                    continue
                else:
                    week_days_total[max_day_index] += 1

        # In the case of the last data, calculate the averages, peak day and add to the week_day_total storage
        else:
            averages = {0: 0,
                        1: 0,
                        2: 0,
                        3: 0,
                        4: 0}

            for day,values in week_days_temp.items():
                if not values:
                    averages[day] = -1
                else:
                     average = utils.meannvalue([val for val in values if val != 'No data' or val != None])
                     week_days_temp[day].clear()
                     averages[day] = average

            max_day_index = utils.maxvalue([val for val in averages.values()])

            if averages[max_day_index] != -1:
                week_days_total[max_day_index] += 1
            
            list_of_all_species[previous_species] = week_days_total

            week_days_total = {0: 0,
                1: 0,
                2: 0,
                3: 0,
                4: 0}

            week_days_temp = {0: [],
                1: [],
                2: [],
                3: [],
                4: []}

            previous_species = species

    # Storage for peaks (species, list of peak work days if several days have the same number of peaks in the data)
    peaks = {}

    calendar = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    # Iterate over each species and the number of the week day
    for pollutant, days in list_of_all_species.items():

        check = False
        if days != {None}:
            for day in days:
                if days[day] != 0:
                    check = True
        # If there is no data - append 'No data'
        if days == {None} or days == 'No data' or not check:
            peaks[pollutant] = 'No data'
        # Otherwise calculate maximum between the values for each work day and add a correponsing day with a maximum number of peaks
        else:
            temp_days = [days[key] for key in days]
            
            max_day = utils.maxvalue([val for val in temp_days if val != 'No data' and val != None and val != ''])

            peaks[pollutant] = [calendar[val] for val in days if days[val] == days[max_day]]
    
    
    return peaks