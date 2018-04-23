# -*- coding: utf-8 -*-
import os
from sys import exit

from service.afinn import AfinnReader
from service.database import DataBase
from tweet import TweetLoader

if __name__ == '__main__':
    # Path of module
    a_path = os.path.dirname(__file__)

    # Load information for account rating
    afinn = AfinnReader(a_path)
    afinn.load()

    # Create connection to db
    db_connect = DataBase()
    # Create parser object
    parser = TweetLoader(a_path, afinn)
    # Parsing json file and load information to db
    parser.load_information(db_connect.new_session())
    # Exit from program
    exit(0)