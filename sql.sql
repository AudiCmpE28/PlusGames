drop database if exists `+games`;
create database `+games`;
use `+games`;


CREATE TABLE Company (
    CompanyName VARCHAR(25),
    
    PRIMARY KEY (CompanyName)
);
CREATE TABLE Platform (
platform_name varchar(25),
PRIMARY KEY (platform_name)
);

CREATE TABLE Released_on (

);


CREATE TABLE Develops (
	-- company_n varchar(25),
--     game_n	varchar(25),
--     primary key (company,game),
--     foreign key (company) references Company(CompanyName),
--     foreign key (game_n) references Company(game_n)
);

CREATE TABLE Game(
  game_id       varchar(25) not null,
  g_company		varchar(25) not null,
  game_n		varchar(25) not null,
  genre			varchar(10),
  rating 		float(2,2),
  release_Date	date,
  price			float(2,2),
  primary key (game_id,game_n),
  foreign key (g_company) references Company(CompanyName)
);

CREATE TABLE Users (

);