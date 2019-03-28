import csv
import time

import serial

import aislib


def decode_file_example():
    """
    Example for decoding a file
    :return:
    """
    # "C:\Users\root\Desktop\feed.ais.txt"
    # with open("ais.exploratorium.edu", "r") as file:

    with open(r"ships20190328-095513.csv", "r") as file:
        ser = serial.Serial("COM9", 38400)
        csv_dict = csv.DictReader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for aline in csv_dict:
            lat_deg = int(float(aline['ship_lat']))
            lon_deg = int(float(aline['ship_lon']))
            lat_min = (float(aline['ship_lat']) - lat_deg) * 60
            lon_min = (float(aline['ship_lon']) - lon_deg) * 60
            aismsg = aislib.AISPositionReportMessage(
                mmsi=int(aline['mmsi']),
                status=int(aline['status']),
                sog=int(float(aline['speed']) * 10),
                pa=1,
                lon=long((lon_deg * 60 + lon_min) * 10000),
                lat=long((lat_deg * 60 + lat_min) * 10000),
                cog=int(aline['course']) * 10,
                comm_state=82419
            )
            ais = aislib.AIS(aismsg)
            payload = ais.build_payload(False)
            print(payload)
            ser.write(payload + "\n\r")
            imo = 0 if aline['imo'] == '' else int(aline['imo'])
            aismsg = aislib.AISStaticAndVoyageReportMessage(
                mmsi=int(aline['mmsi']),
                imo=imo,
                shipname=aline['shipname'],
                epfd=1,
                draught=0,
                destination=0,
            )
            ais = aislib.AIS(aismsg)
            payload = ais.build_payload(False)
            print(payload)
            ser.write(payload + "\n\r")
            # time.sleep(1)


decode_file_example()
