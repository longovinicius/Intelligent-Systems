from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random
import time

# ax + y
class Gerador(Agent):
	rand = random.randint(-1000, 1000)
	a = 0
	while a == 0:
		a = random.randint(-100, 100)
	b = -1 * (a*rand)


	class funcao_1grau(CyclicBehaviour):
		async def run(self):
			res = await self.receive(timeout=5)
			if res:
				x = float(res.body)
				y = float(Gerador.a*x + Gerador.b)
				print("Enviou para " + str(res.sender) +
					  " f(", res.body, ")= ", x, "=>", int(x)) # y = ax + b
				msg = Message(to=str(res.sender))
				msg.set_metadata("performative", "inform")
				msg.body = str(int(y))
				await self.send(msg)

	class funcao_2grau(CyclicBehaviour):
		pass    
	
	class funcao_3grau(CyclicBehaviour):
		pass

	class tipo_funcao(CyclicBehaviour):
		async def run(self):
			msg = await self.receive(timeout=5)
			if msg:
				msg = Message(to=str(msg.sender))
				msg.set_metadata("performative", "inform")
				msg.body = f"{self.tipo_funcao}grau"
				await self.send(msg)
				print("Respondeu para" + str(msg.sender) + " com " + msg.body)

	async def setup(self):
		t = Template()
		t.set_metadata("performative", "subscribe")

		tf = self.funcao_1grau()
		print("Funcao de 1o grau: ", Gerador.rand)
		print("Funcao: ", Gerador.a, "x + (", Gerador.b, ")")

		self.add_behaviour(tf, t)

		ft = self.tipo_funcao()
		template = Template()
		template.set_metadata("performative", "request")
		self.add_behaviour(ft, template)


gerador = Gerador("longovinicius@jix.im", "Jixpassword.")
gerador.web.start(hostname="127.0.0.1", port="10000")
gerador.start()

res = gerador.start()
res.result()

while gerador.is_alive():
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		gerador.stop()
		break
print("Agente encerrou!")
