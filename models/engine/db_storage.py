#!/usr/bin/python3
'''
    Define class DatabaseStorage
'''
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
import models
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    '''
        Create SQLalchemy database
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''
            Create engine and link to MySQL databse (hbnb_dev, hbnb_dev_db)
        '''
        # user = getenv("HBNB_MYSQL_USER")
        # pwd = getenv("HBNB_MYSQL_PWD")
        # host = getenv("HBNB_MYSQL_HOST")
        # db = getenv("HBNB_MYSQL_DB")
        # envv = getenv("HBNB_ENV", "none")
        # self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
        #     user, pwd, host, db), pool_pre_ping=True)
        # if envv == 'test':
        #     Base.metadata.drop_all(self.__engine)
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
            Query current database session
        '''
        db_dict = {}

        if cls != "":
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            # objs = self.__session.query(models.classes[cls]).all()
            # for obj in objs:
            #     if 'is_instance_state' in obj.__dict__:
            #         obj.__dict__.pop('is_instance_state')
            for obj in query:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                db_dict[key] = obj
            # return db_dict
        else:
            obj_list = [User, State, City, Amenity, Place, Review]
            # for k, v in models.classes.items():
            #     if k != "BaseModel":
            for class_name in obj_list:
                query = self.__session.query(class_name)
                # objs = self.__session.query(v).all()
                # if len(objs) > 0:
                for obj in query:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    db_dict[key] = obj
        return db_dict

    def new(self, obj):
        '''
            Add object to current database session
        '''
        self.__session.add(obj)

    def save(self):
        '''
            Commit all changes of current database session
        '''
        self.__session.commit()

    def delete(self, obj=None):
        '''
            Delete from current database session
        '''
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        '''
            Commit all changes of current database session
        '''
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self):
        '''
            Remove private session attribute
        '''
        self.__session.close()
