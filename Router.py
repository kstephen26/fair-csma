import Packet
# import WAN
from Node import Node as Node
import copy

class Router(Node):
    def __init__(self,id):
        super(Router, self).__init__(id)
        self.route_table = {}
        self.packet = (None,0)
        self.packetSize = 10
        self.curReceiver = None
        self.transmissionStartTime = 0
        self.packetCount = 0
        self.status
        self.buffer = []
        
    def update_table(self):
        return

    def add_packet(self, packet,packet_type):
        if packet_type == 'RTS':
            self.buffer.append((packet,2))
        else:
            self.buffer.append((packet,self.packetSize))

    def routing(self, packet):
        packet.mac = self.route_table[packet.ip]
        self.curReceiver = packet.mac

    def operation(self, wan):
        self.dijkstra(wan)

        print("Status of Router {} is {} ".format(self.id,self.status))
        if self.status == 'Ready' and len(self.buffer)>0:
            self.startTransmit(wan)
        elif self.status == 'Transmitting':
            if self.transmissionStartTime + wan.tt + self.curTP < wan.cur_time:
                self.status = "Ready"
                self.curReceiver = None
                self.transmissionStartTime = 0
                send_to = self.packet.mac
                self.packetCount+=1

                if send_to.startswith('R'):
                    idx = int(send_to[-1])-1
                    wan.router[idx].add_packet(self.packet,'RTS')
                    wan.router[idx].receivedPacketCount+=1
                else:
                    idx = ord(send_to) - ord('A')
                    wan.host[idx].receivedPacketCount+=1
                self.packet = None
        elif self.status == 'Collision':
            self.calcBackoffTime(wan)
            self.status = 'Waiting'
        elif self.status == 'Waiting' and self.backoffTime <= wan.cur_time:
            self.reStartTransmit(wan.cur_time)

    def avoidanceRun(self):
        while True:
            #will be randomly generated value here
            time.sleep(0.1)
            if self.status == 'Ready' and len(self.buffer)>0:
                self.startTransmit(wan)
             elif self.status == 'Transmitting':
                 if self.transmissionStartTime + wan.tt + self.curTP < wan.cur_time:
                    # more random num sleep time logic needs to go here
                    self.send('RTS')
                    rec = self.receive()
                    if rec == 'CTS':
                        while rec is not 'ACK':
                            self.send('DATA')
                            rec = self.receive()
                            break
                    # tries 3 times to send
                    if k >= 3:
                        break
                    k += 1


    def startTransmit(self, wan):
        self.packet = copy.deepcopy(self.buffer[0])
        del self.buffer[0]

        self.routing(self.packet)

        print("{} is sending to {}".format(self.id,self.curReceiver))
        self.status = 'Transmitting'
        self.transmissionStartTime = wan.cur_time
    
    def send(self, packet, idx):
        if packet == 'RTS':
            self.send_to_access_point('RTS', 'START', idx)
            time.sleep(self.transmissionStartTime)
            self.send_to_access_point('RTS', 'DONE', idx)
    
        elif packet == 'DATA':
            self.send_to_access_point('DATA', 'START', idx)
            time.sleep(self.transmissionStartTime)
            self.send_to_access_point('DATA', 'DONE', idx)

    def send_to_access_point(self, type, modififer=''):
        to_send = {
            'id': self.id,
            'type': type,
            'mod':modifier
        }
        wan.router[idx].add_packet(to_send)

    def receive(self):
        try:
            message = self.packet.get()
        except queue.Empty:
            return None
        if message == 'ACK':
            return 'ACK'
        elif message == 'NOACK':
            return None
        elif message == "NOCATS":
            return None
        return message

    def dijkstra(self, wan):
        class DijkstraNode:
            def __init__(self, id, cost, path):
                self.id = id
                self.cost = cost
                self.path = path

            def __cmp__(self, other):
                return cmp(self.cost, other.cost)

        end_nodes = ['A', 'B', 'C', 'D']
        nodes = [DijkstraNode(self.id, 0, [self.id])]
        visited = []
        while len(nodes) > 0:
            cur = min(nodes, key=lambda x: x.cost)
            # idx = nodes.index(cur)
            nodes.remove(cur)

            visited.append(cur.id)
            if cur.id in end_nodes:
                self.route_table[cur.id] = cur.path[1]
            else:
                for n, c in wan.graph[cur.id]:
                    if n in visited:
                        continue
                    else:
                        p = cur.path[:]
                        p.append(n)
                        flag = True
                        for i in nodes:
                            if i.id == n:
                                flag = False
                                if i.cost > cur.cost + c:
                                    i.cost = cur.cost + c
                        if flag:
                            temp = DijkstraNode(n, cur.cost + c, p)
                            nodes.append(temp)


