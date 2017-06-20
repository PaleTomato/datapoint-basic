# datapoint-basic
A Python module that provides a simplified way of using some parts of the
datapoint-python module.

__Disclaimer: This module is in no way part of the DataPoint project/service.
No support for this module is provided by the Met Office and may break as the
DataPoint service grows/evolves.__

## Features
* Search functionality for identifying forecast sites
* Simplified functionality to obtain current weather conditions
* Uses site names as inputs to most functions/methods

## Example Usage
Note that you will require a DataPoint API key in order to make use of this
module
### Using the search functionality:
The following example uses the search functionality to find all sites beginning
with "exe." The functionality, like all others in this module, is designed to
be case-insensitive.

```Python
import datapointbasic
api_key = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"

# Create search object
search = datapointbasic.placesearch(api_key)

# Find all places beginning with "exe"
places = search.get_places_beginning_with("exe")

print(places)

```

Example Output:
```Python
['Exe Estuary', 'Exeter', 'Exeter Airport', ... , 'Exeter Youth Hostel']
```

### Getting a forecast
The following example shows how to get a 5 day forecast for a site, and print
the temperatures and times of the first day (day 0). The sites are accessed by
their name, so you can use the sites found with the search tools.

```Python
import datapointbasic
api_key = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
place_name = "York"

# Get the forecast for York
forecast = datapointbasic.locationforecast(place_name, api_key)
temps = forecast.day0.temperature
units = forecast.units.temperature
times = forecast.day0.timesteps

# Print the temperatures
for i in range(len(temps)):
    hours = times[i].time().isoformat(timespec="minutes")
    print("%s - %s%s" % (hours, temps[i], units))

```

Example Output:
```
00:00 - 13C
03:00 - 12C
06:00 - 12C
09:00 - 13C
12:00 - 14C
15:00 - 16C
18:00 - 16C
21:00 - 14C
```
