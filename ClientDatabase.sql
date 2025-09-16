-- Таблица для Idempotency Key
CREATE TABLE Idempotency_Key (
    ik_id serial PRIMARY KEY,
    key varchar(128) NOT NULL,
    created_at timestamp with time zone DEFAULT NOW()
);

-- Таблица для клиентов
CREATE TABLE Client (
    client_id serial PRIMARY KEY,
    ik_id varchar(128),
    surename varchar(50),
    name varchar(50),
    lastname varchar(50),
    email varchar(256) NOT NULL,
    phoneNumber varchar(256),
    passportSeries varchar(256),
    passportNumber varchar(256),
    created_at timestamp with time zone DEFAULT NOW(),
    updated_at timestamp with time zone DEFAULT NOW()
);

-- Таблица для сотрудников
CREATE TABLE Employee (
    employee_id serial PRIMARY KEY,
    ik_id varchar(128),
    name varchar(50) NOT NULL,
    role varchar(100),
    created_at timestamp with time zone DEFAULT NOW(),
    updated_at timestamp with time zone DEFAULT NOW()

);

-- Таблица для логов действий
CREATE TABLE Logs (
    log_id serial PRIMARY KEY,
    actor_id integer NOT NULL,
    client_id integer NOT NULL,
    action varchar(256) NOT NULL,
    timestamp timestamp with time zone DEFAULT NOW(),
    trace_key varchar(128),
    CONSTRAINT fk_client_id
        FOREIGN KEY (client_id)
        REFERENCES Client(client_id),
    CONSTRAINT fk_actor_id
        FOREIGN KEY (actor_id)
        REFERENCES Employee(employee_id)
);
