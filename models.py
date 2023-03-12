from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from databases import Base


many_to_many_table_fuusilised_isikud = Table(
    "many_to_many_table_fuusilised_isikud",
    Base.metadata,
    Column("index", Integer, primary_key=True, autoincrement=True),
    Column("left_id_osauhingud", Integer, ForeignKey("osauhingud.index")),
    Column("right_id_osanikud", Integer, ForeignKey(
        "fuusilisest_isikust_osanikud.index")),
    Column("osakapital", Integer),
    Column("is_asutaja", String(100))
)

many_to_many_table_juriidilised_isikud = Table(
    "many_to_many_table_juriidilised_isikud",
    Base.metadata,
    Column("index", Integer, primary_key=True, autoincrement=True),
    Column("left_id_osauhingud", Integer, ForeignKey("osauhingud.index")),
    Column("right_id_osanikud", Integer, ForeignKey(
        "juriidilisest_isikust_osanikud.index")),
    Column("osakapital", Integer),
    Column("is_asutaja", String(100))
)


class Osauhingud(Base):
    '''
    Osaühingute tabel. Asutamise kuupäev tuli kodeerida stringina,
    et seda frontendis õigesti kuvada.
    '''
    __tablename__ = 'osauhingud'

    index = Column(Integer, primary_key=True, autoincrement=True)
    osauhingu_nimi = Column(String(100), nullable=False)
    registri_kood = Column(Integer, nullable=False)
    asutamise_kuupaev = Column(String(10), nullable=False)
    kapital = Column(Integer, nullable=False)

    fuusilised_osanikud = relationship(
        "FuusilisestIsikustOsanikud",
        secondary=many_to_many_table_fuusilised_isikud,
        back_populates="osaniku_osauhingud",
        cascade="all, delete",
    )

    juriidilised_osanikud = relationship(
        "JuriidilisestIsikustOsanikud",
        secondary=many_to_many_table_juriidilised_isikud,
        back_populates="osaniku_osauhingud",
        cascade="all, delete",
        primaryjoin="Osauhingud.index == \
            many_to_many_table_juriidilised_isikud.c.left_id_osauhingud",
        secondaryjoin="JuriidilisestIsikustOsanikud.index == \
            many_to_many_table_juriidilised_isikud.c.right_id_osanikud"
    )

    def __repr__(self):
        return f"<User(index={self.index}, osauhingu nimi={self.osauhingu_nimi},\
            registrikood={self.registri_kood}, asutamise kuupaev={self.asutamise_kuupaev})>"


class FuusilisestIsikustOsanikud(Base):
    '''
    Füüsilisest isikust osanike andmebaasi tabel.
    Isikukood on kodeeritud stringina, sest isegi BigInt
    andmetüüp ei mahutanud selle ära. 
    '''
    __tablename__ = 'fuusilisest_isikust_osanikud'

    index = Column(Integer, primary_key=True, autoincrement=True)
    nimi = Column(String(200), nullable=False)
    isikukood = Column(String(11), nullable=False)

    osaniku_osauhingud = relationship(
        "Osauhingud",
        secondary=many_to_many_table_fuusilised_isikud,
        back_populates="fuusilised_osanikud",
        cascade="all, delete",
    )

    def __repr__(self):
        return f"<User(index={self.index}, nimi={self.nimi},\
            isikukood={self.isikukood}>"


class JuriidilisestIsikustOsanikud(Base):
    '''
    Juriidilisest isikust osanike andmebaasi tabel.
    '''
    __tablename__ = 'juriidilisest_isikust_osanikud'

    index = Column(Integer, primary_key=True, autoincrement=True)
    nimi = Column(String(200), nullable=False)
    registrikood = Column(Integer, nullable=False)

    osaniku_osauhingud = relationship(
        "Osauhingud",
        secondary=many_to_many_table_juriidilised_isikud,
        back_populates="juriidilised_osanikud",
        cascade="all, delete",
    )

    def __repr__(self):
        return f"<User(index={self.index}, nimi={self.nimi},\
            registrikood={self.registrikood}>"
