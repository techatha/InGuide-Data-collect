from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import csv

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


# /data?_acc=x,y,z&_acc_g=x,y,z&_gyro=x,y,z&_vel=n
@app.route('/data')
def write_data_to_csv_file():
    gps_timestamp = request.args.get("_gps_timestamp", "")
    imu_timestamp = request.args.get("_imu_timestamp", "")
    client_timestamp = request.args.get("_timestamp", "")

    acc_data_xyz = request.args.get("_acc", "")
    acc_data_gxyz = request.args.get("_acc_g", "")
    gyro_data_xyz = request.args.get("_gyro", "")
    gps_velocity = float(request.args.get("_vel", ""))
    gps_lat = float(request.args.get("_lat", ""))
    gps_lon = float(request.args.get("_lon", ""))
    action = request.args.get("_action", "")

    acc_data_xyz = [float(x) for x in acc_data_xyz.split(',')]
    acc_data_gxyz = [float(x) for x in acc_data_gxyz.split(',')]
    gyro_data_xyz = [float(x) for x in gyro_data_xyz.split(',')]

    filename = 'raw_data/imu-data.csv'
    is_csv_exist = os.path.exists(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not is_csv_exist:
            writer.writerow(['timestamp', 'time-imu', 'time-gps', 'acc-x', 'acc_y', 'acc_z', 'acc_gx', 'acc_gy',
                             'acc_gz', 'gyro_x', 'gyro_y', 'gyro_z', 'gps_lat', 'gps_lon', 'gps_velocity', 'action'])
        writer.writerow([client_timestamp, imu_timestamp, gps_timestamp, acc_data_xyz[0], acc_data_xyz[1],
                         acc_data_xyz[2], acc_data_gxyz[0], acc_data_gxyz[1], acc_data_gxyz[2], gyro_data_xyz[0],
                         gyro_data_xyz[1], gyro_data_xyz[2], gps_lat, gps_lon, gps_velocity, action])

    return jsonify({"status": "success"}), 200


if __name__ == '__main__':
    app.run(ssl_context='adhoc')
