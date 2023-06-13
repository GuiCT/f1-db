import configparser
import mariadb
import pandas as pd
from tqdm import tqdm

cfg_parser = configparser.ConfigParser()
with open('database.config', 'r') as config_file:
    cfg_parser.read_file(config_file)
    host = cfg_parser.get('database', 'host')
    port = cfg_parser.get('database', 'port')
    user = cfg_parser.get('database', 'user')
    password = cfg_parser.get('database', 'password')
    name = cfg_parser.get('database', 'name')

conn = mariadb.connect(
    host=host,
    port=int(port),
    user=user,
    password=password,
    database=name
)
cur = conn.cursor()

# DRIVERS
drivers = pd.read_csv("data/drivers.csv")
for index, row in drivers.iterrows():
    cur.execute(
        "INSERT INTO drivers(id, name, surname, birthday, nationality) VALUES (?, ?, ?, ?, ?)",
        [row['driverId'], row['forename'], row['surname'], row['dob'], row['nationality']]
    )

# CIRCUITS
circuits = pd.read_csv("data/circuits.csv")
for index, row in circuits.iterrows():
    cur.execute(
        "INSERT INTO circuits(id, name, location, country) VALUES (?, ?, ?, ?)",
        [row['circuitId'], row['name'], row['location'], row['country']]
    )

# RACES
races = pd.read_csv("data/races.csv")
for index, row in races.iterrows():
    cur.execute(
        "INSERT INTO races(id, year, round, circuit_id) VALUES (?, ?, ?, ?)",
        [row['raceId'], row['year'], row['round'], row['circuitId']]
    )

# LAP_TIMES
lap_times = pd.read_csv("data/lap_times.csv")
# Use tqdm to show progress bar
for index, row in tqdm(lap_times.iterrows(), total=lap_times.shape[0]):
    cur.execute(
        "INSERT INTO lap_times(race_id, driver_id, lap, milliseconds) VALUES (?, ?, ?, ?)",
        [row['raceId'], row['driverId'], row['lap'], row['milliseconds']]
    )


conn.commit()