from flask import Flask, request, jsonify, render_template
import sqlite3

import handle_db

app = Flask(__name__)

# Endpoint to retrieve UUID mapping data
@app.route('/get_uuid_mapping_data', methods=['GET'])
def get_uuid_mapping_data():
    conn = sqlite3.connect('triangulate.db')
    cursor = conn.cursor()
    cursor.execute('SELECT uuid, latitude, longitude FROM uuid_mapping')
    uuid_mapping_data = cursor.fetchall()
    conn.close()

    response_data = []
    for row in uuid_mapping_data:
        response_data.append({
            'uuid': row[0],
            'latitude': row[1],
            'longitude': row[2]
        })

    return jsonify(response_data)

# Endpoint to retrieve time series data for a specific UUID
@app.route('/get_timeseries_data', methods=['GET'])
def get_timeseries_data():
    uuid = request.args.get('uuid')

    dbh = handle_db.DBHandle()
    timeseries_data = dbh.get_ts(uuid)

    timestamps = [str(_) for _ in timeseries_data.index]
    values = [val for val in timeseries_data[timeseries_data.columns[0]]]

    response_data = {
        'timestamps': timestamps,
        'values': values
    }

    return jsonify(response_data)

@app.route('/')
def index():
    return render_template('map_visualization.html')

if __name__ == '__main__':
    app.run(debug=True)
