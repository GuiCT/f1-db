import configparser
import mariadb

cfg_parser = configparser.ConfigParser()
with open('database.config', 'r') as config_file:
    cfg_parser.read_file(config_file)
    host = cfg_parser.get('database', 'host')
    port = cfg_parser.get('database', 'port')
    user = cfg_parser.get('database', 'user')
    password = cfg_parser.get('database', 'password')
    name = cfg_parser.get('database', 'name')

# Connect to an existing database
conn = mariadb.connect(
    host=host,
    port=int(port),
    user=user,
    password=password,
    database=name
)

cur = conn.cursor()

# Create table drivers
cur.execute("""
CREATE TABLE IF NOT EXISTS drivers (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    birthday DATE NOT NULL,
    nationality VARCHAR(255) NOT NULL
    )""")

# Create table circuis
cur.execute("""
CREATE TABLE IF NOT EXISTS circuits (
    id INT PRIMARY KEY,
    name VARCHAR(300) NOT NULL,
    location VARCHAR(300) NOT NULL,
    country VARCHAR(300) NOT NULL
    )""")

# Create table races
cur.execute("""
CREATE TABLE IF NOT EXISTS races (
    id INT PRIMARY KEY,
    year INT NOT NULL,
    round INT NOT NULL,
    circuit_id INT NOT NULL,
    FOREIGN KEY (circuit_id) REFERENCES circuits(id)
    )""")

# Create table lap_times
cur.execute("""
CREATE TABLE IF NOT EXISTS lap_times (
    race_id INT NOT NULL,
    driver_id INT NOT NULL,
    lap INT NOT NULL,
    milliseconds INT NOT NULL,
    PRIMARY KEY (race_id, driver_id, lap),
    FOREIGN KEY (race_id) REFERENCES races(id),
    FOREIGN KEY (driver_id) REFERENCES drivers(id)
    )""")
