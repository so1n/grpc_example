create database if not exists grpc_example;
use grpc_example;
create table if not exists book_comment (
    isbn varchar(32) not null comment 'book isbn',
    content text  null comment 'book comment content',
    uid varchar(32) not null comment 'comment uid',
    create_time             timestamp   default CURRENT_TIMESTAMP null,
    update_time             timestamp   default CURRENT_TIMESTAMP not null,
    deleted                 tinyint(2)  default 0                 not null
) comment 'book comment';

create table if not exists book_like (
    isbn varchar(32) not null comment 'book isbn',
    uid varchar(32) not null comment 'comment uid',
    `like` tinyint(2) not null comment 'user like book flag',
    create_time             timestamp   default CURRENT_TIMESTAMP null,
    update_time             timestamp   default CURRENT_TIMESTAMP not null,
    deleted                 tinyint(2)  default 0                 not null
) comment 'user like book flag';

create table if not exists book_info (
    isbn varchar(32) not null comment 'book isbn',
    book_name varchar(255) not null comment 'book name',
    book_author varchar(255) not null comment 'book author',
    book_desc text not null comment 'book desc',
    book_url text not null comment 'book url',
    create_time             timestamp   default CURRENT_TIMESTAMP null,
    update_time             timestamp   default CURRENT_TIMESTAMP not null,
    deleted                 tinyint(2)  default 0                 not null
) comment 'book';