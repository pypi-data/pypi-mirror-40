import swagger_client
import maya
import os
import json
import datetime
import pandas as pd


class StravaIO():

    def __init__(self, access_token=None):
        if access_token is None:
            access_token = os.getenv('STRAVA_ACCESS_TOKEN')
        self.configuration = swagger_client.Configuration()
        self.configuration.access_token = access_token
        self._api_client = swagger_client.ApiClient(self.configuration)
        self.athletes_api = swagger_client.AthletesApi(self._api_client)
        self.activities_api = swagger_client.ActivitiesApi(self._api_client)
        self.streams_api = swagger_client.StreamsApi(self._api_client)

    def get_athlete(self):
        """Get logged in athlete
        
        Returns
        -------
        athlete: Athlete object
        """
        return Athlete(self.athletes_api.get_logged_in_athlete())

    def get_activity_by_id(self, id):
        """Get activity by ID
        
        Returns
        -------
        activity: Activity ojbect
        """
        return Activity(self.activities_api.get_activity_by_id(id))

    def get_logged_in_athlete_activities(self, after=0, list_activities=None):
        """List all activities after a given date
        
        Parameters
        ----------
        after: int, str or datetime object
            If integer, the time since epoch is assumed
            If str, the maya.parse() compatible date string is expected e.g. iso8601 or 2018-01-01 or 20180101
            If datetime, the datetime object is expected

        Returns
        -------
        list_activities: list
            List of SummaryActivity objects
        """
        if list_activities is None:
            list_activities = []
        if not isinstance(after, int):
            after = maya.parse(after)
            after = after.epoch
        _fetched = self.activities_api.get_logged_in_athlete_activities(after=after)
        if len(_fetched) > 0:
            print(f"Fetched {len(_fetched)}, the latests is on {_fetched[-1].start_date}")
            list_activities.extend(_fetched)
            if len(_fetched) == 30:
                last_after = list_activities[-1].start_date
                return self.get_logged_in_athlete_activities(after=last_after, list_activities=list_activities)
        else:
            print("empty list")
        return list_activities

    def get_activity_streams(self, id, athlete_id=None):
        """Get activity streams by ID
        
        Parameters
        ----------
        id: int
            activity_id
        athlete_id: int (optional, default=None)
            athlete_id, if None, the value will be fetched frome the ActivitiesApi

        Returns
        -------
        streams: Streams ojbect
        """
        keys = ['time', 'distance', 'latlng', 'altitude', 'velocity_smooth',
        'heartrate', 'cadence', 'watts', 'temp', 'moving', 'grade_smooth']
        return Streams(self.streams_api.get_activity_streams(id, keys, key_by_type=True), id, athlete_id)


class Athlete():

    def __init__(self, api_response):
        """
        Parameters
        ----------
        api_response: swagger_client.get...() object
            e.g. athletes_api.get_logged_in_athlete()
        """
        self.api_response = api_response

    def to_dict(self):
        _dict = self.api_response.to_dict()
        _dict = convert_datetime_to_iso8601(_dict)
        return _dict

    def store_locally(self):
        strava_dir = mkdir_stravadata()
        f_name = f"athlete_{self.api_response.id}.json"
        with open(os.path.join(strava_dir, f_name), 'w') as fp:
            json.dump(self.to_dict(), fp)


class Activity():

    def __init__(self, api_response, client=None):
        self.api_response = api_response
        self.athlete_id = self.api_response.athlete.id
        self.id = self.api_response.id
        if client:
            self.streams_api = client.streams_api
        else:
            client = None

    def to_dict(self):
        _dict = self.api_response.to_dict()
        _dict = convert_datetime_to_iso8601(_dict)
        return _dict

    def store_locally(self):
        strava_dir = mkdir_stravadata()
        athlete_id = self.api_response.athlete.id
        activities_dir = os.path.join(strava_dir, f"activities_{athlete_id}")
        if not os.path.exists(activities_dir):
            os.mkdir(activities_dir)
        f_name = f"activity_{self.api_response.id}.json"
        with open(os.path.join(activities_dir, f_name), 'w') as fp:
            json.dump(self.to_dict(), fp)



class Streams():

    def __init__(self, api_response, activity_id, athlete_id = None):
        self.api_response = api_response
        self.activity_id = activity_id
        if athlete_id is None:
            client = StravaIO()
            _activity = client.get_activity_by_id(activity_id)
            self.athlete_id = _activity.athlete_id
        else:
            self.athlete_id = athlete_id

    def to_dict(self):
        _dict = self.api_response.to_dict()
        r = {}
        for k, v in _dict.items():
            r.update({k: v['data']})
        if r.get('latlng', None):
            latlng = r.pop('latlng')
            _r = list(zip(*latlng))
            r.update({'lat': list(_r[0])})
            r.update({'lng': list(_r[1])}) 
        return r

    def store_locally(self):
        _df = pd.DataFrame(self.to_dict())
        strava_dir = mkdir_stravadata()
        streams_dir = os.path.join(strava_dir, f"streams_{self.athlete_id}")
        if not os.path.exists(streams_dir):
            os.mkdir(streams_dir)
        f_name = f"streams_{self.activity_id}.parquet"
        _df.to_parquet(os.path.join(streams_dir, f_name))


def convert_datetime_to_iso8601(d):
    for k, v in d.items():
        if isinstance(v, dict):
            convert_datetime_to_iso8601(v)
        elif isinstance(v, list):
            for i in v:
                if isinstance(i, dict):
                    convert_datetime_to_iso8601(i)
        else:
            if isinstance(v, datetime.datetime):
                d[k] = maya.parse(v).iso8601()
    return d


def mkdir_stravadata():
    home_dir = os.path.expanduser('~')
    strava_dir = os.path.join(home_dir, '.stravadata')
    if not os.path.exists(strava_dir):
        os.mkdir(strava_dir)
    return strava_dir