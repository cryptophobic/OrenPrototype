from app.behaviours.behaviour import register_message_handler, Behaviour
from app.config import Behaviours
from app.core.types import KeyPressEventLogRecord
from app.engine.message_broker.types import MessageTypes, MessageBody, InputPayload, Message, ControlsPayload
from app.protocols.objects.orchestrator_protocol import OrchestratorProtocol


@register_message_handler(
    MessageTypes.INPUT,
    {
        OrchestratorProtocol: "input",
    }
)

class InputHandler(Behaviour):
    name = Behaviours.INPUT_HANDLER
    supported_receivers = (OrchestratorProtocol,)

    @classmethod
    def __input_process(cls, orchestrator: OrchestratorProtocol, payload: InputPayload) -> bool:
        if not isinstance(payload, InputPayload):
            raise TypeError(f"Expected InputPayload, got {type(payload)}")

        puppeteers = orchestrator.get_puppeteers()
        messenger = cls.get_messenger()
        sent = False
        for log_record in payload.input: # type: KeyPressEventLogRecord
            for subscriber in log_record.subscribers_set:
                puppeteer = puppeteers.get(subscriber)
                if puppeteer:
                    sent = True
                    message = Message(
                        sender=orchestrator.name,
                        body=MessageBody(
                            message_type=MessageTypes.KEY_DOWN if log_record.down is True else MessageTypes.KEY_UP,
                            payload=ControlsPayload(key_code=log_record.key)
                        )
                    )
                    _, response_actions = messenger.send_message(message, puppeteer)
                    if response_actions:
                        puppeteer.pending_actions.extend(response_actions)


        return sent

    @classmethod
    def input(cls, orchestrator: OrchestratorProtocol, payload: InputPayload) -> bool:
        return cls.__input_process(orchestrator, payload)
