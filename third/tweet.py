# -*- coding: utf-8 -*-
import model, json


class TweetLoader(object):
    FILE_PATH = '/docs/three_minutes_tweets.json'

    def __init__(self, apath, afinn):
        # Base path
        self._base_path = apath
        # AFINN module (Rating)
        self.afinn = afinn

        # Initiate cash dicts
        self.user_cash = dict()
        self.country_cash = dict()
        self.lang_cash = dict()
        self.location_cash = dict()

    def load_information(self, session):
        '''

        :param apath: str
            file name in string representation
        :param session: Session object
            New db session
        :return: list
            Errors list (Report)

        '''
        # Load classificatories from db and create local cash
        self.user_cash = self.get_users(session)
        self.country_cash = self.get_country(session)
        self.lang_cash = self.get_langs(session)

        # Read json file (per line)
        with open(self._base_path + self.FILE_PATH, 'rb') as input_file:
            for json_body in input_file:
                # Convert string to python object
                data = json.loads(json_body)
                try:
                    # Ignore trash messages
                    if u'delete' not in data.keys():
                        # Create new tweet object
                        n_tweet = model.Tweet(
                            idtweet=data[u'id'],
                            idtweetuser=self._user(data[u'user'], session),
                            idcountry=self._country(data[u'place'], session) if data[u'place'] is not None else None,
                            idlang=self._lang(data[u'lang'], session),
                            tweet_text=data[u'text'],
                            display_url=data[u'source'],
                            created_at=data[u'created_at'],
                            tweetsentiment=self.count_sentiment(data[u'text'], data[u'lang'])
                        )
                        session.add(n_tweet)
                        # Put object to db
                        session.flush()
                        session.commit()
                except Exception as error:
                    session.rollback()
                    print('Error: ' + str(error))
            session.close()
            return True

    def count_sentiment(self, text, lang):
        '''

        :param text: str
            Text from tweet
        :param lang: str
            lang from tweet
        :return: int
            Summ rating words
        '''
        rating = 0
        # AFFINN declare rating only for english words (English language is language which have in 'sname' word 'en')
        if 'en' in lang:
            # Split string
            for word in text.split(' '):
                # Check word to availability in AFINN list
                if word in self.afinn.word_collection:
                    rating += self.afinn.word_collection[word]

        return rating

    @staticmethod
    def get_country(session):
        '''

        :param session: Session object
            New session
        :return: dict
            {Primary objects from db}
        '''
        country_dict = dict()
        # Take countries from db
        for country in session.query(model.Country).all():
            country_dict[country.countrycode] = country

        return country_dict

    @staticmethod
    def get_langs(session):
        '''

        :param session: Session object
            New session
        :return: dict
            {Primary objects from db}
        '''
        lang_dict = dict()
        # Take langs from db
        for lang in session.query(model.Lang).all():
            lang_dict[lang.snamelang] = lang

        return lang_dict

    @staticmethod
    def get_users(session):
        '''

        :param session: Session object
            New session
        :return: dict
            {Primary objects from db}
        '''
        users_dict = dict()
        # Take users from db
        for user in session.query(model.Tweetuser).all():
            users_dict[user.idtweetuser] = user

        return users_dict

    def _country(self, data, session):
        '''

        :param data: dict
            python object with information
        :param session: Session object
            New db session
        :return: int
            Interested id country

        '''

        if data[u'country_code'] in self.country_cash.keys():
            # If country code in cash, take object from cash
            return self.country_cash[data[u'country_code']].idcountry
        else:
            # Check object availability in base
            country = session.query(model.Country)\
                .filter(model.Country.countrycode == data[u'country_code']).one_or_none()
            # Object not in db
            if country is None:
                # Create new Country
                n_country = model.Country(
                    countrycode=data[u'country_code']
                )
                session.add(n_country)
                session.flush()
                # Add country to cash dict
                self.country_cash[data[u'country_code']] = n_country
                return n_country.idcountry

            return country.idcountry

    def _location(self, location, session):
        '''

        :param location: str
            Location name
        :param session: Session object
            New db session
        :return: int
            Id location
        '''
        if location in self.location_cash.keys():
            # If location in cash, take object from cash
            return self.location_cash[location].idlocation
        else:
            db_location = session.query(model.Location) \
                .filter(model.Location.namelocation == location).one_or_none()
            # If location not at db, create new Location
            if db_location is None:
                n_location = model.Location(
                    namelocation=location
                )
                session.add(n_location)
                session.flush()
                # Add location to cash
                self.location_cash[location] = n_location

                return n_location.idlocation

            return db_location.idlocation

    def _user(self, data, session):
        '''

        :param data: dict
            python object with information
        :param session: Session object
            New db session
        :return: tuple(int, dict, dict)
            Interested user id, lang cash, users cash
        '''
        if data[u'id'] in self.user_cash.keys():
            # If user in cash, take object from cash
            return self.user_cash[data[u'id']].idtweetuser
        else:
            # Check object availability in base
            user = session.query(model.Tweetuser)\
                .filter(model.Tweetuser.idtweetuser == data[u'id']).one_or_none()
            # Object not in db
            if user is None:
                # Create new User
                n_user = model.Tweetuser(
                        idtweetuser=data[u'id'],
                        idlang=self._lang(data[u'lang'], session),
                        nameuser=data[u'name'],
                        idlocation=self._location(data[u'location'], session)
                    )

                session.add(n_user)
                session.flush()
                # Add user to cash
                self.user_cash[data[u'id']] = n_user

                return n_user.idtweetuser

            return user.idtweetuser

    def _lang(self, lang, session):
        '''

        :param lang: str
            Name of lang
        :param session: Session object
            New db session
        :return: tuple(int, dict)
            Id lang and lang cash
        '''
        if lang in self.lang_cash.keys():
            # If lang in cash, take object from cash
            return self.lang_cash[lang].idlang
        else:
            db_lang = session.query(model.Lang)\
                .filter(model.Lang.snamelang == lang).one_or_none()
            # If lang not at db, create new
            if db_lang is None:
                n_lang = model.Lang(
                    snamelang=lang
                )
                session.add(n_lang)
                session.flush()
                # Add lang to cash
                self.lang_cash[lang] = n_lang

                return n_lang.idlang

            return db_lang.idlang


