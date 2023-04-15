from spade import agent, quit_spade
import time


class DummyAgent(agent.Agent):
    async def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))


dummy = DummyAgent("longovinicius@jix.im", "Jixpassword.")
future = dummy.start()

future.result()
# while future.is_alive():
#     try:
#         time.sleep(1)
#     except KeyboardInterrupt:
#         future.stop()
#         break
# print("Agente encerrou!")
dummy.stop()
quit_spade()
