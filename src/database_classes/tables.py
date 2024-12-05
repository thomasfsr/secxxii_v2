from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Numeric
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "clientes"

    cliente_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    tel = Column(Integer)

    # Reverse relationships
    comandas = relationship("Comanda", back_populates="cliente")
    log_comandas = relationship("LogComanda", back_populates="cliente")
    registros = relationship("Registro", back_populates="cliente")
    fluxos = relationship("Fluxo", back_populates="cliente")

class Comanda(Base):
    __tablename__ = "comandas"

    comanda_id = Column(Integer, primary_key=True, autoincrement=True) 
    cliente_id = Column(Integer, ForeignKey('clientes.cliente_id'))
    data_entrada = Column(Date)
    data_entrega = Column(Date)
    data_retirada = Column(Date)
    servico = Column(String(100))
    preco_total = Column(Numeric(10, 2))
    sinal = Column(Numeric(10, 2))
    valor_restante = Column(Numeric(10, 2))
    tipo_pag = Column(String(10))
    status_name = Column(String(10))

    # Relationships
    cliente = relationship("Cliente", back_populates="comandas")

    #Reverse Relationship
    log_comandas = relationship("LogComanda", back_populates="comanda")
    registros = relationship("Registro", back_populates="comanda")
    fluxos = relationship("Fluxo", back_populates="comanda")

class LogComanda(Base):
    __tablename__ = "log_comandas"

    log_id = Column(Integer, primary_key=True, autoincrement=True)  
    comanda_id = Column(Integer, ForeignKey('comandas.comanda_id'))
    cliente_id = Column(Integer, ForeignKey('clientes.cliente_id')) 
    data_evento = Column(Date)
    servico = Column(String(100))
    preco_total = Column(Numeric(10, 2))
    sinal = Column(Numeric(10, 2))
    valor_restante = Column(Numeric(10, 2))
    status_name = Column(String(10))

    # Relationships
    comanda = relationship("Comanda", back_populates="log_comandas")
    cliente = relationship("Cliente", back_populates="log_comandas")

class Registro(Base):
    __tablename__ = "registros"

    registro_id = Column(Integer, primary_key=True, autoincrement=True)  
    valor = Column(Numeric(10, 2))
    data_entrada = Column(Date)
    comanda_id = Column(Integer, ForeignKey('comandas.comanda_id')) 
    cliente_id = Column(Integer, ForeignKey('clientes.cliente_id'))
    status_name = Column(String(10))
    tipo_pag = Column(String(10))
    categoria = Column(String(30))
    descricao = Column(String(100))

    # Relationships
    comanda = relationship("Comanda", back_populates="registros")
    cliente = relationship("Cliente", back_populates="registros")

class Fluxo(Base):
    __tablename__ = "fluxo"

    fluxo_id = Column(Integer, primary_key=True, autoincrement=True) 
    valor = Column(Numeric(10, 2))
    data_entrada = Column(Date)
    categoria = Column(String(30))
    comanda_id = Column(Integer, ForeignKey('comandas.comanda_id')) 

    # Relationship
    comanda = relationship("Comanda", back_populates="fluxo")
    cliente = relationship("Cliente", back_populates="fluxo")
