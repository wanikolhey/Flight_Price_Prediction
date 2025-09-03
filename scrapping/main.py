import threading
import data_extractor

class main():
    def __init__(self):
        """
        This class is the main scrapper class.
        """
        self.FINAL_DATA = {}

        self.lock = threading.Lock()

        self.dates = data_extractor.date_generator("04/09/2025")
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

    def main(self):
        """
        This function runs the main thread.
        Returns:

        """
        for i in range(10):
            self.thread_init(self.list[i])

        for thread in self.threads:
            thread.join()

        return self.FINAL_DATA

if __name__ == "__main__":
    scrapper = main()
    data = scrapper.main()
    print(data)

