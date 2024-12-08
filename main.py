import csv
import os


def validate_input(msg, min_day, max_day):
    while True:
        try:
            value = int(input(msg))
            if value < min_day or value > max_day:
                print(f"Out of range - values must be in the range {min_day} to {max_day}.")
            else:
                return value
        except ValueError:
            print("Integer required.")



def validate_date_input():
    day = validate_input("Please enter the day of the survey in the format dd: ", 1, 31)
    month = validate_input("Please enter the month of the survey in the format mm: ", 1, 12)
    year = validate_input("Please enter the year of the survey in the format yyyy: ", 2000, 2024)
    return day, month, year



def validate_continue_input():
    while True:
        user_input = input("\nDo you want to process another file? (y/n): ").strip().lower()
        if user_input in ['y', 'n']:
            return user_input == 'y'
        print("Invalid input. Enter 'y' for yes or 'n' for no.")



def process_csv_data(file_name, day, month, year):
    print(f"Processing {file_name}")
    # Initialize metrics dictionary
    outcomes = {
        "Total Vehicles": 0,
        "Total Trucks": 0,
        "Total Electric Vehicles": 0,
        "Two-Wheeled Vehicles": 0,
        "Buses North": 0,
        "Straight Through": 0,
        "Truck Percentage": 0,
        "Over Speed Limit": 0,
        "Elm Ave Rabbit Road": 0,
        "Hanley Highway Westway": 0,
        "Scooter Percentage": 0,
        "Highest Hourly Count": 0,
        "Most Vehicles Hour": "",
        "Rain Hours": 0,
        "Date": f"{day:02d}{month:02d}{year}",
        "Data File": os.path.basename(file_name)
    }

    # Check file existence
    if not os.path.exists(file_name):
        print(f"File {file_name} does not exist.")
        return None

    # Initialize counters and data structures
    total_vehicles = 0
    total_trucks = 0
    total_electric_vehicles = 0
    two_wheeled_vehicles = 0
    buses_north = 0
    straight_through = 0
    over_speed_limit = 0
    elm_ave_vehicles = 0
    hanley_highway_vehicles = 0
    scooters = 0
    rainy_hours = set()
    hourly_bicycles = set()
    hanley_hourly_counts = {}
    total_bicycle_count = 0

    # Process the CSV file
    try:
        with open(file_name, mode='r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                vehicle_type = row["VehicleType"]
                time_of_day = row["timeOfDay"]
                speed_limit = int(row["JunctionSpeedLimit"])
                vehicle_speed = int(row["VehicleSpeed"])
                is_electric = row["electricHybrid"] == "True"
                junction_name = row["JunctionName"]
                weather_conditions = row["Weather_Conditions"]
                travel_in = row["travel_Direction_in"]
                travel_out = row["travel_Direction_out"]

                # Increment total vehicle count
                total_vehicles += 1

                # Count vehicles at specific junctions
                if junction_name == "Elm Avenue/Rabbit Road":
                    elm_ave_vehicles += 1
                if junction_name == "Hanley Highway/Westway":
                    hanley_highway_vehicles += 1

                # Count vehicle types
                if vehicle_type == "Truck":
                    total_trucks += 1
                if is_electric:
                    total_electric_vehicles += 1
                if vehicle_type in ["Bicycle", "Motorcycle", "Scooter"]:
                    two_wheeled_vehicles += 1

                # Count buses traveling north
                if junction_name == "Elm Avenue/Rabbit Road" and vehicle_type == "Buss" and travel_out == "N":
                    buses_north += 1

                # Count straight-through vehicles
                if travel_in == travel_out:
                    straight_through += 1

                # Count vehicles exceeding speed limit
                if vehicle_speed > speed_limit:
                    over_speed_limit += 1

                # Count scooters at specific junction
                if vehicle_type == "Scooter" and junction_name == "Elm Avenue/Rabbit Road":
                    scooters += 1

                # Record hourly vehicle counts at Hanley Highway/Westway
                if junction_name == "Hanley Highway/Westway":
                    hour = time_of_day.split(":")[0]
                    if hour not in hanley_hourly_counts:
                        hanley_hourly_counts[hour] = 0
                    hanley_hourly_counts[hour] += 1

                # Record hourly bicycle counts
                if vehicle_type == "Bicycle":
                    hour = time_of_day.split(":")[0]  # Extract the hour
                    hourly_bicycles.add(hour)  # Track unique hours bicycles were recorded
                    total_bicycle_count += 1  # Increment total bicycle count

                # Count rainy hours
                date = row["Date"]
                time_of_day = row["timeOfDay"]
                if weather_conditions == "Light Rain" or weather_conditions == "Heavy Rain":
                    # Extract hour from the time_of_day
                    hour = time_of_day.split(":")[0]
                    # Create a unique key for (date, hour)
                    rainy_hours.add((date, hour))
        total_rainy_hours = len(rainy_hours)

        # Update outcomes with calculated metrics
        outcomes.update({
            "Total Vehicles": total_vehicles,
            "Total Trucks": total_trucks,
            "Total Electric Vehicles": total_electric_vehicles,
            "Two-Wheeled Vehicles": two_wheeled_vehicles,
            "Buses North": buses_north,
            "Straight Through": straight_through,
            "Over Speed Limit": over_speed_limit,
            "Elm Ave Rabbit Road": elm_ave_vehicles,
            "Hanley Highway Westway": hanley_highway_vehicles,
            "Truck Percentage": round((total_trucks / total_vehicles) * 100) if total_vehicles else 0,
            "Rain Hours": total_rainy_hours,
        })

        # Calculate the total number of unique hours for the date
        unique_hours_in_day = len(set(range(0, 24)))  # 24 hours in a day
        total_hours = unique_hours_in_day

        average_bicycles_per_hour = round(total_bicycle_count / total_hours) if total_hours > 0 else 0
        outcomes["Average Bicycles Per Hour"] = average_bicycles_per_hour

        # Calculate scooter percentage
        if elm_ave_vehicles > 0:
            scooter_percentage = (scooters / elm_ave_vehicles) * 100
            outcomes["Scooter Percentage"] = int(scooter_percentage)
        else:
            outcomes["Scooter Percentage"] = 0

        # Determine highest hourly count and corresponding times
        if hanley_hourly_counts:
            highest_hourly_count = max(hanley_hourly_counts.values())
            outcomes["Highest Hourly Count"] = highest_hourly_count
            most_vehicles_hours = [hour for hour, count in hanley_hourly_counts.items() if
                                   count == highest_hourly_count]
            outcomes["Most Vehicles Hour"] = " and ".join(
                [f"Between {hour}:00 and {int(hour) + 1}:00" for hour in most_vehicles_hours])

    except Exception as e:
        print(f"Error processing file: {e}")
        return None

    return outcomes


def display_outcomes(outcomes):
    if not outcomes:
        print("No data to display.")
        return

    print(f"data file selected is {outcomes['Data File']}\n")
    print(f"The total number of vehicles recorded for this date is {outcomes['Total Vehicles']}")
    print(f"The total number of trucks recorded for this date is {outcomes['Total Trucks']}")
    print(f"The total number of electric vehicles for this date is {outcomes['Total Electric Vehicles']}")
    print(f"The total number of two-wheeled vehicles for this date is {outcomes['Two-Wheeled Vehicles']}")
    print(f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes['Buses North']}")
    print(f"The total number of Vehicles through both junctions not turning left or right is {outcomes['Straight Through']}")
    print(f"The percentage of total vehicles recorded that are trucks for this date is {outcomes['Truck Percentage']}%.")
    print(f"The average number of Bikes per hour for this date is {outcomes['Average Bicycles Per Hour']}")
    print(f"The total number of Vehicles recorded as over the speed limit for this date is {outcomes['Over Speed Limit']}")
    print(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['Elm Ave Rabbit Road']}")
    print(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['Hanley Highway Westway']}")
    print(f"{outcomes['Scooter Percentage']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.")
    print(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['Highest Hourly Count']}")
    print(f"The most vehicles through Hanley Highway/Westway were recorded {outcomes['Most Vehicles Hour']}")
    print(f"The number of hours of rain for this date is {outcomes['Rain Hours']}")
    print("\n***************************************************************\n")


def save_results_to_file(outcomes_list):
    file_name = "results.txt"
    try:
        with open(file_name, "a") as file:
            for outcomes in outcomes_list:
                file.write(f"Data file selected is {outcomes['Data File']}\n")
                file.write(
                    f"\nThe total number of vehicles recorded for this date is {outcomes['Total Vehicles']}\n")
                file.write(
                    f"The total number of trucks recorded for this date is {outcomes['Total Trucks']}\n")
                file.write(
                    f"The total number of electric vehicles for this date is {outcomes['Total Electric Vehicles']}\n")
                file.write(
                    f"The total number of two-wheeled vehicles for this date is {outcomes['Two-Wheeled Vehicles']}\n")
                file.write(
                    f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes['Buses North']}\n")
                file.write(
                    f"The total number of Vehicles through both junctions not turning left or right is {outcomes['Straight Through']}\n")
                file.write(
                    f"The percentage of total vehicles recorded that are trucks for this date is {outcomes['Truck Percentage']}%\n")
                file.write(
                    f"The average number of Bikes per hour for this date is {outcomes['Average Bicycles Per Hour']}\n")
                file.write(
                    f"The total number of Vehicles recorded as over the speed limit for this date is {outcomes['Over Speed Limit']}\n")
                file.write(
                    f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['Elm Ave Rabbit Road']}\n")
                file.write(
                    f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['Hanley Highway Westway']}\n")
                file.write(
                    f"{outcomes['Scooter Percentage']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters\n")
                file.write(
                    f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['Highest Hourly Count']}\n")
                file.write(
                    f"The most vehicles through Hanley Highway/Westway were recorded between {outcomes['Most Vehicles Hour']}\n")
                file.write(
                    f"The number of hours of rain for this date is {outcomes['Rain Hours']}\n")
                file.write("\n***************************************************************\n")

    except Exception as e:
        print(f"Error saving results: {e}")


def main():
    print("*********************************************\n"
          "\tTraffic Data Analysis Program\n"
          "*********************************************\n")
    outcomes_list = []
    while True:
        day, month, year = validate_date_input()
        file_name = f"traffic_data{day:02}{month:02}{year}.csv"
        outcomes = process_csv_data(file_name, day, month, year)

        if outcomes:
            outcomes_list.append(outcomes)
            display_outcomes(outcomes)

        if not validate_continue_input():
            break

    save_results_to_file(outcomes_list)

if __name__ == "__main__":
    main()