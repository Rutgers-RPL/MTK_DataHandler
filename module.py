import zip
import numpy as np
import matplotlib.pyplot as plt

class FlightDataHandler:

    def __init__(self, launch_date = None, board_version = None) -> None:
        self.file_path = None
        self.launch_date = launch_date
        self.board_version = board_version
        self.packet_data = None
        self.state_data = None
        self.config = None
        self.state_data_dict = None

        self.state_column_to_index = {'magic':0, 'state_flags':1, 'arming_time':2, 
                                      'apogee_time':3, 'drogue_time': 4, 'main_time': 5, 
                                      'sus_time':6}

        self.column_to_index = {'magic':0, 'status':1, 'time_us':2, 'main_voltage_v':3, 'pyro_voltage_v':4, 'numSatellites':5, 'gpsFixType':6, 'latitude_degrees':7, 
    'longitude_degrees':8, 'gps_hMSL_m':9, 'barometer_hMSL_m':10, 'temperature_c':11, 'acceleration_x_mss':12, 'acceleration_y_mss':13, 'acceleration_z_mss':14, 
    'angular_velocity_x_rads':15, 'angular_velocity_y_rads':16, 'angular_velocity_z_rads':17, 'gauss_x':18, 'gauss_y':19, 'gauss_z':20, 
    'kf_acceleration_mss':21, 'kf_velocity_ms':22, 'kf_position_m':23, 'w':24, 'x':25, 'y':26, 'z':27, 'checksum':28}

    def update_column_to_index(self,updated):
        self.column_to_index = updated
    
    def from_np(self,file_path,launch_date = None, board_version = None, packet_data= True):
        self.launch_date = launch_date
        self.board_version = board_version
        if packet_data:
            self.packet_data = np.load(file_path)
        else:
            self.state_data = np.load(file_path)
        
    

    def plot_column(self, column_name, title = None, start = None, end = None):
        if start is None:
            start = 0
        if self.data is None:
            print("No data loaded.")
            return
        if column_name not in self.column_to_index:
            print(f"Column: '{column_name}' not found in data.")
            return
        index = self.column_to_index[column_name]
        if end is None:
            end = self.packet_data[index].shape[0]
        self.packet_data[index].plot(kind='line', title=title or f"{column_name} over Time")
        plt.xlabel("Index")
        plt.ylabel(column_name)
        plt.show()

    def display_metadata(self):
        print(f"Launch Date: {self.launch_date}")
        print(f"Board Version: {self.board_version}")

    def find_stages(self):

        #populates state_data_dict with column_name value pairings

        if self.state_data is None:
            print("No state data loaded.")
            return

        self.state_data_dict = {}

        for column_name, index in self.state_column_to_index.items():
            self.state_data_dict[column_name] = self.state_data[1, index]

    
    def plot_column_with_stages(self, column_name, title = None, start = None, end = None):
        if start is None:
            start = 0
        if self.data is None:
            print("No data loaded.")
            return
        if column_name not in self.column_to_index:
            print(f"Column: '{column_name}' not found in data.")
            return
        index = self.column_to_index[column_name]
        if end is None:
            end = self.packet_data[index].shape[0]

        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '#FF5733']

        if not self.state_data_dict:
            print("No state data loaded.")
            return

        for i, (stage_name, stage_time) in enumerate(self.state_data_dict.items()):
            color = colors[i % len(colors)]  
            plt.axvline(x=stage_time, color=color, linestyle='--', label=stage_name)
        

        self.packet_data[index].plot(kind='line', title=title or f"{column_name} over Time")
        plt.xlabel("Index")
        plt.ylabel(column_name)
        plt.show()

    def display_metadata(self):
        print(f"Launch Date: {self.launch_date}")
        print(f"Board Version: {self.board_version}")
    

        
        
