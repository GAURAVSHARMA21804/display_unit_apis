# connection_verifier.py
import threading
import time

class ConnectionVerifier(threading.Thread):
    def __init__(self, connection):
        super(ConnectionVerifier, self).__init__()
        self.connection = connection
        self._stopped = False

    def run(self):
        while not self._stopped:
            # print("###################################################")
            if not self.connection.is_connected():
                # print("#########################@#*^@^$@&$(&@(&(@&($&(@&$(#*&$&#*$&*#&*$&#*&$*#&*$&##########################")
                self.connection.reconnect()
            time.sleep(4)  # Check every 60 seconds

    @property
    def stopped(self):
        return self._stopped

    @stopped.setter
    def stopped(self, value):
        self._stopped = value
