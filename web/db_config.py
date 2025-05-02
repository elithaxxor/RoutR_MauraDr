import configparser
import os

# Define the path to the config file
# config_path = os.path.join(os.path.dirname(__file__), "config.ini")
config_path = os.getcwd()
config_file = config_path + "config.ini" 
print("config file is assumed to be located in ", config_file)
print("please double check after running!" ) 

# Initialize the config parser
config = configparser.ConfigParser()
config.read(config_file)

# Access configuration values
database_path = config["database"]["path"]
print(f"Database Path: {database_path}")
