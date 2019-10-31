require 'socket'        # Sockets are in standard library
require 'sqlite3'

def socket()
  hostname = 'localhost'
  port = 9999
  db = SQLite3::Database.open "development.sqlite3"

  maxId = db.execute "SELECT MAX(id) FROM users"
  stm = db.prepare "SELECT key FROM active_storage_blobs WHERE id=?"

  #stm.bind_param 1, maxId[0][0]
  stm.bind_param 1, 3
  rs = stm.execute

  row = rs.next

  puts row

  s = TCPSocket.open(hostname, port)
  s.write(row)
  s.close                 # Close the socket when done
end

#socket()
