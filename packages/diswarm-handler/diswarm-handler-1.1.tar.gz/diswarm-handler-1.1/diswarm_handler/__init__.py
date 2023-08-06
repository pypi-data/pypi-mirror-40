from DiSwarm import Swarm
import time

class Handler:
    def __init__(self, channel, token, swarm_id, bot_id, lead_timeout=5, role=None):
        self.swarm = Swarm(channel,token,swarm_id,bot_id)
        self.role = role
        if not self.role:
            self.swarm.send(str(['request-leader',(),None]))
            time.sleep(lead_timeout)
            q = self.swarm.get_queue()
            self.role = 'leader'
            for i in q:
                print(eval(i[1]))
                if eval(i[1])[0] == 'leader':
                    self.role = 'drone'
        print(self.role)
    def request(self, req, args=()):
        #print('s ' + str(req))
        self.swarm.send(str([req, tuple(args), self.role]))
    def process_one(self, response):
        response = eval(response)
        if response[0] == 'request-leader':
            self.request('leader')
        #print(response)
        return str(response[0]) + ' with args ' + ','.join(response[1]) + ' from a ' + str(response[2])
    def process(self):
        q = self.swarm.get_queue()
        responses = []
        for i in q:
            responses.append(self.process_one(eval(i[1])))
        return responses
