from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random


class Gerador(Agent):
    x = random.randint(-1000, 1000)
    a = 0
    while a == 0:
        a = random.randint(-100, 100)
    y = -1 * (a*x)

    class funcao_1grau(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)
                x = float(Gerador.a*x + Gerador.y)
                print("Enviou para " + str(res.sender) +
                      " f(", res.body, ")= ", x, "=>", int(x))
                msg = Message(to=str(res.sender))
                msg.set_metadata("performative", "inform")
                msg.body = str(int(x))
                await self.send(msg)

    class tipo_funcao(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                msg = Message(to=str(msg.sender))
                msg.set_metadata("performative", "inform")
                msg.body = "1grau"
                await self.send(msg)
                print("Respondeu para" + str(msg.sender) + " com " + msg.body)

    async def setup(self):
        t = Template()
        t.set_metadata("performative", "subscribe")

        tf = self.funcao_1grau()
        print("Funcao de 1o grau: ", Gerador.x)
        print("Funcao: ", Gerador.a, "x + (", Gerador.y, ")")

        self.add_behaviour(tf, t)

        ft = self.tipo_funcao()
        template = Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(ft, template)


gerador = Gerador("aulaufsc@jix.im", "digite_senha")
gerador.web.start(hostname="127.0.0.1", port="10000")
gerador.start()
