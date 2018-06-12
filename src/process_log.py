from csv import DictReader
from lru_queue import LRUQueue
from datetime import datetime
from session import Session


'''
The main LogProcessor class, that processes the log data as a stream and handles the LRUQueue and the set of active sessions
'''
class LogProcessor:
    def __init__(self):
        self.sessions = {}
        self.lru_queue = LRUQueue(self.get_inactivity_period())

    '''
    To efficiently process multiple updates occuring within a single second, we cache all the updates for a single second,
    squash multiple updates for a particula IP into a single update and batch process the entire data for a particular second in one shot.
    '''
    def process_log(self):
        stream = self.get_log_stream()
        next_line = next(stream)
        with open('output/sessionization.txt', 'w+') as f:
            while next_line:
                batch_lines, batch_sessions, new_line = [], set(), None
                expired_sessions = self.lru_queue.get_expired_sessions(self.get_datetime(next_line))
                self.handle_expired_sessions(expired_sessions, f)
                batch_lines.append(next_line)

                temp_next_line = None
                for new_line in stream:
                    if self.get_datetime(next_line) != self.get_datetime(new_line):
                        temp_next_line = new_line
                        break
                    batch_lines.append(new_line)
                next_line = temp_next_line

                for log_line in batch_lines:
                    ip = log_line['ip']
                    access_time = self.get_datetime(log_line)
                    session = self.get_updated_session(ip, access_time)
                    batch_sessions.add(session)
                self.lru_queue.update(batch_sessions)

            self.handle_expired_sessions(list(self.sessions.values()), f)

    '''Retrieve a session for an ip, if it is already active, or create a new one'''
    def get_updated_session(self, ip, access_time):
        if ip not in self.sessions:
            self.sessions[ip] = Session(ip, access_time)
        self.sessions[ip].last_accessed = access_time
        self.sessions[ip].count += 1
        return self.sessions[ip]

    '''Get the list of expired sessions as input, update the active set of sessions and write to the output'''
    def handle_expired_sessions(self, expired_sessions, f):
        for session in expired_sessions:
            self.sessions.pop(session.ip)
            self.write_session_to_output(session, f)


    @staticmethod
    def get_datetime(log_line):
        return datetime.strptime(log_line['date'] + ' ' + log_line['time'], "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_inactivity_period():
        try:
            with open('input/inactivity_period.txt', 'r') as f:
                return int(f.readline())
        except IOError as e:
            print(e)
            raise e

    @staticmethod
    def get_log_stream():
        try:
            with open('input/log.csv', 'r') as f:
                for line in DictReader(f):
                    yield line
        except IOError as e:
            print(e)
            raise e

    @staticmethod
    def write_session_to_output(session, file):
        out = session.ip + ',' + str(session.start) + ',' + str(session.last_accessed) + ',' + str(int((session.last_accessed - session.start).total_seconds() + 1)) + ',' + str(session.count) + '\n'
        file.write(out)

if __name__ == '__main__':
    LogProcessor().process_log()