def validate_input(msg, minDay, maxDay):
    while True:
        try:
            value = int(input(msg))
            if value < minDay or value > maxDay:
                print(f"Out of range - values must be in the range {minDay} to {maxDay}.")
            else:
                return value
        except ValueError:
            print("Integer required.")


def validate_date_input():
    day = validate_input("Please enter the day of the survey in the format dd: ", 1, 31)
    month = validate_input("Please enter the month of the survey in the format mm: ", 1, 12)
    year = validate_input("Please enter the year of the survey in the format yyyy: ", 2000, 2024)
    return day, month, year

def process_csv_data(file_name, day, month, year):
    print(f"Processing {file_name}")


def display_outcomes(outcomes):
    pass



def validate_continue_input():
    while True:
        user_input = input("\nDo you want to process another file? (y/n): ").strip().lower()
        if user_input in ['y', 'n']:
            return user_input == 'y'
        print("Invalid input. Enter 'y' for yes or 'n' for no.")


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
if __name__ == "__main__":
    main()