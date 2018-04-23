# coding: utf-8
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Country(Base):
    __tablename__ = 'country'

    idcountry = Column(Integer, primary_key=True, server_default=text("nextval('country_idcountry_seq'::regclass)"))
    countrycode = Column(Text)


class Lang(Base):
    __tablename__ = 'lang'

    idlang = Column(Integer, primary_key=True, server_default=text("nextval('lang_idlang_seq'::regclass)"))
    snamelang = Column(Text)


class Location(Base):
    __tablename__ = 'location'

    idlocation = Column(Integer, primary_key=True, server_default=text("nextval('location_idlocation_seq'::regclass)"))
    namelocation = Column(Text)


class Tweet(Base):
    __tablename__ = 'tweet'

    idtweet = Column(BigInteger, primary_key=True)
    idcountry = Column(ForeignKey(u'country.idcountry', match=u'FULL'))
    idlang = Column(ForeignKey(u'lang.idlang', match=u'FULL'))
    tweet_text = Column(Text)
    display_url = Column(Text)
    created_at = Column(Text)
    tweetsentiment = Column(BigInteger)
    idtweetuser = Column(ForeignKey(u'tweetuser.idtweetuser', match=u'FULL'))

    country = relationship(u'Country')
    lang = relationship(u'Lang')
    tweetuser = relationship(u'Tweetuser')


class Tweetuser(Base):
    __tablename__ = 'tweetuser'

    idtweetuser = Column(BigInteger, primary_key=True)
    idlang = Column(ForeignKey(u'lang.idlang', match=u'FULL'))
    idlocation = Column(ForeignKey(u'location.idlocation', match=u'FULL'))
    nameuser = Column(Text)

    lang = relationship(u'Lang')
    location = relationship(u'Location')
