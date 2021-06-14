"""
* File name: test_postgresql.py
* Purpose: test postgresql.py
* Use python moduel unittest

"""
# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import os
import unittest

try:
    from dbinterface.sql import Sql
except:
    import sys
    sys.path.insert(0, os.path.abspath('../dbinterface'))
    from sql import Sql

def GetPostgreSQLLoginInfo():
    """
    * Get database login information from pem file
    """
    passfile = '/mnt/data/other/pem/sinnud_pg.dat'
    with open(passfile, 'r') as f:
        passinfo = f.read().strip()
    (host, user, dbname, password, port) = passinfo.split()
    if os.path.isfile(passfile):
        return (True, (host, user, dbname, password, port))
    return (False, None)

class TestSQL(unittest.TestCase):

    def test_sql_connect(self):
        """
        * test connection using simple query
        """
        (getpass, (host, user, dbname, password, port)) = GetPostgreSQLLoginInfo()
        if not getpass:
            print(f"Failed to get password information from pem file!!!")
            exit(1)
        ps = Sql(host, dbname, user=user, passwd=password, port=port
                )
        qry = "SELECT distinct table_name FROM INFORMATION_SCHEMA.columnS WHERE TABLE_SCHEMA='wdinfo' AND TABLE_NAME='sinnud'"
        rst=ps.sql_execute_with_replace(qry)[0][0]
        self.assertEqual(rst, "sinnud")

    def test_export(self):
        """
        * test export_to_file method
        """
        (getpass, (host, user, dbname, password, port)) = GetPostgreSQLLoginInfo()
        if not getpass:
            print(f"Failed to get password information from pem file!!!")
            exit(1)
        ps = Sql(host, dbname, user=user, passwd=password, port=port
                )
        temptbl = "wdinfo.sinnud"
        df = "/tmp/sinnud_out.csv"
        with open(df, "w") as f:
            qry = f"COPY {temptbl} TO STDOUT HEADER DELIMITER as '|' CSV NULL ''"
            rst=ps.export_to_file(qry, f)
        

if __name__ == '__main__':
    unittest.main()