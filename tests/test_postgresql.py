# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import os
import unittest

from src.py_pkg_db.postgresql import PostgreSQL

def GetPostgreSQLLoginInfo():
    # check password file exists
    passfile = '/mnt/data/other/pem/sinnud_pg.dat'
    with open(passfile, 'r') as f:
        passinfo = f.read().strip()
    (host, user, dbname, password, port) = passinfo.split()
    if os.path.isfile(passfile):
        return (True, (host, user, dbname, password, port))
    return (False, None)

class TestPostgreSQL(unittest.TestCase):

    def test_postgresql_connect(self):
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


if __name__ == '__main__':
    unittest.main()