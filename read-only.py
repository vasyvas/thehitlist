import sqlite3
import commands

# Core data times are not Unix times. They start at January 1st 2001 GMT
# http://stackoverflow.com/questions/11388461
NSTIMEINTERVAL = 978307200

# Read the file path from the system defaults so that we don't need to hardcode
# a path in here
SQL_FILE = commands.getoutput('defaults read com.potionfactory.TheHitList libraryURL').strip()
#SQL_FILE = SQL_FILE.replace('file://localhost', '')
#SQL_FILE = SQL_FILE.replace('%20', ' ')
SQL_FILE += '/library.sqlite3'

SQL_STATEMENT = '''
SELECT ZTITLE, ZSTARTDATE, ZDUEDATE FROM ZTASK
WHERE ZCOMPLETEDDATE is NULL
AND ZDUEDATE < (strftime('%%s', date('now')) - %(offset)s)
''' % {
    'offset': NSTIMEINTERVAL
}

conn = sqlite3.connect(SQL_FILE)

c = conn.cursor()

for row in c.execute(SQL_STATEMENT):
    print row[0].encode('utf8', 'replace')