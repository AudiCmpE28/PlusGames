-- sql tables 
--New testing comment
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

CREATE TABLE Released_on ( -- see Ch8 Relational mapping slide 14
game_id VARCHAR(25) not null,
platform_name VARCHAR(25) not null,
primary key (game_id,platform_name),
foreign key (game_id) references Game(game_id) ON UPDATE CASCADE ON DELETE CASCADE,
foreign key (platform_name) references Platform(platform_name) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE Game(
  game_id       varchar(25) not null,
  g_company		varchar(25) not null,
  game_n		varchar(25) not null,
  genre			varchar(10),
  rating 		float(2,2),
  release_Date	date,
  price			float(2,2),
  primary key (game_id,g_company), -- pull PK of owner entity to weak entity
  foreign key (g_company) references Company(CompanyName)
);
-- need to decide if we keep Users table and link Guests/Members/Admins via Foreign Keys or doaway with inheritance
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
unique_id	integer(16),
mem_username	varchar(16),
mem_password	varchar(255) default null, -- insert hashed passwords by using a select statment and MD5('password')
primary key		(unique_id, mem_username)  -- temporary, might need to add email column for these tables
-- foreign key (unique_id) references Users(unique_id)
-- on delete cascade
);

CREATE TABLE request_game (
mem_username	varchar(16),
game_id       varchar(25) not null,
primary key (game_id,mem_username),
foreign key (game_id) references Game(game_id) ON UPDATE CASCADE ON DELETE CASCADE,
foreign key (mem_username) references Members(mem_username) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE comment_on (
c_date	date,
c_time 	timestamp,
comment_text varchar(250),
mem_username	integer(16),
game_id		integer(10),
primary key (mem_username, game_id), 
foreign key (mem_username) references Members(mem_username) on delete CASCADE,
foreign key (game_id) references Game(game_id) on delete CASCADE
);

CREATE TABLE review_on (
rv_date	date,
rv_time 	timestamp,
review_text varchar(250),
mem_username	integer(16),
game_id		integer(10),
primary key (mem_username, game_id), 
foreign key (mem_username) references Members(mem_username) on delete CASCADE,
foreign key (game_id) references Game(game_id) on delete CASCADE
);

CREATE TABLE report_on (
rp_date	date,
rp_time 	timestamp,
report_text varchar(250),
mem_username	integer(16),
game_id		integer(10),
primary key (mem_username, game_id), 
foreign key (mem_username) references Members(mem_username) on delete CASCADE,
foreign key (game_id) references Game(game_id) on delete CASCADE
);

CREATE TABLE bookmarked (
mem_username	integer(16),
game_id		integer(10),
primary key (mem_username, game_id), 
foreign key (mem_username) references Members(mem_username) on delete CASCADE,
foreign key (game_id) references Game(game_id) on delete CASCADE
);

CREATE TABLE Administrator (
unique_id	integer(16),
admin_username	varchar(16),
admin_password	varchar(255) default null,
primary key (unique_id, admin_username)
-- foreign key (unique_id) references Users(unique_id)
-- on update cascade
);

--  new (Pls check to see if its correct)
CREATE TABLE Profile (
user_id integer(16) not null,
name varchar(16),
primary key (user_id)
); 

--  new (Pls check to see if its correct)
CREATE TABLE interact_with (
mem_username	varchar(16),
user_id       varchar(16) not null,
primary key (mem_username, user_id),
foreign key (mem_username) references Members(mem_username) ON DELETE CASCADE,
foreign key (user_id) references Profile(user_id) ON DELETE CASCADE
);

--  new (Pls check to see if its correct)
CREATE TABLE manage (
admin_username	varchar(16),
user_id       varchar(16) not null,
primary key (admin_username, user_id),
foreign key (admin_username) references Administrator(admin_username) ON DELETE CASCADE,
foreign key (user_id) references Profile(user_id) ON DELETE CASCADE
);

insert into `Users` (`unique_id`) values (0); -- leave value at 0 for autoincrement to take effect, or insert custom user id --though the autoincrement continues from greatest previous value
insert into `Members` (`unique_id`, `mem_username`, `mem_password`) values (111, 'Anon', sha1('password123'));
