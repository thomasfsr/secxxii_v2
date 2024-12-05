CREATE TABLE IF NOT EXISTS clientes (
    cliente_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(30),
    tel INTEGER
);

CREATE TABLE IF NOT EXISTS comandas (
    comanda_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    data_entrada DATE,
    data_entrega DATE,
    data_retirada DATE,
    servico VARCHAR(100),
    preco_total DECIMAL(10,2),
    sinal DECIMAL(10,2),
    valor_restante DECIMAL(10,2),
    tipo_pag VARCHAR(10),
    status_name VARCHAR(10)
); 

CREATE TABLE IF NOT EXISTS log_comandas (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    comanda_id INT,
    cliente_id INTEGER,
    data_evento DATE,
    servico VARCHAR(100),
    preco_total DECIMAL(10,2),
    sinal DECIMAL(10,2),
    valor_restante DECIMAL(10,2),
    status_name VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS registros (
    registro_id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor DECIMAL(10,2),
    data_entrada DATE,
    comanda_id INT,
    cliente_id VARCHAR(10),
    status_name VARCHAR(10),
    tipo_pag VARCHAR(10),
    categoria VARCHAR(30),
    descricao VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS fluxo (
    fluxo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor DECIMAL(10,2),
    data_entrada DATE,
    categoria VARCHAR(30),
    comanda_id INT
    
);

-- CREATE TABLE IF NOT EXISTS cliente (
--     cliente_id INTEGER PRIMARY KEY,
--     nome VARCHAR(30),
--     tel HUGEINT
-- );

-- CREATE TABLE IF NOT EXISTS comanda (
--     comanda_id INT PRIMARY KEY,
--     cliente_id INTEGER,
--     data_entrada DATE,
--     data_entrega DATE,
--     data_retirada DATE,
--     servico VARCHAR(100),
--     preco_total DECIMAL(10,2),
--     sinal DECIMAL(10,2),
--     valor_restante DECIMAL(10,2),
--     status_name VARCHAR(10)
-- );

-- CREATE TABLE IF NOT EXISTS log_comanda (
--     log_id INT PRIMARY KEY,
--     comanda_id INT,
--     cliente_id INTEGER,
--     data_evento DATE,
--     servico VARCHAR(100),
--     preco_total DECIMAL(10,2),
--     sinal DECIMAL(10,2),
--     valor_restante DECIMAL(10,2),
--     status_name VARCHAR(10)
--     );

-- CREATE TABLE IF NOT EXISTS registro (
--     registro_id INT PRIMARY KEY,
--     valor DECIMAL(10,2),
--     data_entrada DATE,
--     comanda_id INT,
--     cliente_id VARCHAR(10),
--     status_name VARCHAR(10)
-- )