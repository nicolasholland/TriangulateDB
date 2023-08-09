from flask import Flask, request, jsonify, render_template
import sqlite3

import handle_db
import triangulate

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

def df_to_dict(df):
    """ Turn db retval into dict """
    timestamps = [str(_) for _ in df.index]
    values = [val for val in df[df.columns[0]]]

    response_data = {
        'timestamps': timestamps,
        'values': values
    }
    return response_data

# Endpoint to retrieve time series data for a specific UUID
@app.route('/get_timeseries_data', methods=['GET'])
def get_timeseries_data():
    uuid = request.args.get('uuid')

    dbh = handle_db.DBHandle()
    timeseries_data = dbh.get_ts(uuid)

    response_data = df_to_dict(timeseries_data)

    return jsonify(response_data)

@app.route('/calculate', methods=['GET'])
def calculate():
    try:
        # Get the float parameters from the query string
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))

        result = triangulate.main(latitude, longitude)
        response_data = df_to_dict(result)
        return jsonify(response_data)
    except ValueError:
        return jsonify({'error': 'Invalid parameters'})

@app.route('/')
def index():
    return render_template('map_visualization.html')

if __name__ == '__main__':
    app.run(debug=True)
