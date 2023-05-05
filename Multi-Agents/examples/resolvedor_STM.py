import time
import random
import numpy as np
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

STATE_ONE = "GET_TYPE"
STATE_TWO = "PERGUNTADOR"
STATE_THREE = "CALCULATOR"

XMPP_RECEIVER = "longovinicius@yax.im"
XMPP_SENDER = "lucastt@yax.im"
XMPP_PASSWORD = "XMPPpassword."

tipo_fc = 0

A = []
B = []

x_teste = 0
y_infos = 0
solved = False

class ExampleFSMBehaviour(FSMBehaviour):
	async def on_start(self):
		print(f"FSM starting at initial state {self.current_state}")

	async def on_end(self):
		print(f"FSM finished at state {self.current_state}")
		await self.agent.stop()


class Get_type(State):

	async def run(self):
		global tipo_fc
		print("InformBehav running")
		# Instantiate the message to Gerador
		msg = Message(to=XMPP_RECEIVER)
		# Set the "inform" FIPA performative
		msg.set_metadata("performative", "request")
		msg.body = "PASSA O GRAU"                    # Set the message content
		print(f"msg.body: {msg.body}")
		await self.send(msg)
		print("Message sent!")

		res = await self.receive(timeout=10)
		print(f"Res Get_type_body(): {res.body}")
		if res:
			print("Message received!")
			# msg.body = f"{self.tipo_funcao}grau"
			# Resolvedor.function_grau = res[-1]
			print(f"res.body: {res.body}")
			tipo_fc = int((res.body)[0])
			self.set_next_state(STATE_TWO)

# y = 5X + 1, X1 = 0, y = 1, X2 = 1, y = 6...


class Perguntador(State):
	async def run(self):
		#print("Encontrou Tipo de Funcao")
		# Instantiate the message to Gerador
		msg = Message(to=XMPP_RECEIVER)
		msg.set_metadata("performative", "subscribe")
		msg.body = str(int(x_teste))
		await self.send(msg)
		# !  COMO VER SE TIMEOUT ACONTECEU?????
		#res = await self.receive(timeout=10)
		res = None
		while not res:
			res = await self.receive(timeout=10)
		if res:
			print(f"Valor de y recebido = {int(res.body)} x = {x_teste}")
			if int(res.body) == 0:
				print(f"Resolvido com x = {x_teste}!!!!")  # !TERMINAR O AGENTE
				await fsmagent.stop()
			else:
				print(f"Errado em x = {x_teste} Keep trying...")
				R = int(res.body)  # ! MUDEI PARA INT

		B.append(R)
		self.set_next_state(STATE_THREE)


class Calculator(State):
	async def run(self):
		global x_teste,tipo_fc,A,B,y_infos,solved
		num_elements = []
		for y in range(tipo_fc + 1):
			num_elements.append(x_teste**(tipo_fc-y))
		A.append(num_elements)

		if y_infos == (tipo_fc):
			M_cofs = np.array(A)
			M_consts = np.array(B)
			generator_function = np.linalg.solve(M_cofs, M_consts)
			soluction = np.roots(generator_function)[0]
			msg = Message(to=XMPP_RECEIVER)
			msg.set_metadata("performative", "subscribe")
			msg.body = str(float(soluction))
			await self.send(msg)

			res = await self.receive(timeout=10)
			if res:
				print(f"Valor de y recebido = {int(res.body)}")
				if int(res.body) == 0:
					print(f"Resolvido com x = {soluction}!!!!")
					solved = True
					await fsmagent.stop()
				else:
					print(f"SOU BURRO")
					await fsmagent.stop()
		x_teste = x_teste + 1
		y_infos = y_infos + 1
		if not solved:
			self.set_next_state(STATE_TWO)


class FSMAgent(Agent):
	async def setup(self):
		fsm = ExampleFSMBehaviour()
		fsm.add_state(name=STATE_ONE, state=Get_type(), initial=True)
		fsm.add_state(name=STATE_TWO, state=Perguntador())
		fsm.add_state(name=STATE_THREE, state=Calculator())
		fsm.add_transition(source=STATE_ONE, dest=STATE_TWO)
		fsm.add_transition(source=STATE_TWO, dest=STATE_THREE)
		fsm.add_transition(source=STATE_THREE, dest=STATE_TWO)
		self.add_behaviour(fsm)


if __name__ == "__main__":
	fsmagent = FSMAgent(XMPP_SENDER, XMPP_PASSWORD)
	future = fsmagent.start()
	future.result()

	while fsmagent.is_alive():
		try:
			time.sleep(1)
		except KeyboardInterrupt:
			fsmagent.stop()
			break
	print("Agent finished")
