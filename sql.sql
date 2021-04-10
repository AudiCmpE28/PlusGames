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

-- CREATE TABLE Released_on (

-- );


-- CREATE TABLE Develops (
-- 	company_n varchar(25),
--     game_n	varchar(25),
--     primary key (company,game),
--     foreign key (company) references Company(CompanyName),
--     foreign key (game_n) references Company(game_n)
-- );

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
-- need 2 decide if we keep Users table and link Guests/Members/Admins via Foreign Keys or doaway with inheritance
CREATE TABLE Users (
unique_id	integer not null AUTO_INCREMENT primary key
);


CREATE TABLE Guests (
unique_id	integer,
primary key (unique_id)
-- foreign key (unique_id) references Users(unique_id)
-- on delete cascade
);

CREATE TABLE Members (
unique_id	integer(10),
mem_username	varchar(16),
mem_password	varchar(255) default null, -- insert hashed passwords by using a select statment and MD5('password')
primary key		(unique_id, mem_username)  -- temporary, might need to add email column for these tables
-- foreign key (unique_id) references Users(unique_id)
-- on delete cascade
);

CREATE TABLE comment_on (
c_date	date,
c_time 	timestamp,
comment_text varchar(250),
unique_id	integer(10),
game_id		integer(10),
primary key (unique_id, game_id), -- ?
-- primary key (c_date, c_time, unique_id, game_id),
foreign key (unique_id) references Members(unique_id) on delete set null,
foreign key (game_id) references Game(game_id) on delete set null
);

-- CREATE TABLE request (

-- );

-- CREATE TABLE review (

-- );

-- CREATE TABLE report (

-- );

-- CREATE TABLE bookmark (

-- );

CREATE TABLE Administrator (
unique_id	integer(10),
admin_username	varchar(16),
admin_password	varchar(255) default null,
primary key (unique_id, admin_username)
-- foreign key (unique_id) references Users(unique_id)
-- on update cascade
);

insert into `Users` (`unique_id`) values (0); -- leave value at 0 for autoincrement to take effect, or insert custom user id --though the autoincrement continues from greatest previous value
insert into `Members` (`unique_id`, `mem_username`, `mem_password`) values (111, 'Anon', sha1('password123'));
