import time

class Timer():

    def start(self):
        self.partial_time = self.genesis_time = time.time_ns()

    def from_start(self, description=''):
        now = time.time_ns()
        print(description, (now-self.genesis_time)/1000000000, 'Seconds')

    def partial(self, description=''):
        now = time.time_ns()
        print(description, (now-self.partial_time)/1000000000, 'Seconds')
        self.partial_time = time.time_ns()


