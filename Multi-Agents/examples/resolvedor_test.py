from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade.message import Message
import random
import time

class Resolvedor(Agent):

	function_grau = 0

	class Get_type(OneShotBehaviour):
		async def run(self):
			print("InformBehav running")
			msg = Message(to="receiver@your_xmpp_server")     # Instantiate the message to Gerador
			msg.set_metadata("performative", "request")  # Set the "inform" FIPA performative
			msg.body = "PASSA O GRAU"                    # Set the message content

			await self.send(msg)
			print("Message sent!")

			res = await self.receive(timeout=10)
			if res:
				print("Message received!")
				Resolvedor.function_grau = res[0]  # msg.body = f"{self.tipo_funcao}grau" 
				print("function type: ",res[0])
	
	class Resolver(CyclicBehaviour):
		async def run(self):
			if Resolvedor.function_grau:
				x = random.randint(-100, 100)
				msg = Message(to="receiver@your_xmpp_server") # Instantiate the message to Gerador
				msg.set_metadata("performative", "subscribe")
				msg.body = str(int(x))
				await self.send(msg)
			
				res = await self.receive(timeout=5)
				if res:
					if int(res) == 0:
						print("Resolvido!!!!")
						pass 
					else:
						print("Errado!!! Keep trying...")
		
	async def setup(self):
		print("SenderAgent started")
		gt = self.Get_type()

		template = Template()
		template.set_metadata("performative", "inform")

		self.add_behaviour(gt, template)

		r = self.Resolver()
		template = Template()
		template.set_metadata("performative", "inform")

if __name__ == "__main__":
	senderagent = Resolvedor("sender@your_xmpp_server", "sender_password")
	senderagent.start()