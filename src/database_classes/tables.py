from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Numeric
from sqlalchemy.orm import relationship, declarative_base, registry, mapped_column, Mapped
from datetime import date
from enum import Enum

Base = declarative_base()

table_registry = registry()

class pagamento_state(str,Enum):
    DINHEIRO = 'DINHEIRO'
    PIX = 'PIX'
    CREDITO = 'CRÉDITO'
    DEBITO = 'DÉBITO'

class status_state(str, Enum):
    A_FAZER = 'A FAZER'
    PRONTO = 'PRONTO'
    RETIRADO = 'RETIRADO'
    
@table_registry.mapped_as_dataclass
class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    nome: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)

@table_registry.mapped_as_dataclass
class Cliente(Base):
    __tablename__ = "clientes"

    cliente_id = mapped_column(init=False, primary_key=True)
    nome : Mapped[str]
    tel : Mapped[int]

@table_registry.mapped_as_dataclass
class Comanda(Base):
    __tablename__ = "comandas"

    comanda_id: Mapped[int] = mapped_column(primary_key=True, init=False) 
    cliente_id: Mapped[int] = mapped_column(Integer, ForeignKey('clientes.cliente_id'))
    data_entrada: Mapped[date] = mapped_column(Date)
    data_entrega: Mapped[date] = mapped_column(Date)
    data_retirada: Mapped[date] = mapped_column(Date)
    servico: Mapped[str] = mapped_column(String(100))
    preco_total: Mapped[float] = mapped_column(Numeric(10, 2))
    sinal: Mapped[float] = mapped_column(Numeric(10, 2))
    valor_restante: Mapped[float] = mapped_column(Numeric(10, 2))
    tipo_pag: Mapped[pagamento_state] = mapped_column(String(10))
    status_name: Mapped[status_state] = mapped_column(String(10))

    # Relationships
    cliente = relationship("Cliente", back_populates="comandas")

    #Reverse Relationship
    log_comandas = relationship("LogComanda", back_populates="comanda")
    registros = relationship("Registro", back_populates="comanda")
    fluxos = relationship("Fluxo", back_populates="comanda")

@table_registry.mapped_as_dataclass
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

@table_registry.mapped_as_dataclass
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

@table_registry.mapped_as_dataclass
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
