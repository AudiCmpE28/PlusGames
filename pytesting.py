import mysql.connector
from mysql.connector import Error
import pandas as pd
from pyconnector import *


connection = create_db_connection("localhost","root","1234","+games")

samplequery="""
insert into `Members`
(`unique_id`, `mem_username`, `mem_password`)
values
(111, 'Anon', sha1('password123'));
"""
## above query does not work atm, below work. you can see it appear in the workbench table
execute_query(connection, samplequery)

companyinsert = """
INSERT Company VALUES
('Microsoft'),('Bethesda'),('Arkane'),('Epic'),('Steam'),('Frontier'),('Ubisoft'),('Mojang');
"""

execute_query(connection, companyinsert)