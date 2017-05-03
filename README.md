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

###Using the search functionality:
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
