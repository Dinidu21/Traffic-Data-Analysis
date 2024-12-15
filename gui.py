import tkinter as tk
import csv


# Task D: Histogram Display using tkinter
class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.

        Args:
            traffic_data (list): A list of dictionaries containing traffic data
            date (str): The selected date in the format DDMMYYYY
        """
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.root.title(f"Histogram - {self.date}")
        self.canvas = tk.Canvas(self.root, width=900, height=620, bg="white")
        self.canvas.pack()

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.

        This includes creating the title, X-axis label, and setting up the
        canvas for the histogram drawing.
        """

        # Title
        self.canvas.create_text(
            400, 40,
            text=f"Histogram of Vehicle Frequency per Hour ({self.date})",
            font=("Poppins", 16)
        )

        # X-axis Label
        self.canvas.create_text(
            400, 580,
            text="Hours 00:00 to 24:00",
            font=("Poppins", 12)
        )

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars for vehicle frequency per hour.
        """
        # Initialize a dictionary to store vehicle counts per hour for each junction
        hourly_data = {hour: [0, 0] for hour in range(24)}

        # Populate hourly_data with vehicle counts from traffic_data
        for record in self.traffic_data:
            hour = int(record['timeOfDay'].split(":")[0])  # Extract hour from timeOfDay
            if record['JunctionName'] == 'Elm Avenue/Rabbit Road':
                hourly_data[hour][0] += 1  # Increment Elm Avenue count
            elif record['JunctionName'] == 'Hanley Highway/Westway':
                hourly_data[hour][1] += 1  # Increment Hanley Highway count

        # Calculate the maximum traffic count to determine scaling factor
        max_traffic = max(max(counts) for counts in hourly_data.values())
        scaling_factor = 450 / max_traffic if max_traffic > 0 else 1

        # Draw histogram bars and labels for each hour
        for hour, (elm_count, hanley_count) in hourly_data.items():
            x0 = 60 + hour * 30  # Calculate x-coordinate based on hour
            elm_height = elm_count * scaling_factor
            hanley_height = hanley_count * scaling_factor

            # Draw Elm Avenue bar and display its count
            self.canvas.create_rectangle(x0, 550 - elm_height, x0 + 10, 550, fill="#4bc949", outline="#4bc949")
            self.canvas.create_text(x0 + 5, 550 - elm_height - 10, text=str(elm_count), font=("Arial", 8), fill="green")

            # Draw Hanley Highway bar and display its count
            self.canvas.create_rectangle(x0 + 15, 550 - hanley_height, x0 + 25, 550, fill="#f9969b", outline="#f9969b")
            self.canvas.create_text(x0 + 20, 550 - hanley_height - 10, text=str(hanley_count), font=("Arial", 8), fill="red")

            # Label the hour below the bars
            self.canvas.create_text(x0 + 14, 560, text=f"{hour:02d}", font=("Arial", 8))

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.

        This function creates two rectangles and two text labels to create a legend
        for the histogram. The first rectangle and label are for Elm Avenue/Rabbit Road,
        while the second pair are for Hanley Highway/Westway.
        """
        # Create Elm Avenue/Rabbit Road rectangle and label
        self.canvas.create_rectangle(650, 100, 670, 120, fill="#4bc949", outline="#4bc949")
        self.canvas.create_text(700, 110, text="Elm Avenue/Rabbit Road", anchor="w", font=("Arial", 10))

        # Create Hanley Highway/Westway rectangle and label
        self.canvas.create_rectangle(650, 130, 670, 150, fill="#f9969b", outline="#f9969b")
        self.canvas.create_text(700, 140, text="Hanley Highway/Westway", anchor="w", font=("Arial", 10))

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.

        This method calls the methods to set up the window, draw the histogram,
        and add the legend. Finally, it starts the Tkinter main loop to display
        the histogram.
        """
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        # Start the Tkinter main loop to display the histogram
        self.root.mainloop()

# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.

        This class is designed to handle multiple CSV files. It keeps track of the
        current data being processed and provides methods to load a new CSV file,
        clear the previous data, and handle user interaction when processing a new
        dataset.
        """
        self.current_data = None
        """
        Keeps track of the current data being processed. This is set to None initially
        and is updated when a new CSV file is loaded.
        """

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.

        Args:
            file_path (str): The path to the CSV file to be loaded.

        This method reads the CSV file and stores the data in the current_data
        attribute. The data is stored as a list of dictionaries, where each
        dictionary represents a row in the CSV file. The keys of the dictionary
        are the column names in the CSV file.
        """
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            self.current_data = list(reader)

    def clear_previous_data(self):
        """
        Clears the current data stored in memory.

        This method resets the current_data attribute to None, ensuring that
        any data from a previous dataset is removed before processing a new dataset.
        """
        # Reset the current_data attribute to clear previous dataset
        self.current_data = None

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.

        This method repeatedly prompts the user to input a CSV file path until
        a valid file path is entered. The method then loads the CSV file using
        the load_csv_file method and breaks out of the loop. If the file is not
        found, the method prints an error message and continues to prompt the
        user for input.
        """
        while True:
            file_path = input("Please enter the CSV file path: ").strip()
            if not file_path:
                print("Input cannot be empty.")
                continue

            try:
                self.load_csv_file(file_path)
                break
            except FileNotFoundError:
                print("File not found. Please try again.")

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.

        This method clears previous data, handles user input for a new file, and
        processes the file using the HistogramApp class. The user is then asked
        if they want to process another file. If the user enters 'N', the loop
        breaks and the program exits.
        """
        while True:
            # Clear previous data
            self.clear_previous_data()

            # Handle user input for a new file
            self.handle_user_interaction()

            # Get the date for the histogram
            date = input("Please enter the date for the histogram (DD/MM/YYYY): ").strip()
            if not date:
                print("Input cannot be empty.")
                continue

            # Create a new HistogramApp instance and run it
            app = HistogramApp(self.current_data, date)
            app.run()

            # Ask the user if they want to process another file
            continue_input = input("Do you want to process another file? (Y/N): ").strip().upper()
            if continue_input == 'N':
                break
