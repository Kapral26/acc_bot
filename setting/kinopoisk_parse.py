# -*- coding: utf-8 -*-

"""Поиск фильмов с сайта КиноПоиск"""

import requests

class Searchbykeyword:
    """Класс для поиска по ключевому слову"""
    def __init__(self, query: str=None, searchapikey: str=None, page: int=None):
        self.query = query
        self.page = page
        self.searchapikey = searchapikey
        self.acception = {
            "accept": "application/json",
            "X-API-KEY": self.searchapikey
        }

    def searchbykeyword(self):
        """
        Ищем по ключевому слову
        :return: словарь фильмов
        """
        if self.page == None:
            self.page = 1
        else:
            self.page

        if self.query == None:
            raise Exception("Query is not defined!")
        elif self.query:
            self.query

        searchbykeyword = requests.get(f"https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={self.query}&page={self.page}", headers=self.acception)
        return searchbykeyword

class Searchbyid:
    def __init__(self, filmid: int=None, searchapikey: str=None):
        self.filmid = filmid
        self.searchapikey = searchapikey
        self.acception = {
            "accept": "application/json",
            "X-API-KEY": self.searchapikey
        }

    def searchbyid(self):
        searchbyid = requests.get(f"https://kinopoiskapiunofficial.tech/api/v2.1/films/{self.filmid}", headers=self.acception)
        return searchbyid

class Searchdatabyid:
    def __init__(self, filmid: int=None, searchapikey: str=None):
        self.filmid = filmid
        self.searchapikey = searchapikey
        self.acception = {
            "accept": "application/json",
            "X-API-KEY": self.searchapikey
        }

        searchbyid = requests.get(f"https://kinopoiskapiunofficial.tech/api/v2.1/films/{self.filmid}", headers=self.acception)
        searchbyid = searchbyid.json()

        self.filmTitleru = searchbyid['data']['nameRu']
        self.filmTitleen = searchbyid['data']['nameEn']
        self.filmMainurlru = searchbyid['data']['webUrl']
        self.filmMainurlen = searchbyid['data']['webUrl']
        self.posterUrl = searchbyid['data']['posterUrl']
        self.posterUrlPreview = searchbyid['data']['posterUrlPreview']
        self.year = searchbyid['data']['year']
        self.filmLength = searchbyid['data']['filmLength']
        self.slogan = searchbyid['data']['slogan']
        self.description = searchbyid['data']['description']
        self.types = searchbyid['data']['type']
        self.ratingMpaa = searchbyid['data']['ratingMpaa']
        self.ratingAgeLimits = searchbyid['data']['ratingAgeLimits']
        self.premiereRu = searchbyid['data']['premiereRu']
        self.distributors = searchbyid['data']['distributors']
        self.premiereWorld = searchbyid['data']['premiereWorld']
        self.premiereDigital = searchbyid['data']['premiereDigital']
        self.premiereWorldCountry = searchbyid['data']['premiereWorldCountry']
        self.premiereDvd = searchbyid['data']['premiereDvd']
        self.premiereBluRay = searchbyid['data']['premiereBluRay']
        self.distributorRelease = searchbyid['data']['distributorRelease']
        self.countries = searchbyid['data']['countries'][0]['country']
        def genres():
            genres = list()
            for i in searchbyid['data']['genres']:
                genres.append(i['genre'])
            return genres
        self.genres = genres()
        self.facts = searchbyid['data']['facts']
