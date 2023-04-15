from spade import agent, quit_spade


class DummyAgent(agent.Agent):
    async def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))


dummy = DummyAgent("longovinicius@jix.im", "Jixpassword.")
future = dummy.start()
future.result()

dummy.stop()
quit_spade()
