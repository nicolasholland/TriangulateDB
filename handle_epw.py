"""
Handle epw
----------

This is a script used to read data from .epw files and write them into the db.

For example we add a few timeseries to the db:

python handle_epw.py VNM_HANOI_HadCM3-A2-2050.epw 21.26347411413358 105.63912300232661
python handle_epw.py THA_BANGKOK_HadCM3-A2-2050.epw 13.86223610846692 100.45250147564053
python handle_epw.py NPL_KATHMANDU_INTL_ARPT_HadCM3-A2-2050.epw 27.73259182798238 85.32597539879666
python handle_epw.py BGD_RANGPUR_HadCM3-A2-2050.epw 25.75163995669843 89.26101291512217
"""
import sys
import pandas as pd

import handle_db

def read_epwfile(epwfile):
    """
    Read epwfile into dataframe

    #TODO add check if file is in this format
    """
    skiprows = fine_first_line(epwfile)
    df = pd.read_csv(epwfile, sep=",", skiprows=skiprows, header=None)
    df = df.rename(columns={
        0: 'Year', 1: 'Month', 2: 'Day', 3: 'Hour', 4: 'Minute'
    })
    df['Datetime'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour', 'Minute']])
    df = df.set_index('Datetime')

    #TODO complete list
    df = df.rename(columns={
        6 : "Dry Bulb Temperature",
        7: "Dew Point Temperature",
        8 : "Relative Humidity [%]",
        9 : "Wind Speed [m/s]",
        10 : "Wind Direction [°]",
        11: "Global Horizontal Radiation"
    })

    return df

def fine_first_line(csv_file_path):
    line_number = None
    with open(csv_file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            if line.startswith('2050'):
                line_number = line_num
                break
    if line_number is not None:
        return line_number  - 1
    return  0

def extract_ts(epwfile, variable = "Dry Bulb Temperature"):
    """
    Extract a timeseries from the epw file.
    #TODO make variable selectable
    """
    df = read_epwfile(epwfile)

    ts = df[variable]

    return ts


def main(epwfile, latitude, longitude):
    """
    Write epw file data into database.
    """
    ts = extract_ts(epwfile)
    dbh = handle_db.DBHandle()

    geoid = dbh.gen_uuid()
    dbh.insert_geocoord(geoid, latitude, longitude)
    dbh.insert_ts(ts, geoid)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit(f"Use with {sys.argv[0]} <epw file> <latitude> <longitude>")

    main(sys.argv[1], sys.argv[2], sys.argv[3])
