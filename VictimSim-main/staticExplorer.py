class staticExplorer:
    total = 0
    agentes = 0

    @staticmethod
    def agentArrived():
        staticExplorer.total += 1

    @staticmethod
    def addAgent():
        staticExplorer.agentes += 1

    @staticmethod
    def checked():
        return staticExplorer.total == staticExplorer.agentes
