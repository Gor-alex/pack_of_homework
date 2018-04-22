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

    def __hash__(self):
        return hash(self.countrycode)


class Lang(Base):
    __tablename__ = 'lang'

    idlang = Column(Integer, primary_key=True, server_default=text("nextval('lang_idlang_seq'::regclass)"))
    snamelang = Column(Text)


class Tweet(Base):
    __tablename__ = 'tweet'

    idtweet = Column(BigInteger, primary_key=True)
    iduser = Column(ForeignKey(u'user.iduser', match=u'FULL'))
    idcountry = Column(ForeignKey(u'country.idcountry', match=u'FULL'))
    idlang = Column(ForeignKey(u'lang.idlang', match=u'FULL'))
    tweet_text = Column(Text)
    display_url = Column(Text)
    created_at = Column(Text)

    country = relationship(u'Country')
    lang = relationship(u'Lang')
    user = relationship(u'User')


class User(Base):
    __tablename__ = 'user'

    iduser = Column(BigInteger, primary_key=True)
    idlang = Column(ForeignKey(u'lang.idlang', match=u'FULL'))
    nameuser = Column(Text)
    locationuser = Column(Text)

    lang = relationship(u'Lang')
