-- Write more insert , delete queries which would be useful. 
-- test and report any errors in a comment

insert into `Users` (`unique_id`) values (0);

-- the line below gives an error 
-- insert into `Members` (`unique_id`, `mem_username`, `mem_password`) values (1, 'Anon', sha1('password123'));
-- Cannot add or update a child row: a foreign key constraint fails (`+games`.`members`, CONSTRAINT `members_ibfk_1` FOREIGN KEY (`unique_id`) REFERENCES `users` (`unique_id`) ON DELETE CASCADE ON UPDATE CASCADE)

INSERT Company VALUES ('Microsoft'),('Bethesda'),('Arkane'),('Epic'),('Steam'),('Frontier'),('Ubisoft'),('Mojang');

INSERT INTO Game (g_company, game_id, game_n, genre) VALUES ('Microsoft', 21345, 'Minecraft', 'Action');
INSERT INTO Game (g_company, game_id, game_n, genre) VALUES ('Microsoft', 54398, 'Halo', 'Shooter');
INSERT INTO Game (g_company, game_id, game_n, genre) VALUES ('Microsoft', 23904, 'Forza Horizon', 'Racing');

select game_id, game_n, g_company from game where genre = 'Action';

SELECT game_n FROM game WHERE g_company = 'Microsoft';

INSERT INTO Profile (name, user_id) VALUES ('Carter', '82394');
INSERT INTO Profile (name, user_id) VALUES ('Carp', '34904');
INSERT INTO Profile (name, user_id) VALUES ('Devin', '43029');

SELECT DISTINCT user_id, name
FROM Profile
WHERE name LIKE '_a%';

-- new test cases
SELECT DISTINCT game_id 
FROM Game
WHERE game_id = 21345 OR game_id = 23904;

-- test cases for administrator
-- you cannot add admins/guests/members without adding a user first. see addmembers connector as example
INSERT INTO administrator (unique_id, admin_username, admin_password) VALUES('12345','izdawiz1','sjsu');
INSERT INTO administrator (unique_id, admin_username, admin_password) VALUES('67896','audiCmpe2','doggo');
INSERT INTO administrator (unique_id, admin_username, admin_password) VALUES('98765','dankman3','yolo');
INSERT INTO administrator (unique_id, admin_username, admin_password) VALUES('23457','vasser4','hello');

SELECT *
FROM administrator
;

insert into company values('Company1');
insert into company values('Company2');
insert into game(g_company, game_id, game_n,rating,release_Date,genre,price) values ('Company1',1,'Game1',4.50,'2020-02-20','Action',59.99);
insert into game(g_company, game_id, game_n,rating,release_Date,genre,price) values ('Company2',2,'Game2',1.50,'2020-01-10','RPG',19.99);
insert into comment_on (mem_username, game_id,c_date,c_time,comment_text) values ('hremvgltumluwxwk', 23904,NOW(),NOW(), "COMMENT TEXT");
select * from Game order by rating desc;


SELECT g.game_id,g.game_n,g.genre,g.rating,g.release_date,g.price FROM Game as g join Released_on as r WHERE g.game_id = r.game_id and r.platform_name!=" ";