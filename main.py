import os
from dotenv import load_dotenv
from twilio.rest import Client
import datetime
import csv

if __name__ == '__main__':
    load_dotenv()

    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

    rooms = client.video.v1.rooms.list(
        status="completed",
        date_created_after=datetime.date(2022,8,1).strftime('%Y-%m-%dT%H:%M:%SZ'), # yyyy-MM-dd'T'HH:mm:ss'Z'
        date_created_before=datetime.date(2023,1,1).strftime('%Y-%m-%dT%H:%M:%SZ')
    )

    results = []

    for room in rooms:
        participants = client.video.v1 \
            .rooms(room.sid) \
            .participants \
            .list()

        if len(participants) < 2:
            total_time = 0
        else:
            sorted_participants_start_time = sorted(participants, key=lambda x: x.start_time)
            second_participant_to_connect = sorted_participants_start_time[1].start_time
            sorted_participants_end_time = sorted(participants, key=lambda x: x.end_time, reverse=True)
            second_to_last_participant_left = sorted_participants_end_time[1].end_time
            total_time = (second_to_last_participant_left - second_participant_to_connect).total_seconds()

        results.append([room.sid, room.unique_name, len(participants), total_time])

    filename = "rooms.csv"
    fields = ['Room sid', 'Room unique name', 'Max participants', 'Duration (s)']
    with open(filename, "w") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(results)
