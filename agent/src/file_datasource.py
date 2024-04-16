from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.parking import Parking
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
import csv

class FileDatasource:
    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
        parking_filename: str,
    ) -> None:
        
        self.is_reading_stoped = False

        self.accelerometer_filename = accelerometer_filename
        self.accelerometer_data = []
        self.accelerometer_data_reading_finished = False

        self.gps_filename = gps_filename
        self.gps_data = []
        self.gps_reading_reading_finished = False

        self.parking_filename = parking_filename
        self.parking_data = []
        self.parking_reading_reading_finished = False

    def read(self) -> AggregatedData:
        if self.is_reading_stoped: return;
    
        acc_data = [0] * 3
        if len(self.accelerometer_data) > 0:
            acc_data = list(map(float, self.accelerometer_data.pop(0)))
        else :
            self.accelerometer_data_reading_finished = True

        gps_data = [0] * 2
        if len(self.gps_data) > 0:
            gps_data = list(map(float, self.gps_data.pop(0)))
        else :
            self.gps_reading_reading_finished = True

        park_data = [0] * 3
        if len(self.parking_data) > 0:
            park_data = list(map(float, self.parking_data.pop(0)))
        else :
            self.parking_reading_reading_finished = True

        self.stopReading()

        """Метод повертає дані отримані з датчиків"""
        return AggregatedData(
            Accelerometer(*acc_data),
            Gps(*gps_data),
            datetime.now(),
            Parking(park_data[0], Gps(park_data[1],park_data[2]))
        )

    def startReading(self, *args, **kwargs):
        
        def read_csv(filename):
            data = []
            with open(filename, 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    data.append(row)
            return data[1:]
        
        self.accelerometer_data = read_csv(self.accelerometer_filename)
        self.gps_data = read_csv(self.gps_filename)
        self.parking_data = read_csv(self.parking_filename)

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        self.is_reading_stoped = self.accelerometer_data_reading_finished and self.gps_reading_reading_finished and self.parking_reading_reading_finished
