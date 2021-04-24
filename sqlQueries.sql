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
