from augustus.system.metabase_env import augustusEnvBase


class RiskManagerBase(augustusEnvBase):

    def __init__(self):
        self.env.risk_managers.update({self.__class__.__name__: self})

    def run(self):
        pass


