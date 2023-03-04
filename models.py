from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from databases import Base

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship


many_to_many_table_fuusilised_isikud = Table(
    "many_to_many_table_fuusilised_isikud",
    Base.metadata,
    Column("left_id_osauhingud", ForeignKey("osauhingud.index"), primary_key=True),
    Column("right_id_osanikud", ForeignKey("fuusilisest_isikust_osanikud.index"), primary_key=True),
)

many_to_many_table_juriidilised_isikud = Table(
    "many_to_many_table_juriidilised_isikud",
    Base.metadata,
    Column("left_id_osauhingud", ForeignKey("osauhingud.index"), primary_key=True),
    Column("right_id_osanikud", ForeignKey("juriidilisest_isikust_osanikud.index"), primary_key=True),
)

class Osauhingud(Base):
    __tablename__ = 'osauhingud'

    index = Column(Integer, primary_key=True, autoincrement=True)
    osauhingu_nimi = Column(String(100), nullable=False)
    registri_kood = Column(Integer, nullable=False)
    asutamise_kuupaev = Column(Date)

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
        primaryjoin="Osauhingud.index == many_to_many_table_juriidilised_isikud.c.left_id_osauhingud",
        secondaryjoin="JuriidilisestIsikustOsanikud.index == many_to_many_table_juriidilised_isikud.c.right_id_osanikud"
    )

    def __repr__(self):
        return "<User(index='%s', osauhingu nimi='%s', registri kood='%s', asutamise kuupaev='%s')>" % (
            self.index,
            self.osauhingu_nimi,
            self.registri_kood,
            self.asutamise_kuupaev,
        )


class FuusilisestIsikustOsanikud(Base):
    __tablename__ = 'fuusilisest_isikust_osanikud'

    index = Column(Integer, primary_key=True, autoincrement=True)
    nimi = Column(String(200), nullable=False)
    isikukood = Column(Integer, nullable=False)

    osaniku_osauhingud = relationship(
        "Osauhingud",
        secondary=many_to_many_table_fuusilised_isikud,
        back_populates="fuusilised_osanikud",
        cascade="all, delete",
    )


class JuriidilisestIsikustOsanikud(Base):
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



'''
many_to_many_tabel_fuusilised_isikud = Table(
    "many_to_many_tabel_fuusilised_isikud",
    Base.metadata,
    Column("left_id_osauhingud", ForeignKey("osauhingud.index"), primary_key=True),
    Column("right_id_osanikud", ForeignKey("fuusilisest_isikust_osanikud.index"), primary_key=True),
)

many_to_many_tabel_juriidilised_isikud = Table(
    "many_to_many_tabel_juriidilised_isikud",
    Base.metadata,
    Column("left_id_osauhingud", ForeignKey("osauhingud.index"), primary_key=True),
    Column("right_id_osanikud", ForeignKey("juriidilised_isikust_osanikud.index"), primary_key=True),
)

class Osauhingud(Base):
    __tablename__='osauhingud'

    index = Column(Integer, primary_key = True, autoincrement=True)
    osauhingu_nimi = Column(String(100), nullable=False)
    registri_kood = Column(Integer, nullable=False)
    asutamise_kuupaev= Column(Date)
    fuusilised_osanikud = relationship(
        secondary=many_to_many_tabel_fuusilised_isikud, back_populates="osaniku_osauhingud"
    )
    juriidilised_osanikud = relationship(
        secondary=many_to_many_tabel_juriidilised_isikud, back_populates="osaniku_osauhingud"
    )

    def __repr__(self):
        return "<User(index='%s', osauhingu nimi='%s', registri kood='%s', asutamise kuupaev='%s')>" % (
            self.index,
            self.osauhingu_nimi,
            self.registri_kood,
            self.asutamise_kuupaev)

class FuusilisestIsikustOsanikud(Base):
    __tablename__='fuusilisest_isikust_osanikud'

    index = Column(Integer, primary_key = True, autoincrement=True)
    nimi = Column(String(200), nullable=False)
    isikukood = Column(Integer, nullable=False)
    osaniku_osauhingud= relationship(
        secondary=many_to_many_tabel_fuusilised_isikud, back_populates="fuusilised_osanikud"
    )


class JuriidilisestIsikustOsanikud(Base):
    __tablename__='juriidilisest_isikust_osanikud'

    index = Column(Integer, primary_key=True, autoincrement=True)
    nimi = Column(String(200), nullable=False)
    registrikood = Column(Integer, nullable=False)
    osaniku_osauhingud= relationship(
        secondary=many_to_many_tabel_juriidilised_isikud, back_populates="juriidilised_osanikud"
    )

    
'''
