"""Recollect Waste"""
from datetime import datetime
from datetime import date
from datetime import timedelta
import json
import requests

API_URL = 'https://api.recollect.net/api/places/{}/services/{}/events?after={}&before={}'


class PickupEvent:  # pylint: disable=too-few-public-methods
    """Represents a pickup event"""
    def __init__(self, event_date):
        self.event_date = event_date
        self.pickup_types = []
        self.area_name = None


class RecollectWasteClient():
    """The Recollect client"""
    def __init__(self, place_id, service_id):
        self.place_id = place_id
        self.service_id = service_id

    def get_next_pickup(self):
        """Get the next pickup using today's date"""
        todays_date = datetime.today()
        events = self.get_pickup_events(todays_date, todays_date + timedelta(weeks=4))
        return events[0] if events.__sizeof__() > 0 else None

    def get_pickup_events(self, start_date, end_date):
        """Get the pickups from the recollect waste website"""
        session = requests.session()
        request_url = API_URL.format(self.place_id, self.service_id, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        resp = session.get(request_url)
        json_object = json.loads(resp.text)

        # Get all the events and their flags
        pickup_events = []
        for event in json_object['events']:
            # Some times there are events without a flags key
            if 'flags' not in event.keys():
                continue

            event_date = datetime.strptime(event['day'], '%Y-%m-%d').date()
            pickup_event = PickupEvent(event_date)
            pickup_events.append(pickup_event)

            for flag in event['flags']:
                # We only want pickup event types
                if flag['event_type'] == 'pickup':
                    pickup_event.pickup_types.append(flag['name'])
                    pickup_event.area_name = flag['area_name']

        return pickup_events
