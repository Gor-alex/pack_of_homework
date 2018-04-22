# -*- coding: utf-8 -*-
import json

from service.database import DataBase
from third import model


def parse_json(json_filename, session):
    # Load classificatories from db
    user_cash = dict()
    country_cash = dict()
    lang_cash = dict()

    with open(json_filename, 'rb') as input_file:
        for json_body in input_file:
            data = json.loads(json_body)
            try:
                if u'delete' not in data.keys():
                    id_user, lang_cash, user_cash = _user(data[u'user'], session, user_cash, lang_cash)
                    id_country = None
                    if data[u'place'] is not None:
                        id_country, country_cash = _place(data[u'place'],  country_cash, session)

                    tweet_lang, lang_cash = _lang(data[u'lang'], session, lang_cash)

                    n_tweet = model.Tweet(
                        idtweet=data[u'id'],
                        iduser=id_user,
                        idcountry=id_country,
                        idlang=tweet_lang,
                        tweet_text=data[u'text'],
                        display_url=data[u'source'],
                        created_at=data[u'created_at']
                    )
                    session.add(n_tweet)
                session.flush()
                session.commit()

            except Exception as error:
                print('Error: ' + error.message)


def _place(data, country_cash, session):
    if data[u'country_code'] in country_cash:
        return country_cash[data[u'country_code']], country_cash
    else:
        country = session.query(model.Country)\
            .filter(model.Country.countrycode == data[u'country_code']).one_or_none()

        if country is None:
            n_country = model.Country(
                countrycode=data[u'country_code']
            )
            session.add(n_country)
            session.flush()

            country_cash.add(n_country)

            return n_country.idcountry, country_cash

        return country.idcountry, country_cash


def _user(data, session, user_cash, lang_cash):
    user = session.query(model.User)\
        .filter(model.User.iduser == data[u'id']).one_or_none()

    if user is None:
        id_lang, lang_cash = _lang(data[u'lang'], session, lang_cash)

        n_user = model.User(
                iduser=data[u'id'],
                idlang=id_lang,
                nameuser=data[u'name'],
                locationuser=data[u'location']
            )

        session.add(n_user)
        session.flush()

        user_cash.add(n_user)

        return n_user.iduser, lang_cash, user_cash

    return user.iduser, lang_cash, user_cash


def _lang(lang, session, lang_cash):
    db_lang = session.query(model.Lang)\
        .filter(model.Lang.snamelang == lang).one_or_none()

    if db_lang is None:
        n_lang = model.Lang(
            snamelang=lang
        )
        session.add(n_lang)
        session.flush()

        lang_cash.add(n_lang)

        return n_lang.idlang, lang_cash

    return db_lang.idlang, lang_cash


if __name__ == '__main__':
    db_connect = DataBase()
    parse_json(
        '/home/goralex/projects/pack_of_homework/third/docs/three_minutes_tweets.json',
        session=db_connect.new_session()
    )