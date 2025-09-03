import threading
import data_extractor

class main():
    def __init__(self):
        self.FINAL_DATA = {}

        self.dates = data_extractor.date_generator()
        self.threads = []

        self.list = []
        self.list[0] = self.dates[0:36]
        self.list[1] = self.dates[36:72]
        self.list[2] = self.dates[72:108]
        self.list[3] = self.dates[108:144]
        self.list[4] = self.dates[144:180]
        self.list[5] = self.dates[180:216]
        self.list[6] = self.dates[216:252]
        self.list[7] = self.dates[252:288]
        self.list[8] = self.dates[288:324]
        self.list[9] = self.dates[324:365]

    def thread_init(self, dates: list) -> None:
        thread = threading.Thread(target=data_extractor.extract_details, args=(dates,))
        thread.start()
        self.threads.append(thread)

    def main(self):
        for i in range(10):
            self.thread_init(self.list[i])

