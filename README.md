# A simple framework for Unix-domain-socket-based daemons

Features:
* A base class for a Unix-domain-based server (**Server**)
* A controller class for managing the daemon process (**ServerApp**):
  * start
  * stop
  * status
  * restart
  * log
* No root is required to run the process,
  Default working directory is *~/.ServerClassName* where *ServerClassName*
  is derived from *Server*
