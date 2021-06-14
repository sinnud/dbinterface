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

from io import StringIO

try:
    from dbinterface.postgresql import PostgreSQL
except:
    import sys
    sys.path.insert(0, os.path.abspath('../dbinterface'))
    from postgresql import PostgreSQL

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

class TestPostgreSQL(unittest.TestCase):

    def test_postgresql_connect(self):
        """
        * test connection using simple query
        """
        (getpass, (host, user, dbname, password, port)) = GetPostgreSQLLoginInfo()
        if not getpass:
            print(f"Failed to get password information from pem file!!!")
            exit(1)
        ps = PostgreSQL(host
                        , user
                        , dbname
                        , password
                        , port=port
                       )
        qry = "SELECT distinct table_name FROM INFORMATION_SCHEMA.columnS WHERE TABLE_SCHEMA='wdinfo' AND TABLE_NAME='sinnud'"
        rst=ps.execute(qry)[0][0]
        self.assertEqual(rst, "sinnud")
    
    def test_postgresql_import(self):
        """
        * test import_from_file method
        """
        (getpass, (host, user, dbname, password, port)) = GetPostgreSQLLoginInfo()
        if not getpass:
            print(f"Failed to get password information from pem file!!!")
            exit(1)
        ps = PostgreSQL(host
                        , user
                        , dbname
                        , password
                        , port=port
                       )
        temptbl = "wdinfo.sinnud"
        df = "/tmp/sinnud.csv"
        # COPY {0} FROM stdin DELIMITER as '{1}' CSV NULL '' ESCAPE '{2}' QUOTE E'{3}'
        qry = f"COPY {temptbl} FROM STDIN DELIMITER as '|' CSV NULL ''"
        with open(df, "r") as f:
            dfbuffer = f.read()
        dflist=list(filter(None, dfbuffer.split('\n')))
        print(f"Length of dflist: {len(dflist)}")
        rst=ps.import_from_file(qry, StringIO('\n'.join(dflist)))
        print(f"Result: {rst}")
        qry = "SELECT count(*) from wdinfo.sinnud"
        rst=ps.execute(qry)[0][0]
        self.assertEqual(rst, 5)
    

if __name__ == '__main__':
    unittest.main()