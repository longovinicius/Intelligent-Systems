from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random
import time


XMPP_LOGIN = "longovinicius@yax.im"
XMPP_PASSWORD = "XMPPpassword."


def gen_coefs(scale, degree):
    # coeficientes que garantem raiz na funcao
    a = random.randint(-scale, scale)
    b = random.randint(-scale, scale)
    c = random.randint(-scale, scale)
    d = random.randint(-scale, scale)

    if degree == 1:  # a != 0
        while a == 0:
            a = random.randint(-scale, scale)
        return a, b, None, None

    if degree == 2:  # delta >= 0
        delta = b**2 - 4*a*c
        while delta < 0 or a == 0:
            a = random.randint(-scale, scale)
            delta = b**2 - 4*a*c
        return a, b, c, None

    if degree == 3:  # delta >= 0
        while True:
            a = random.randint(-scale, scale)
            delta = 18*a*b*c*d - 4*b**3*d + b**2*c**2 - 4*a*c**3 - 27*a**2*d**2
            if delta >= 0 and a != 0:
                break
        return a, b, c, d


class Gerador(Agent):
    funcao_grau = 0
    a, b, c, d = 0, 0, 0, 0

    class funcao_1grau(CyclicBehaviour):
        async def run(self):
            #print(f"Rodando funcao {Gerador.funcao_grau} grau")
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)
                y = float(Gerador.a*x + Gerador.b)
                print("Enviou para " + str(res.sender) +
                      " f(", res.body, ") = ", int(y))  # y = ax + b
                msg = Message(to=str(res.sender))
                msg.set_metadata("performative", "inform")
                msg.body = str(int(y))
                await self.send(msg)

    class funcao_2grau(CyclicBehaviour):
        async def run(self):
            #print(f"Rodando funcao {Gerador.funcao_grau}grau")
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)
                y = float(Gerador.a*x**2 + Gerador.b*x + Gerador.c)
                print("Enviou para " + str(res.sender) +
                      " f(", res.body, ") = ", int(y))  # y = ax^2 + bx + c
                msg = Message(to=str(res.sender))
                msg.set_metadata("performative", "inform")
                msg.body = str(int(y))
                await self.send(msg)

    class funcao_3grau(CyclicBehaviour):
        async def run(self):
            #print(f"Rodando funcao {Gerador.funcao_grau}grau")
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)
                y = float(Gerador.a*x**3 + Gerador.b*x **
                          2 + Gerador.c*x + Gerador.d)
                print("Enviou para " + str(res.sender) +
                      " f(", res.body, ") = ", int(y))  # y = ax^2 + bx^2 + cx + d
                msg = Message(to=str(res.sender))
                msg.set_metadata("performative", "inform")
                msg.body = str(int(y))
                await self.send(msg)

    class tipo_funcao(CyclicBehaviour):
        async def run(self):
            #print("Rodando Tipo Funcao")
            msg = await self.receive(timeout=5)
            if msg:
                msg = Message(to=str(msg.sender))
                msg.set_metadata("performative", "inform")
                # msg.set_metadata(outro)
                msg.body = f"{Gerador.funcao_grau} grau"
                await self.send(msg)
                print("Respondeu para " + str(msg.sender) + " com " + msg.body)

    async def setup(self):

        degree = random.randint(1, 3)
        Gerador.funcao_grau = degree
        Gerador.a, Gerador.b, Gerador.c, Gerador.d = gen_coefs(
            100, Gerador.funcao_grau)
        print(f"Grau: {Gerador.funcao_grau}")
        print(f"Coefs: {Gerador.a, Gerador.b, Gerador.c, Gerador.d}")

        if degree == 1:
            tf = self.funcao_1grau()
        elif degree == 2:
            tf = self.funcao_2grau()
        else:
            tf = self.funcao_3grau()

        t1 = Template()
        t1.set_metadata("performative", "subscribe")
        # Vincula template performativo/subscribe a funcao tf informada
        self.add_behaviour(tf, t1)

        ft = self.tipo_funcao()
        t2 = Template()
        t2.set_metadata("performative", "request")
        self.add_behaviour(ft, t2)


gerador = Gerador(XMPP_LOGIN, XMPP_PASSWORD)
# gerador.web.start(hostname="127.0.0.1", port="10000")
# gerador.start()

res = gerador.start()
res.result()

while gerador.is_alive():
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        gerador.stop()
        break
print("Agente encerrou!")
