from ..bus.message_broker.broker import MessageBroker


class MessageBrokerContext:
    _instance = None

    def __init__(self):
        self.context: MessageBroker = MessageBroker()


    @classmethod
    def instance(cls) -> "MessageBrokerContext":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
