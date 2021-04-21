-- Write more insert , delete queries which would be useful. 
-- test and report any errors in a comment

insert into `Users` (`unique_id`) values (0); -- leave value at 0 for autoincrement to take effect, or insert custom user id --though the autoincrement continues from greatest previous value
insert into `Members` (`unique_id`, `mem_username`, `mem_password`) values (111, 'Anon', sha1('password123'));

INSERT Company VALUES
('Microsoft'),('Bethesda'),('Arkane'),('Epic'),('Steam'),('Frontier'),('Ubisoft'),('Mojang');

select game_id, game_name, release_date from games where genre = 'Action'