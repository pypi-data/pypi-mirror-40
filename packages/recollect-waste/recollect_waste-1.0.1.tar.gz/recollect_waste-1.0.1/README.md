[![PyPI version](https://badge.fury.io/py/recollect-waste.svg)](https://badge.fury.io/py/recollect-waste)

# python-recollect-waste
Python 3 API for Recollect Waste to obtain curbside collection information.

## Prerequisites

Find your place_id and service_id:
1. In Chrome open developer tools and go to network tab.
2. Go to your city's Recollect collection calendar.
3. Search for and select your address in the UI.
4. Watch for a request that looks like

   `https://api.recollect.net/api/places/(place_id)/services/(service_id)/events?nomerge ...`

5. Use the place_id and service_id when instantiating a new RecollectWasteClient.

## Install
`pip install recollect-waste`

## Usage
```python
from datetime import date
import recollect_waste

# Instantiate client using your place identifier
client = recollect_waste.RecollectWasteClient("place_id","service_id")

# Get the next pickup event
pickup_event = client.get_next_pickup()

# Get pickup events between two dates
pickup_events = client.get_pickup_events(datetime.date(2019, 1, 1),datetime.date(2019, 2, 1))
```

## Development

### Lint and Test

`tox`

### Create sdist
`python setup.py sdist`

# Disclaimer
Not affiliated with Recollect Waste.