"""
Set of filters for filtering the outputted data from datapoint.
"""
from datetime import datetime, timedelta


class BaseFilter(object):
    """
    Base filter that contains the underlying methods required.
    """
    def __init__(self, datapoint_request):
        self.name = "BaseFilter"
        self.request = datapoint_request

    def __str__(self):
        return self.name

    def __getitem__(self, param):
        return self.get_all_values(param)

    @property
    def times(self):
        """
        Return all timesteps as a list of datetime objects.
        """
        return self.get_all_times()

    def get_date(self):
        """
        Return a datetime object for today (based on data date).
        """
        datestr = self.request.json['SiteRep']['DV']['dataDate']
        return datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%SZ")

    def get_all_times(self):
        """
        Return all timesteps as a list of datetime objects.
        """
        times = []

        for day in self.request.json["SiteRep"]["DV"]["Location"]["Period"]:
            day_value = datetime.strptime(day['value'], "%Y-%m-%dZ")
            for timestep in day["Rep"]:
                time_value = timedelta(minutes=int(timestep["$"]))
                times.append(day_value + time_value)

        return times

    def get_all_values(self, param):
        """
        Return all values for specified parameter as a list.
        """
        values = []

        for day in self.request.json["SiteRep"]["DV"]["Location"]["Period"]:
            for timestep in day["Rep"]:
                values.append(timestep[param])

        return values


class FilterAll(BaseFilter):
    """
    A filter that returns all values.
    """

    def __init__(self, datapoint_request):
        BaseFilter.__init__(self, datapoint_request)
        self.name = "All"


class FilterToday(BaseFilter):
    """
    A filter that returns only today's values.
    """

    def __init__(self, datapoint_request):
        BaseFilter.__init__(self, datapoint_request)
        self.name = "Today"

    def get_all_times(self):

        all_times = BaseFilter.get_all_times(self)

        data_date_str = self.request.json["SiteRep"]["DV"]["dataDate"]
        data_date = datetime.strptime(data_date_str, "%Y-%m-%dT%H:%M:%SZ")

        today_times = []

        for time in all_times:
            if time.date() == data_date.date():
                today_times.append(time)

        return today_times

    def get_all_values(self, param):

        all_values = BaseFilter.get_all_values(self, param)
        all_times = BaseFilter.get_all_times(self)

        data_date_str = self.request.json["SiteRep"]["DV"]["dataDate"]
        data_date = datetime.strptime(data_date_str, "%Y-%m-%dT%H:%M:%SZ")

        today_values = []

        for (time, value) in zip(all_times, all_values):
            if time.date() == data_date.date():
                today_values.append(value)

        return today_values


class FilterTomorrow(BaseFilter):
    """
    A filter that returns only tomorrow's values.
    """

    def __init__(self, datapoint_request):
        BaseFilter.__init__(self, datapoint_request)
        self.name = "Tomorrow"

    def get_all_times(self):

        all_times = BaseFilter.get_all_times(self)

        data_date_str = self.request.json["SiteRep"]["DV"]["dataDate"]
        data_date = datetime.strptime(data_date_str, "%Y-%m-%dT%H:%M:%SZ")

        today_times = []

        for time in all_times:
            if time.date() == data_date.date() + timedelta(days=1):
                today_times.append(time)

        return today_times

    def get_all_values(self, param):

        all_values = BaseFilter.get_all_values(self, param)
        all_times = BaseFilter.get_all_times(self)

        data_date_str = self.request.json["SiteRep"]["DV"]["dataDate"]
        data_date = datetime.strptime(data_date_str, "%Y-%m-%dT%H:%M:%SZ")

        today_values = []

        for (time, value) in zip(all_times, all_values):
            if time.date() == data_date.date() + timedelta(days=1):
                today_values.append(value)

        return today_values


class FilterNext24(BaseFilter):
    """
    A filter that returns the next 24 hours' data.
    """

    def __init__(self, datapoint_request):
        BaseFilter.__init__(self, datapoint_request)
        self.name = "Next 24 Hours"

    def get_all_times(self):

        all_times = BaseFilter.get_all_times(self)

        time_0 = datetime.now()
        time_24 = time_0 + timedelta(hours=24)

        out_times = []
        for time in all_times:
            if time >= time_0 and time <= time_24:
                out_times.append(time)

        return out_times

    def get_all_values(self, param):

        all_values = BaseFilter.get_all_values(self, param)
        all_times = BaseFilter.get_all_times(self)

        time_0 = datetime.now()
        time_24 = time_0 + timedelta(hours=24)

        out_values = []
        for (time, value) in zip(all_times, all_values):
            if time >= time_0 and time <= time_24:
                out_values.append(value)

        return out_values
