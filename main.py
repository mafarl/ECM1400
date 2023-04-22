import utils
import reporting
import intelligence
import monitoring
import datetime
import os


def main_menu():
    """
    Function executed upon the initialisation of the program, showing the main menu of the program.

    Allows the user to navigate through the different options.

    @param none
    @return none
    """

    print(f"""\n{utils.colors.fg.purple}{utils.colors.bg.lightgrey}{utils.colors.bold}Welcome to the AQUA system!{utils.colors.reset}
{utils.colors.fg.purple}{utils.colors.bold}AQUA platform  is an air pollution data analytics solution.
AQUA users are policy-makers and public servants responsible for monitoring the pollution levels in different areas of the country.{utils.colors.reset}""")

    options = ["R", "I", "M", "A", "Q"]
    descriptions = ["Access the PR module", "Access the MI module", "Access the RM module", f"Access the {utils.colors.italic}About text{utils.colors.reset}", "Quit the application"]
    print(f"+{'-'*37}+")
    print("|{:<15}|{:<21}|".format('Key', 'Description'))
    print(f"+{'-'*37}+")
    for index in range(len(options)):
        output1 = f"{utils.colors.fg.yellow}{utils.colors.bold}{options[index]}{utils.colors.reset}"
        output2 = f"{utils.colors.fg.green}{descriptions[index]}{utils.colors.reset}"
        print("|{:<29}|{:<30}|".format(output1, output2))
        print(f"+{'-'*37}+")

    chosen_option = input(f"\n{utils.colors.underline}Please enter the module you are interested to explore:{utils.colors.reset} ")
    temp = False
    while not temp:
        if chosen_option.upper() in options:
            temp = True
        else:
            chosen_option = input("\nSorry, you have entered a non-existing option. Try again: ")
            
    if chosen_option.upper() == "R":
        reporting_menu()
    elif chosen_option.upper() == "I":
        intelligence_menu()
    elif chosen_option.upper() == "M":
        monitoring_menu()
    elif chosen_option.upper() == "A":
        about()
    else:
        quit()

    
def reporting_menu():
    """
    Function executed when the user chooses the 'R' option in the main menu. 

    Allows the user to choose the options to perform the analyses in reporting module.

    Allowsto navigate through the different options and returnto the main menu.

    @param none
    @return none
    """
    options = ["Daily average (da)", "Daily median (dm)", "Hourly average (ha)", "Monthly average (ma)", "Peak hour (ph)", "Count missing data (cd)", "Fill missing data(fd)"]
    options_abbreviations = ["da", "dm", "ha", "ma", "ph", "cd", "fd"]
    descriptions = ["Prints the daily averages (i.e., 365 values) for a specified pollutant and monitoring station",
                    "Prints the daily median values (i.e., 365 values) for a particular pollutant and monitoring station",
                    "Prints the hourly averages (i.e., 24 values) for a particular pollutant and monitoring station",
                    "Prints the monthly averages (i.e., 12 values) for a particular pollutant and monitoring station",
                    "Prints the hour of the day with the highest pollution level and its corresponding value for a specified date",
                    "Prints the number of 'No data' entries in the data for a specified monitoring station and pollutant",
                    "Prints new data with 'No data' values being replaced by the new specified value"]

    print(f"""\n{utils.colors.fg.purple}{utils.colors.bg.lightgrey}{utils.colors.bold}Welcome to the Reporting Module!{utils.colors.reset}
This module allows you to access pollution statistics of 3 stations during the period from 2021-01-01 until 2021-01-31:
-> Marylebone Road
-> N. Kensington
-> Harlington

Here are the options for you to explore:
    """)
    print(f"+{'-'*120}+")
    for index in range(len(options)):
        print(f"""|{utils.colors.bold}{utils.colors.fg.cyan}{options[index]}:{' '*(len(descriptions[6])-len(options[index]) + 40)}{utils.colors.reset}|
|    > {descriptions[index]}{' '*(len(descriptions[6]) - len(descriptions[index]) + 35)}|
+{'-'*120}+""")

    print(f"""|{utils.colors.bold}{utils.colors.fg.red}Main menu (M):{' '*(len(descriptions[6]) + 27)}{utils.colors.reset}|
|    > Back to main menu{' '*(len(descriptions[6]) + 18)}|
+{'-'*120}+""")

    chosen_option = input(f"""\n{utils.colors.underline}Please enter the function you are interested to explore:{utils.colors.reset} """).strip()
    temp = False
    while not temp:
        if chosen_option.lower() in options_abbreviations or chosen_option.upper() == "M" or chosen_option.upper() == "Q":
            temp = True
        else:
            chosen_option = input("\nSorry, you have entered a non-existing option. Try again: ")
            
    if chosen_option.lower() == "da":
        print(f"You have chosen to print the {utils.colors.fg.purple}{utils.colors.bold}daily averages{utils.colors.reset} for a particular monitoring station and pollutant in 2021")

        stations = ["marylebone", "harlington", "kensington"]
        pollutants = ["NO", "PM10", "PM25"]

        monitoring_station = input("Please enter the monitoring station (Marylebone, Harlington, Kensington): ").strip()
        pollutant = input("Please enter the pollutant (NO, PM10, PM25): ").strip()

        temp = False
        while not temp:
            if monitoring_station.lower() in stations and pollutant.upper() in pollutants:
                temp = True
            else:
                print(f"Sorry, your input was incorrect.")
                monitoring_station = input("Please enter the monitoring station (Marylebone, Harlington, Kensington): ")
                pollutant = input("Please enter the pollutant (NO, PM10, PM25): ")

        result = reporting.daily_average(None, monitoring_station, pollutant.lower())
        result = list(round(val,2) if val != 'No data' else val for val in result)
        print(f"\nThe daily averages at {monitoring_station} station and {pollutant} pollutant are: {result}")

        temp = False
        while not temp:
            cont = input("Do you want to stay in this module (PR) or go back to the main menu (MM)? ")
            if cont.upper() == "PR":
                temp = True
                reporting_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue

    elif chosen_option.lower() == "dm":
        print(f"You have chosen to print the {utils.colors.fg.purple}{utils.colors.bold}daily medians{utils.colors.reset} for a particular monitoring station and pollutant in 2021")

        stations = ["marylebone", "harlington", "kensington"]
        pollutants = ["NO", "PM10", "PM25"]

        monitoring_station = input("Please enter the monitoring station (Marylebone, Harlington, Kensington): ").strip()
        pollutant = input("Please enter the pollutant (NO, PM10, PM25): ").strip()

        temp = False
        while not temp:
            if monitoring_station.lower() in stations and pollutant.upper() in pollutants:
                temp = True
            else:
                print(f"Sorry, your input was incorrect.")
                monitoring_station = input("Please enter the monitoring station (Marylebone, Harlington, Kensington): ")
                pollutant = input("Please enter the pollutant (NO, PM10, PM25): ")

        result = reporting.daily_median(None, monitoring_station, pollutant.lower())
        result = list(round(val,2) if val != 'No data' else val for val in result)
        print(f"\nThe daily medians at {monitoring_station} station and {pollutant} pollutant are: {result}")

        temp = False
        while not temp:
            cont = input("Do you want to stay in this module (PR) or go back to the main menu (MM)? ")
            if cont.upper() == "PR":
                temp = True
                reporting_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue

    elif chosen_option.lower() == "ha":
        print(f"You have chosen to print the {utils.colors.fg.purple}{utils.colors.bold}hourly averages{utils.colors.reset} for a particular monitoring station and pollutant in 2021")

        stations = ["marylebone", "harlington", "kensington"]
        pollutants = ["NO", "PM10", "PM25"]

        monitoring_station = input("Please enter the monitoring station (Marylebone, Harlington, Kensington): ").strip()
        pollutant = input("Please enter the pollutant (NO, PM10, PM25): ").strip()

        temp = False
        while not temp:
            if monitoring_station.lower() in stations and pollutant.upper() in pollutants:
                temp = True
            else:
                print(f"Sorry, your input was incorrect.")
                monitoring_station = input("Please enter the monitoring station (Marylebone, Harlington, Kensington): ")
                pollutant = input("Please enter the pollutant (NO, PM10, PM25): ")

        result = reporting.hourly_average(None, monitoring_station, pollutant.lower())
        result = list(round(val,2) if val != 'No data' else val for val in result)
        print(f"\nThe hourly averages at {monitoring_station} station and {pollutant} pollutant are:")
        for index in range(24):
            print(f"{index+1}:00:00 - {result[index]}")
        
        temp = False
        while not temp:
            cont = input("Do you want to stay in this module (PR) or go back to the main menu (MM)? ")
            if cont.upper() == "PR":
                temp = True
                reporting_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue

    elif chosen_option.lower() == "ma":
        print(f"You have chosen to print the {utils.colors.fg.purple}{utils.colors.bold}monthly averages{utils.colors.reset} for a particular monitoring station and pollutant in 2021")

        stations = ["marylebone", "harlington", "kensington"]
        pollutants = ["NO", "PM10", "PM25"]

        monitoring_station = input("Please enter the monitoring station (Marylebone, Harlington, Kensington): ").strip()
        pollutant = input("Please enter the pollutant (NO, PM10, PM25): ").strip()

        temp = False
        while not temp:
            if monitoring_station.lower() in stations and pollutant.upper() in pollutants:
                temp = True
            else:
                print(f"Sorry, your input was incorrect.")
                monitoring_station = input("Please enter the monitoring station (Marylebone, Harlington, Kensington): ")
                pollutant = input("Please enter the pollutant (NO, PM10, PM25): ")

        result = reporting.monthly_average(None, monitoring_station, pollutant.lower())
        result = list(round(val,2) if val != 'No data' else val for val in result)
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

        print(f"\nThe monthly averages at {monitoring_station} station and {pollutant} pollutant are:")
        for month in months:
            print(f"-> {month}: {result[months.index(month)]}\n")

        temp = False
        while not temp:
            cont = input("Do you want to stay in this module (PR) or go back to the main menu (MM)? ")
            if cont.upper() == "PR":
                temp = True
                reporting_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue

    elif chosen_option.lower() == "ph":
        print(f"You have chosen to print the {utils.colors.fg.purple}{utils.colors.bold}hour of the day with the highest pollution level{utils.colors.reset} and its value for a particular monitoring station, pollutant, and day")

        stations = ["marylebone", "harlington", "kensington"]
        pollutants = ["NO", "PM10", "PM25"]

        monitoring_station = input("Please enter the monitoring station (Marylebone, Harlington, Kensington): ").strip()
        pollutant = input("Please enter the pollutant (NO, PM10, PM25): ").strip()
        date_format = '%Y-%m-%d'
        date = input("Enter the date (YY-MM-DD): ")

        temp = False
        while not temp:
    
            if monitoring_station.lower() in stations and pollutant.upper() in pollutants:
                try:
                    datetime.datetime.strptime(date, date_format)
                    temp = True
                except:
                    print(f"Sorry, your date input was incorrect.")
                    date = input("Enter the date (YY-MM-DD): ")
            else:
                print(f"Sorry, your input of station or pollutant was incorrect.")
                monitoring_station = input("Please enter the monitoring station (Marylebone, Harlington, Kensington): ")
                pollutant = input("Please enter the pollutant (NO, PM10, PM25): ")


        result = reporting.peak_hour_date(None, date, monitoring_station, pollutant.lower())

        if type(result) == tuple:
            print(f"\nThe peak hour for {date} at {monitoring_station} station and {pollutant.upper()} pollutant is {utils.colors.fg.cyan}{utils.colors.bold}{result[1]}{utils.colors.reset} with the pollution value {utils.colors.fg.cyan}{utils.colors.bold}{result[0]}{utils.colors.reset}.\n")
        else:
            print(f"There are several peak hours on {date} at {monitoring_station}:")
            for each in result:
                print(f"Hour: {each[1]} with pollution value {each[0]}")
        
        temp = False
        while not temp:
            cont = input("Do you want to stay in this module (PR) or go back to the main menu (MM)? ")
            if cont.upper() == "PR":
                temp = True
                reporting_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue

    elif chosen_option.lower() == "cd":
        print(f"You have chosen to {utils.colors.fg.purple}{utils.colors.bold}count the number of missing data{utils.colors.reset} for a particular monitoring station and pollutant")

        stations = ["marylebone", "harlington", "kensington"]
        pollutants = ["NO", "PM10", "PM25"]

        monitoring_station = input("Please enter the monitoring station (Marylebone, Harlington, Kensington): ").strip()
        pollutant = input("Please enter the pollutant (NO, PM10, PM25): ").strip()

        temp = False
        while not temp:
            if monitoring_station.lower() in stations and pollutant.upper() in pollutants:
                temp = True
            else:
                print(f"Sorry, your input was incorrect.")
                monitoring_station = input("Please enter the monitoring station (Marylebone, Harlington, Kensington): ")
                pollutant = input("Please enter the pollutant (NO, PM10, PM25): ")

        result = reporting.count_missing_data(None, monitoring_station, pollutant.lower())
        print(f"\nThe number of missing data at {monitoring_station} station and {pollutant} pollutant is: {utils.colors.fg.lightcyan}{utils.colors.bold}{result}{utils.colors.reset}")

        temp = False
        while not temp:
            cont = input("Do you want to stay in this module (PR) or go back to the main menu (MM)? ")
            if cont.upper() == "PR":
                temp = True
                reporting_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue

    elif chosen_option.lower() == "fd":
        print(f"You have chosen to {utils.colors.fg.purple}{utils.colors.bold}replace missing data with a new value{utils.colors.reset} for a particular monitoring station and pollutant")

        stations = ["marylebone", "harlington", "kensington"]
        pollutants = ["NO", "PM10", "PM25"]

        monitoring_station = input("Please enter the monitoring station (Marylebone, Harlington, Kensington): ").strip()
        pollutant = input("Please enter the pollutant (NO, PM10, PM25): ").strip()
        new_value = input("Enter new value: ")

        temp = False
        while not temp:
            if monitoring_station.lower() in stations and pollutant.upper() in pollutants:
                temp = True
            else:
                print(f"Sorry, your input was incorrect.")
                monitoring_station = input("Please enter the monitoring station (Marylebone, Harlington, Kensington): ")
                pollutant = input("Please enter the pollutant (NO, PM10, PM25): ")

        result = reporting.fill_missing_data(None, new_value, monitoring_station, pollutant.lower())

        print(f"\nYour new data is: ")
        for value in result:
            print(value)

        temp = False
        while not temp:
            cont = input("Do you want to stay in this module (PR) or go back to the main menu (MM)? ")
            if cont.upper() == "PR":
                temp = True
                reporting_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue

    elif chosen_option.upper() == "M":
        main_menu()


def monitoring_menu():
    """
    Function executed when the user chooses the 'M' option in the main menu. 

    Allows the user to choose options to perform the tasks implemented for the RM module. 

    Allows to navigate through the different options and return to the main menu.

    @param none
    @return none
    """
    options = ["Find station code (sc)", "Commonly monitored pollutants (mp)", "Pollutant health information (phi)", "Daily air quality index (di)", "Hourly air quality index (hi)", "Station statistics (ss)", "Peak workday (pw)"]
    options_abbreviations = ["sc", "mp", "phi", "di", "hi", "ss", "pw"]
    descriptions = ["Prints the station code of a specified monitoring station",
                    "Prints all the commonly monitored pollutants with their codes",
                    "Prints health information about a specified pollutant",
                    "Prints the day's Air Quality Index for all available pollutants for a specified day and station",
                    "Prints the last hour's pollutants with their Air Quality Index and Air Quality Band",
                    "Prints all hourly data for the specified day(-s), average and peak hour (with value)",
                    "Prints the peak polluted work day at peak hours for all available pollutants for a specified period of time"]

    print(f"""\n{utils.colors.fg.purple}{utils.colors.bg.lightgrey}{utils.colors.bold}Welcome to the Monitoring Module!{utils.colors.reset}
This module provides real-time statistics for different monitoring stations and pollutants

Here are the options for you to explore:
    """)
    print(f"+{'-'*113}+")
    for index in range(len(options)):
        print(f"""|{utils.colors.bold}{utils.colors.fg.cyan}{options[index]}:{' '*(len(descriptions[-1])-len(options[index]) + 5)}{utils.colors.reset}|
|    > {descriptions[index]}{' '*(len(descriptions[-1]) - len(descriptions[index]))}|
+{'-'*113}+""")

    print(f"""{utils.colors.bold}{utils.colors.fg.red}|Main menu (M):{' '*(len(descriptions[-1]) - 8)}{utils.colors.reset}|
|    > Back to main menu{' '*(len(descriptions[-1]) - 17)}|
+{'-'*113}+""")

    chosen_option = input(f"""\n{utils.colors.underline}Please enter the function you are interested to explore:{utils.colors.reset} """).strip()
    temp = False
    while not temp:
        if chosen_option.lower() in options_abbreviations or chosen_option.upper() == "M" or chosen_option.upper() == "Q":
            temp = True
        else:
            chosen_option = input("\nSorry, you have entered a non-existing option. Try again: ")
    
    if chosen_option.lower() == 'sc':
        print(f"\nYou have chosen to find a {utils.colors.fg.purple}{utils.colors.bold}station code{utils.colors.reset}.")

        station = input("Please enter a station name: ")
        station_code = monitoring.find_station_code(station)

        print(f"Station code you are trying to find: {station_code}")

        temp = False
        while not temp:
            cont = input("Do you want to stay in this module (RM) or go back to the main menu (MM)? ")
            if cont.upper() == "RM":
                temp = True
                monitoring_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue
    
    elif chosen_option.lower() == 'mp':
        print(f"\nYou have chosen to find all {utils.colors.fg.purple}{utils.colors.bold}commonly monitored pollutants{utils.colors.reset}.\n")
        monitoring.get_all_available_pollutant_names()

        temp = False
        while not temp:
            cont = input("\nDo you want to stay in this module (RM) or go back to the main menu (MM)? ")
            if cont.upper() == "RM":
                temp = True
                monitoring_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue

    elif chosen_option.lower() == 'phi':
        print(f"\nYou have chosen to find {utils.colors.fg.purple}{utils.colors.bold}health information{utils.colors.reset} about a specified pollutant.\n")
        pollutant = input("Please enter the pollutant code: ")
        print(monitoring.get_particular_pollutant_health_info(pollutant))

        temp = False
        while not temp:
            cont = input("\nDo you want to stay in this module (RM) or go back to the main menu (MM)? ")
            if cont.upper() == "RM":
                temp = True
                monitoring_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue
    
    elif chosen_option.lower() == 'di':
        print(f"\n You have chosen to print the {utils.colors.fg.purple}{utils.colors.bold}day's Air Quality Index for all available pollutants{utils.colors.reset} for a specified day and station")
        site_code = input("Please enter the site code: ")
        date = input("Please enter the date (e.g., 01 Jan 2022): ")
        monitoring.get_daily_for_particular_site(site_code, date)

        temp = False
        while not temp:
            cont = input("\nDo you want to stay in this module (RM) or go back to the main menu (MM)? ")
            if cont.upper() == "RM":
                temp = True
                monitoring_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue

    elif chosen_option.lower() == 'hi':
        print(f"\n You have chosen to print {utils.colors.fg.purple}{utils.colors.bold}last hour's pollutants with their Air Quality Index and Air Quality Band{utils.colors.reset}")
        site_code = input("Please enter the site code: ")
        pollutant = input("Enter species code or enter 'all' to see all available: ")
        output = monitoring.hourly_sitecode_dynamic(site_code, pollutant)
        print(f"+{'-'*50}+")
        print("|{:<15}|{:<15}|{:<15}|".format('Pollutant Code', 'Air Quality Index', 'Air Quality Band'))
        print(f"+{'-'*50}+")

        if pollutant == 'all':
            for pollut in output:
                to_print = [f"{utils.colors.fg.yellow}{utils.colors.bold}{pollut[0]}{utils.colors.reset}", 
                        f"{utils.colors.fg.yellow}{utils.colors.bold}{pollut[1]}{utils.colors.reset}",
                        f"{utils.colors.fg.yellow}{utils.colors.bold}{pollut[2]}{utils.colors.reset}"]
                print("|{:<29}|{:<31}|{:<30}|".format(to_print[0], to_print[1], to_print[2]))
                print(f"+{'-'*50}+")
        else:
            to_print = [f"{utils.colors.fg.yellow}{utils.colors.bold}{output[0]}{utils.colors.reset}", 
                        f"{utils.colors.fg.yellow}{utils.colors.bold}{output[1]}{utils.colors.reset}",
                        f"{utils.colors.fg.yellow}{utils.colors.bold}{output[2]}{utils.colors.reset}"]
            print("|{:<29}|{:<31}|{:<30}|".format(to_print[0], to_print[1], to_print[2]))
            print(f"+{'-'*50}+")

        temp = False
        while not temp:
            cont = input("\nDo you want to stay in this module (RM) or go back to the main menu (MM)? ")
            if cont.upper() == "RM":
                temp = True
                monitoring_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue

    elif chosen_option.lower() == 'ss':
        print(f"You have chosen to print {utils.colors.fg.purple}{utils.colors.bold}all hourly data{utils.colors.reset} for the specified day(-s), average or peak hour (with value)")
        species_code = str(input("Please enter the species code: "))
        site_code = str(input("Please enter the site code: "))
        start_date = str(input("Enter the start date (e.g., 01 Jan 2022): "))
        end_date = str(input("Enter the end date (e.g., 01 Jan 2022): "))

        output = monitoring.get_live_data_for_station_species(site_code, species_code, start_date, end_date)

        print(output[0])
        print(f"{utils.colors.fg.yellow}{utils.colors.bold}Average: {utils.colors.reset}{output[1]}")
        print(f"{utils.colors.fg.yellow}{utils.colors.bold}Peak hour{utils.colors.reset}: {output[2][1]} with the value of {output[2][0]}")

        temp = False
        while not temp:
            cont = input("\nDo you want to stay in this module (RM) or go back to the main menu (MM)? ")
            if cont.upper() == "RM":
                temp = True
                monitoring_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue

    elif chosen_option.lower() == 'pw':
        print(f"You have chosen to print {utils.colors.fg.purple}{utils.colors.bold}the peak polluted work day at peak hours (07:00-09:00 and 16:00-19:00){utils.colors.reset} for all available pollutants for a specified period of time")
        site_code = str(input("Please enter the site code: "))
        start_date = str(input("Enter the start date (e.g., 01 Jan 2022): "))
        end_date = str(input("Enter the end date (e.g., 01 Jan 2022): "))

        output = monitoring.peak_workday(site_code, start_date, end_date)
    
        for pollutant in output:
            if output[pollutant] == 'No data':
                print(f"{utils.colors.fg.red}{utils.colors.bold}{pollutant}{utils.colors.reset}: {output[pollutant]}")
            else:
                print(f"{utils.colors.fg.red}{utils.colors.bold}{pollutant}{utils.colors.reset}: {[val for val in output[pollutant]]}")
        
        temp = False
        while not temp:
            cont = input("\nDo you want to stay in this module (RM) or go back to the main menu (MM)? ")
            if cont.upper() == "RM":
                temp = True
                monitoring_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue
    
    elif chosen_option.upper() == "M":
        main_menu()


def intelligence_menu():
    """
    Function executed when the user chooses the 'I' option in the main menu. 

    Allows the user to choose the options to perform the tasks implemented in MI module.

    Allows to navigate through the different options and return to the main menu.

    @param none
    @return none
    """
    options = ["Find red pixels (fr)", "Find cyan pixels (fc)", "Detect connected components (dc)", "Sort connected components (sc)"]
    options_abbreviations = ["fr", "fc", "dc", "sc"]
    descriptions = ["Makes an image of pavement walkable from both sides ('map-red-pixels.jpg')",
                    "Makes an image of pavement walkable from one side ('map-cyan-pixels.jpg')",
                    "Detects connected components and saves in a file 'cc-output-2a.txt'",
                    "Sorts the passed connected components by size ('cc-output-2b.txt') and saves two largest components ('cc-top-2.jpg')"]

    print(f"""\n{utils.colors.fg.purple}{utils.colors.bg.lightgrey}{utils.colors.bold}Welcome to the Intelligence Module!{utils.colors.reset}
This module is responsible for the analyses of the road infrastructure around one of the three monitoring stations:
-> Marylebone Road
-> N. Kensington
-> Harlington

Here are the options for you to explore:
    """)
    print(f"+{'-'*122}+")
    for index in range(len(options)):
        print(f"""|{utils.colors.bold}{utils.colors.fg.cyan}{options[index]}:{' '*(len(descriptions[3])-len(options[index]) + 5)}{utils.colors.reset}|
|    > {descriptions[index]}{' '*(len(descriptions[3]) - len(descriptions[index]))}|
+{'-'*122}+""")

    print(f"""{utils.colors.bold}{utils.colors.fg.red}|Main menu (M):{' '*(len(descriptions[3]) - 8)}{utils.colors.reset}|
|    > Back to main menu{' '*(len(descriptions[3]) - 17)}|
+{'-'*122}+""")

    chosen_option = input(f"""\n{utils.colors.underline}Please enter the function you are interested to explore:{utils.colors.reset} """)
    temp = False
    while not temp:
        if chosen_option.lower() in options_abbreviations or chosen_option.upper() == "M" or chosen_option.upper() == "Q":
            temp = True
        else:
            chosen_option = input("\nSorry, you have entered a non-existing option. Try again: ")

    if chosen_option.lower() =="fr":
        print(f"You have chosen to {utils.colors.fg.purple}{utils.colors.bold}create an image of pavement walkable from both sides{utils.colors.reset} ('map-red-pixels.jpg')")

        address = input("Please enter the address of the pavement image (EXcluding the address of the current working directory e.g., data/map.png): ")
        intelligence.find_red_pixels(address)

        print(f"\nImage is created!")

        temp = False
        while not temp:
            cont = input("Do you want to stay in this module (MI) or go back to the main menu (MM)? ")
            if cont.upper() == "MI":
                temp = True
                intelligence_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue
    
    elif chosen_option.lower() == "fc":
        print(f"You have chosen to {utils.colors.fg.purple}{utils.colors.bold}create an image of pavement walkable from one side{utils.colors.reset} ('map-cyan-pixels.jpg')")

        address = input("Please enter the address of the pavement image (EXcluding the address of the current working directory e.g., data/map.png): ")
        intelligence.find_cyan_pixels(address)

        print(f"\nImage is created!")

        temp = False
        while not temp:
            cont = input("Do you want to stay in this module (MI) or go back to the main menu (MM)? ")
            if cont.upper() == "MI":
                temp = True
                intelligence_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue

    elif chosen_option.lower() == "dc":
        print(f"\n You have chosen to {utils.colors.fg.purple}{utils.colors.bold}detect connected components{utils.colors.reset} and save them to a file 'cc-output-2a.txt'")
        colour = input("Red or cyan pavement? ")
        if colour.lower() == 'red':
            if os.path.exists(f"{os.getcwd()}/map-red-pixels.jpg"):
                address = input("Please enter the address of the initial pavement image: ")
                intelligence.detect_connected_components(intelligence.find_red_pixels(address))
                print(f"\nFile with the detected connected components is created!")
            else:
                print(f"There is no map yet. You need to do 'Find red pixels' function first.")
        else:
            if os.path.exists(f"f{os.getcwd()}/map-cyan-pixels.jpg"):
                address = input("Please enter the address of the initial pavement image (EXcluding the address of the current working directory e.g., data/map.png): ")
                intelligence.detect_connected_components(intelligence.find_cyan_pixels(address))
                print(f"\nFile with the detected connected components is created!")
            else:
                print(f"There is no map yet. You need to do 'Find cyan pixels' function first.")
        
        temp = False
        while not temp:
            cont = input("Do you want to stay in this module (MI) or go back to the main menu (MM)? ")
            if cont.upper() == "MI":
                temp = True
                intelligence_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue

    elif chosen_option.lower() == "sc":
        print(f"\n You have chosen to {utils.colors.fg.purple}{utils.colors.bold}sort the connected components by size{utils.colors.reset} ('cc-output-2b.txt') and save two largest components ('cc-top-2.jpg')")
        if os.path.exists(f"{os.getcwd()}/cc-output-2a.txt"):
            address = input("Please enter the address of the initial pavement image (EXcluding the address of the current working directory e.g., data/map.png): ")
            colour = input("Red or cyan pavement? ")
            if colour.lower() == 'red':
                # Delete everything written in the 'cc-output-2a.txt' since new data will be appended when performing the function
                file_to_delete = open("cc-output-2a.txt", "w")
                file_to_delete.close()
                intelligence.detect_connected_components_sorted(intelligence.detect_connected_components(intelligence.find_red_pixels(address)))
                print(f"\nFile with the sorted detected connected components is created!")
            else:
                # Delete everything written in the 'cc-output-2a.txt' since new data will be appended when performing the function
                file_to_delete = open("cc-output-2a.txt", "w")
                file_to_delete.close()
                print(f"\nFile with the sorted detected connected components is created!")
                intelligence.detect_connected_components_sorted(intelligence.detect_connected_components(intelligence.find_cyan_pixels(address)))
            
            print(f"\nImage is created!")

        else:
            print(f"\nThere is no file with connected components yet.")
            print(f"You need to do 'Detect connected components' function firts.")

        temp = False
        while not temp:
            cont = input("Do you want to stay in this module (MI) or go back to the main menu (MM)? ")
            if cont.upper() == "MI":
                temp = True
                intelligence_menu()
            elif cont.upper() == "MM":
                temp = True
                main_menu()
            else:
                continue
    
    elif chosen_option.upper() == "M":
        main_menu()


def about():
    """
    Function that executed when the user chooses the 'A' option in the main menu.

    Prints module code and 6-digit candidate number.
    
    @param none
    @return none
    """
    candidate_number = "257628"
    print("\n\n\n")
    print(f"{utils.colors.fg.red}{utils.colors.bold}Module code:{utils.colors.reset} {utils.colors.italic}ECM1400{utils.colors.reset}")
    print(f"{utils.colors.fg.green}{utils.colors.bold}Candidate number:{utils.colors.reset} {candidate_number}")

    return main_menu()


def quit():
    """
    Function that will be executed when the user chooses the 'Q' option in the main menu.
    
    Terminates the program.
    
    @param none
    @return none
    """
    exit()


if __name__ == '__main__':
    main_menu()