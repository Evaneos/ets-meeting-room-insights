import os, re, datetime, csv, itertools
import sys
from dotenv import load_dotenv
from twilio.rest import Client
from progress.bar import ChargingBar

def overlapping_time(participants):
    sorted_participant = sorted(participants, key=lambda x: x.start_time)
    overlap = 0
    for p1, p2 in itertools.combinations(sorted_participant, 2):
        start = max(p1.start_time, p2.start_time)
        end = min(p1.end_time, p2.end_time)
        if start < end:
            overlap += (end - start).total_seconds()
    return overlap

if __name__ == '__main__':
    load_dotenv()
    
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

    rooms = client.video.v1.rooms.list(
        status="completed",
        date_created_after=datetime.date(2022,10,12).strftime('%Y-%m-%dT%H:%M:%SZ'), # yyyy-MM-dd'T'HH:mm:ss'Z'
        date_created_before=datetime.date.today().strftime('%Y-%m-%dT%H:%M:%SZ')
    )

    results = []
    bar = ChargingBar('Fetching', max=len(rooms))
    
    for room in rooms:
        participants = client.video.v1 \
            .rooms(room.sid) \
            .participants \
            .list()

        if re.match(r'.*@\d+', room.unique_name) == None:
            bar.next()
            continue

        request_id = room.unique_name.split('@')[1]
        destination_name = room.unique_name.split('@')[0]
            
        if len(participants) < 2:
            bar.next()
            continue
        
        total_time = int(overlapping_time(participants))
         
        results.append([
            room.sid, 
            room.unique_name, 
            room.date_updated,
            request_id,
            destination_name,
            len(participants), 
            total_time
        ])
        
        bar.next()
    bar.finish()
    
    filename = "rooms.csv"
    fields = ['Room sid', 'Room unique name', 'Room created at', 'Request ID', 'Destination', 'Max participants', 'Duration (s)']
    with open(filename, "w") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(results)

    with open(filename, 'r') as f:
        for line in f:
            sys.stderr.write(line)
