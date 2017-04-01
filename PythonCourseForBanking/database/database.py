import datetime

from sqlalchemy import Column, Integer, Float, VARCHAR, DateTime
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DatabaseManagement:
    def __init__(self, server, database):
        self.server = server
        self.database = database

        self.connection_string = 'mssql+pyodbc://' + server + '/' + database + '?driver=SQL+Server+Native+Client+11.0'
        self.engine = create_engine(self.connection_string, echo=True)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

        self.deals_table = self.create_table_deals()

    def create_table_deals(self):
        if 'Deals' not in self.metadata.tables:
            Base.metadata.create_all(self.engine)

        deals_table = self.metadata.tables['Deals']
        return deals_table


# since Deal inherits Base, sqlalchemy is used as an ORM and the class is linked to a table in ms sql
class Deal(Base):
    __tablename__ = 'Deals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    type = Column(VARCHAR(20))
    quantity = Column(Float)
    isin = Column(VARCHAR(12))
    price = Column(Float)

    def __str__(self):
        return 'id =' + str(self.id) + ', date=' + str(self.date) + ', type=' + str(self.type) + ', quantity=' + \
               str(self.quantity) + ', isin=' + str(self.isin) + ', price=' + str(self.price)


if __name__ == '__main__':
    server = 'LAPTOP-JM6KCP86\SQLEXPRESS2'
    database = 'VbaFinanceDb'  # Nifigo
    db_mgmt = DatabaseManagement(server=server, database=database)

    # DELETE
    # clear table method 1 (interesting because use comprehension list)
    [db_mgmt.session.delete(x) for x in db_mgmt.session.query(Deal).all()]  # comprehension list --> important in Python
    db_mgmt.session.commit()
    # clear table method 2 (interesting because use bulk)
    db_mgmt.session.query(Deal).delete()

    # INSERT
    # single insertion
    my_deal_1 = Deal(date=datetime.datetime.today(), type='Action', quantity=5000, isin='US037833101 ', price=182.76)
    db_mgmt.session.add(my_deal_1)
    db_mgmt.session.commit()
    # multiple insertion
    my_deal_2 = Deal(date=datetime.datetime.today(), type='Action', quantity=15000, isin='US037833102 ', price=32.98)
    my_deal_3 = Deal(date=datetime.datetime.today(), type='Bond', quantity=2000, isin='US037833103 ', price=917.41)
    db_mgmt.session.add_all([my_deal_2, my_deal_3])
    db_mgmt.session.commit()

    # GET
    all_deals = db_mgmt.session.query(Deal).all()

    for deal in all_deals:
        print(deal)

    all_bonds = db_mgmt.session.query(Deal).filter_by(type='Bond').all()
    first_action = db_mgmt.session.query(Deal).filter_by(type='Action').first()

    # DISPLAY IN THE CONSOLE (view / tools windows / python console)
    # the following line works because we have overriden the __str__method of the class Deal
    print(first_action)
    [print(x) for x in all_bonds]  # we use a comprehension list again to make very concise code
