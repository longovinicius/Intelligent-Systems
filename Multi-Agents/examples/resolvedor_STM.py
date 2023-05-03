import time
import random
import numpy as np
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

STATE_ONE = "GET_TYPE"
STATE_TWO = "RESOLVER"

XMPP_RECEIVER = "longovinicius@yax.im"
XMPP_SENDER = "lucastt@yax.im"
XMPP_PASSWORD = "XMPPpassword."

tipo_fc = 0

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
            tipo_fc = int(res.body)
            self.set_next_state(STATE_TWO)

# y = 5X + 1, X1 = 0, y = 1, X2 = 1, y = 6...


class Resolver(State):
    async def run(self):
        resolvido = False
        a, b, c, d = 0
        R0, R1, R2, R3 = 0

        print("Encontrou Tipo de Funcao")
        x = 0
        # Instantiate the message to Gerador
        msg = Message(to=XMPP_RECEIVER)
        msg.set_metadata("performative", "subscribe")
        msg.body = str(int(x))
        await self.send(msg)

        res = await self.receive(timeout=5)
        if res:
            print(f"Valor de y recebido = {int(res.body)}")
            if int(res.body) == 0:
                print(f"Resolvido com x = {x}!!!!")
                resolvido = True
            else:
                print(f"Errado em x = {x} Keep trying...")
                R0 = int(res.body)

        x = 1
        # Instantiate the message to Gerador
        msg = Message(to=XMPP_RECEIVER)
        msg.set_metadata("performative", "subscribe")
        msg.body = str(int(x))
        await self.send(msg)

        res = await self.receive(timeout=5)
        if res:
            print(f"Valor de y recebido = {int(res.body)}")
            if int(res.body) == 0:
                print(f"Resolvido com x = {x}!!!!")
                resolvido = True
            else:
                print(f"Errado em x = {x} Keep trying...")
                R1 = int(res.body)
        if tipo_fc == 1:
            b = R0
            a = R1 - R0
            x = np.roots([a, b])[0]

        # Instantiate the message to Gerador
        msg = Message(to=XMPP_RECEIVER)
        msg.set_metadata("performative", "subscribe")
        msg.body = str(float(x))
        await self.send(msg)

        res = await self.receive(timeout=5)
        if res:
            print(f"Valor de y recebido = {int(res.body)}")
            if int(res.body) == 0:
                print(f"Resolvido com x = {x}!!!!")
                resolvido = True
            else:
                print(f"Errado em x = {x} Keep trying...")


class FSMAgent(Agent):
    async def setup(self):
        fsm = ExampleFSMBehaviour()
        fsm.add_state(name=STATE_ONE, state=Get_type(), initial=True)
        fsm.add_state(name=STATE_TWO, state=Resolver())
        fsm.add_transition(source=STATE_ONE, dest=STATE_TWO)
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
