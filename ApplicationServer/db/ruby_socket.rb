require 'socket'        # Sockets are in standard library
require 'sqlite3'

def socket()
  hostname = 'localhost'
  port = 9999
  db = SQLite3::Database.open "development.sqlite3"

  rs = db.execute("SELECT created_at from users WHERE id = 1")
  #rs1 = db1.q("SELECT * from users;")

  puts rs
  #puts rs1

  s = TCPSocket.open(hostname, port)
  s.write(rs)
  s.close                 # Close the socket when done
end
