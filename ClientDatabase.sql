-- Таблица для Idempotency Key
create table Idempotency_Key (
    ik_id serial primary key,
    key varchar(128),
    created_at timestamp with time zone
);

-- Таблица для клиентов
create table Client (
    client_id serial primary key,
    ik_id integer,
    surename varchar(50),
    name varchar(50),
    lastname varchar(50),
    email varchar(255),
    phoneNumber varchar(15),
    passportSeries varchar(4),
    passportNumber varchar(6),
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    constraint fk_client_ik_id
        foreign key (ik_id)
        references Idempotency_Key(ik_id)
);

-- Таблица для сотрудников
create table Employee (
    employee_id serial primary key,
    ik_id integer,
    name varchar(50),
    role varchar(100),
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    constraint fk_employee_ik_id
        foreign key (ik_id)
        references Idempotency_Key(ik_id)
);

-- Таблица для логов действий
create table Logs (
    log_id serial primary key,
    actor_id integer,
    client_id integer,
    action varchar(256),
    timestamp timestamp with time zone,
    trace_key varchar(128),
    constraint fk_client_id
        foreign key (client_id)
        references Client(client_id),
    constraint fk_actor_id
        foreign key (actor_id)
        references Employee(employee_id)
);
