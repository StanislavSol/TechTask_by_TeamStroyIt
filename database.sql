DROP TABLE IF EXISTS top100;
DROP TABLE IF EXISTS repo_info;

CREATE TABLE top100 (
    id SERIAL PRIMARY KEY,
    repo varchar(255) UNIQUE,
    owner varchar(255),
    position_cur integer,
    position_prev integer,
    stars integer,
    watchers integer,
    forks integer,
    open_issues integer,
    language varchar(255));

CREATE TABLE repo_info (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    topId integer,
    date DATE,
    commits integer,
    autors text[]);
