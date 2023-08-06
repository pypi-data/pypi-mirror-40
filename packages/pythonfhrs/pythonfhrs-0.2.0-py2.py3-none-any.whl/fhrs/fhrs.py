import pandas as pd
import requests


class Client(object):
    """
    A class which creates the requests session object to request data from FHRS api.


    Attributes
    ----------

    session : requests.Session()
        a session object which persists to call the fhrs api endpoints.
    url_base : str
        the path to the fhrs api domain
    headers : dict()
        the headers to be used in the requests session

    """

    def __init__(self):

        self.session = requests.Session()
        self.url_base = 'http://api.ratings.food.gov.uk/'
        self.headers = {'x-api-version': '2', 'accept': 'application/json'}

    def getregions(self):
        """Returns a dataframe containing details for all regions in the UK.

        """
        region = self.session.get(self.url_base + 'Regions/', headers=self.headers)
        region = pd.DataFrame.from_dict(region.json()['regions'])
        return region

    def getregionbyid(self, _id):
        """Returns a dataframe conatining details for a region specified by parameter _id.

           Parameters
           ----------
             _id : int
                The id for a region for which details are needed.
        """
        region = self.session.get(self.url_base + 'Regions/' + str(_id), headers=self.headers)
        region = pd.DataFrame.from_dict(region.json())
        return region

    def getregionsbasic(self):
        """Returns a dataframe containing basic details of all the regions in the UK.
        """
        region = self.session.get(self.url_base + 'Regions/basic', headers=self.headers)
        region = pd.DataFrame.from_dict(region.json()['regions'])
        return region

    def getauthorities(self):
        """Returns a dataframe of details about all the authorities in the UK.
        """
        auth = self.session.get(self.url_base + 'Authorities/', headers=self.headers)
        auth = pd.DataFrame.from_dict(auth.json()['authorities'])
        return auth

    def getauthoritiesbasic(self):
        """Returns a dataframe of basic details about all the authorities in the UK.
        """
        auth = self.session.get(self.url_base + 'Authorities/basic', headers=self.headers)
        auth = pd.DataFrame.from_dict(auth.json()['authorities'])
        return auth

    def getauthoritybyid(self, _id):
        """Returns a dataframe of details about a single authority selected by `_id`.

           Parameters
           ----------
              _id : int
                The id of the authority for which details are needed.
        """
        auth = self.session.get(self.url_base + 'Authorities/' + str(_id), headers=self.headers)
        auth = pd.DataFrame.from_dict(auth.json())
        return auth

    def getbusinesstypes(self):
        """Return a dataframe of details about all business types.
        """
        business = self.session.get(self.url_base + 'BusinessTypes', headers=self.headers)
        business = pd.DataFrame.from_dict(business.json()['businessTypes'])
        return business

    def getbusinesstypesbasic(self):
        """Return a dataframe containing basic information about all business types.
        """
        business = self.session.get(self.url_base + 'BusinessTypes/basic', headers=self.headers)
        business = pd.DataFrame.from_dict(business.json()['businessTypes'])
        return business

    def getbusinesstypebyid(self, _id):
        """Return a dataframe containing details about a single business indexed by its `_id`

           Parameters
           ----------
              _id : int
                 The id of the business whose details are required.
        """
        business = self.session.get(self.url_base + 'BusinessTypes/' + str(_id), headers=self.headers)
        business = pd.DataFrame.from_dict(business.json())
        return business

    def getcountries(self):
        """Returna a dataframe of details about all the countries in the UK.
        """
        countries = self.session.get(self.url_base + 'Countries', headers=self.headers)
        countries = pd.DataFrame.from_dict(countries.json()['countries'])
        return countries

    def getcountrybyid(self, _id):
        """Returns a dataframe about the details for a single country indexed by its `_id`.

           Parameters
           ----------
             _id : int
               The id of the country whose details are required.
        """
        countries = self.session.get(self.url_base + 'Countries/' + str(_id), headers=self.headers)
        countries = pd.DataFrame.from_dict(countries.json())
        return countries

    def getcountriesbasic(self):
        """Returns a dataframe containing basic information about all the countries in the UK.
        """
        countries = self.session.get(self.url_base + 'Countries/basic', headers=self.headers)
        countries = pd.DataFrame.from_dict(countries.json()['countries'])
        return countries

    def getestablishmentsbyid(self, _id):
        """Returns a dataframe containing details for a single establishment indexed by its `_id`.

           Parameters
           ----------
              _id : int
                 The id of the establishment for which details are requested.
        """
        establishment = self.session.get(self.url_base + 'Establishments/' + str(_id), headers=self.headers)
        return establishment.json()

    def getschemetypes(self):
        """Returns a dataframe containing details of all the schemes.
        """
        schemetypes = self.session.get(self.url_base + 'SchemeTypes', headers=self.headers)
        schemetypes = pd.DataFrame.from_dict(schemetypes.json()['schemeTypes'])
        return schemetypes

    def getsortoptions(self):
        """Returns a dataframe containing details of all the sort options.
        """
        options = self.session.get(self.url_base + 'SortOptions', headers=self.headers)
        options = pd.DataFrame.from_dict(options.json()['sortOptions'])
        return options

    def getscoredescriptorbyid(self, _id):
        """Returns a dataframe containing details of scores for an establishment by `_id`

           Parameters
           ----------
              _id : int
                 The id for the establishement for which the scores are requested.
        """
        scoredescriptor = self.session.get(self.url_base + 'ScoreDescriptors?establishmentId=' + str(_id),
                                           headers=self.headers)
        scoredescriptor = pd.DataFrame.from_dict(scoredescriptor.json()['scoreDescriptors'])
        return scoredescriptor

    def getratings(self):
        """Returns a dataframe containing details of all ratings.
        """
        ratings = self.session.get(self.url_base + 'Ratings', headers=self.headers)
        ratings = pd.DataFrame.from_dict(ratings.json()['ratings'])
        return ratings

    def getratingsoperators(self):
        """Return a dataframe containing details of all rating operators.
        """
        ratingoperator = self.session.get(self.url_base + 'RatingOperators', headers=self.headers)
        ratingoperator = pd.DataFrame.from_dict(ratingoperator.json()['ratingOperator'])
        return ratingoperator
