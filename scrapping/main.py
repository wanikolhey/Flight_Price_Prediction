import threading
import data_extractor
import csv
import re

class main():
    def __init__(self):
        """
        This class is the main scrapper class.
        """
        self.FINAL_DATA = {}

        self.lock = threading.Lock()

        self.dates = data_extractor.date_generator()
        self.threads = []
        num_threads = 10

        self.list = [self.dates[i * len(self.dates) // num_threads: (i + 1) * len(self.dates) // num_threads] for i in
                     range(num_threads)]

    def thread_init(self, dates: list) -> None:
        """
        This function initializes a new thread for data extraction.
        Args:
            dates:

        Returns:

        """
        thread = threading.Thread(target=self.get_data, args=(dates,))
        thread.start()
        self.threads.append(thread)

    def get_data(self, dates: list) -> None:
        """
        This function extracts data from the given dates.
        Args:
            dates:

        Returns:

        """
        result = data_extractor.extract_details(dates)
        with self.lock:
            self.FINAL_DATA.update(result)

    def convert_to_csv(self, flight_data: dict, csv_file_name: str = "flight_data.csv", headers: list = ['Date', 'Airline', 'Departure_Time', 'Arrival_Time', 'Duration', 'Price']) -> None:
        """
        Converts the flight_data dictionary to a CSV file.
        Args:
            flight_data:
            csv_file_name:
            headers:
        Returns:

        """
        try:
            # Open the file for writing
            with open(csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                # Write the header row
                writer.writerow(headers)

                # Loop through each date and its list of flights in the dictionary
                for date, flights in flight_data.items():
                    # Loop through each individual flight's details
                    for flight_details in flights:
                        # Check for expected structure to avoid errors
                        if len(flight_details) == 4 and isinstance(flight_details[1], list) and len(
                                flight_details[1]) == 2:
                            airline = flight_details[0]
                            departure_time = flight_details[1][0]
                            arrival_time = flight_details[1][1]
                            duration = flight_details[2]
                            raw_price_string = flight_details[3]

                            # Cleaning the Price
                            price_part = raw_price_string.split('Rs.')[-1]
                            cleaned_price = re.sub(r'[^\d]', '', price_part)

                            # Create a list representing the row to write
                            row_to_write = [date, airline, departure_time, arrival_time, duration, cleaned_price]

                            # Write the row to the CSV file
                            writer.writerow(row_to_write)

            print(f"Successfully converted the dictionary to '{csv_file_name}'")

        except IOError as e:
            print(f"Error writing to file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def main(self):
        """
        This function runs the main thread.
        Returns:

        """
        for i in range(10):
            self.thread_init(self.list[i])

        for thread in self.threads:
            thread.join()

        self.convert_to_csv(self.FINAL_DATA)

if __name__ == "__main__":
    scrapper = main()
    scrapper.main()
    print("Done!")


