import zipfile
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
        self.column_to_index = {'magic':0, 'status':1, 'time_us':2, 'main_voltage_v':3, 'pyro_voltage_v':4, 'numSatellites':5, 'gpsFixType':6, 'latitude_degrees':7, 
    'longitude_degrees':8, 'gps_hMSL_m':9, 'barometer_hMSL_m':10, 'temperature_c':11, 'acceleration_x_mss':12, 'acceleration_y_mss':13, 'acceleration_z_mss':14, 
    'angular_velocity_x_rads':15, 'angular_velocity_y_rads':16, 'angular_velocity_z_rads':17, 'gauss_x':18, 'gauss_y':19, 'gauss_z':20, 
    'kf_acceleration_mss':21, 'kf_velocity_ms':22, 'kf_position_m':23, 'w':24, 'x':25, 'y':26, 'z':27, 'checksum':28}

    def update_column_to_index(self,updated):
        self.column_to_index = updated
    
    def update_board_version(self,board_version):
        self.board_version = board_version
    
    def update_launch_data(self, launch_date):
        self.launch_date = launch_date
    
    def from_np(self,file_path,launch_date = None, board_version = None, packet_data= True):
        self.launch_date = launch_date if launch_date is not None else print("Warning. No launch date provided.")
        self.board_version = board_version if board_version is not None else print("Warning. No board version provided.")
        if packet_data:
            self.packet_data = np.load(file_path)
        else:
            self.state_data = np.load(file_path)
    


    def from_zip(self, file_path, launch_date=None, board_version=None, csv=False):
    
        self.launch_date = launch_date if launch_date is not None else print("Warning. No launch date provided.")
        self.board_version = board_version if board_version is not None else print("Warning. No board version provided.")

        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                packet_file = "packet_data.csv" if csv else "packet_data.npy"
                state_file = "state_data.csv" if csv else "state_data.npy"
                if packet_file in file_list:
                    with zip_ref.open(packet_file) as data_file:
                        if csv:
                            self.packet_data = np.loadtxt(data_file, delimiter=',', skiprows=1)  
                        else:
                            self.packet_data = np.load(data_file)  
                else:
                    raise FileNotFoundError(f"Error: '{packet_file}' is missing in the ZIP file.")
                # Check and load 'state_data'
                if state_file in file_list:
                    with zip_ref.open(state_file) as data_file:
                        if csv:
                            self.state_data = np.loadtxt(data_file, delimiter=',', skiprows=1)  
                        else:
                            self.state_data = np.load(data_file)  
                else:
                    raise FileNotFoundError(f"Error: '{state_file}' is missing in the ZIP file.")
                # Check and load '.config' file 
                config_file_name = next((f for f in file_list if f.endswith('.config')), None)
                if config_file_name:
                    with zip_ref.open(config_file_name) as config_file:
                        self.config = config_file.read().decode('utf-8')  
                else:
                    raise FileNotFoundError("Error: '.config' file is missing in the ZIP file.")

        except zipfile.BadZipFile:
            print("Error: The provided file is not a valid ZIP file.")
        except FileNotFoundError as e:
            print(e)


        
    def plot_column(self, column_name, title=None, start=None, end=None):
        # Check if packet_data is loaded
        if self.packet_data is None:
            print("No data loaded.")
            return
        # Check if the column name exists
        if column_name not in self.column_to_index:
            print(f"Column: '{column_name}' not found in data.")
            return
        # Obtaine the index and intialize start and end plotting index if not specified 
        index = self.column_to_index[column_name]
        if start is None:
            start = 0
        if end is None:
            end = self.packet_data.shape[0]  
        # Obtain indexed data
        column_data = self.packet_data[start:end, index]

        plt.plot(range(start, end), column_data, label=column_name)
        plt.title(title or f"{column_name} over Time")
        plt.xlabel("Index")
        plt.ylabel(column_name)
        plt.legend()
        plt.grid(True)  # Add grid for better visualization

    def display_metadata(self):
        print(f"Launch Date: {self.launch_date}")
        print(f"Board Version: {self.board_version}")
