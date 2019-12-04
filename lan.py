import Node
import time
import collections
import WAN
 
class LAN:
	def __init__(self, nodeList):
		self.numCollisions = 0
		self.band = -100
		self.nodes = nodes
		self.numNodes= len(self.nodes)
 
	#used to call operation method of the particular node. 
	#once operation begin, collDetect checks if collision in network
	def run(self, wan):
		for i in range(self.numNodes):
			self.nodes[i].operation(wan)
			print("---")
			self.collDetect()
 
	#checks if collision in network based on node state
	def collDetect(self):
		coll = []
		for i in range(self.numNodes):
			if self.nodes[i].status = "Transmitting":
				colls.append(i)
			if len(coll) >= 2:
				self.numCollisions = self.numCollisions+1
				if self.nodes[i].id.startswith("R"):
					self.nodes[i].stopTransmit("Collision")
				else:
					self.nodes[i].stopTransmit("Collision") 
