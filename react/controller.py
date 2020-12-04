import sqlite3
import os
conn = sqlite3.connect( os.path.join( os.path.dirname( __file__ ) + '\\reaction.db' ) )

print( os.path.join( os.path.dirname( __file__ ) + '\\reaction.db' ) )

c = conn.cursor()

c.execute( "CREATE TABLE IF NOT EXISTS single_role (msg integer, emoji text, role integer)" )

#conn.commit()

#c.execute( "INSERT INTO single_role VALUES ('123456789','王小寶','321654879')" )
#c.execute( "INSERT INTO single_role VALUES ('984351168','吳有明','416846615')" )
#c.execute( "INSERT INTO single_role VALUES ('135416846','白采君','168135123')" )

#conn.commit()
#c.execute( 'DELETE FROM single_role' )

for row in c.execute( 'SELECT * FROM ind ORDER BY msg' ):
    print( row )

for row in c.execute(
        "SELECT * FROM single_role WHERE msg=782510126119518230 AND emoji='<:black_question:782510826224353320>'" ):
    print( 'OC => ' + str( row ) )

conn.close()
