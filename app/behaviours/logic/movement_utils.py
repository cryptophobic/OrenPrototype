from app.behaviours.types import BufferedMoverState
from app.config import CommonAnimations
from app.core.geometry.types import Directions
from app.core.vectors import CustomVec2i, CustomVec2, CustomVec2f
from app.engine.message_broker.types import Message, MessageBody, MessageTypes, PushedByPayload, Payload
from app.protocols.engine.grid.grid_protocol import GridProtocol
from app.protocols.engine.message_broker.broker_protocol import MessageBrokerProtocol
from app.protocols.objects.coordinate_holder_protocol import CoordinateHolderProtocol
from app.protocols.objects.unit_protocol import UnitProtocol
from app.registry.animation_registry import LoadedAnimation


class MovementUtils:
    
    def __init__(self, grid: GridProtocol, messenger: MessageBrokerProtocol):
        self._grid = grid
        self._messenger = messenger

    def calculate_buffered_move(
            self,
            coordinate_holder: CoordinateHolderProtocol,
            state: BufferedMoverState,
            delta_time: float,
    ) -> tuple[BufferedMoverState, CustomVec2i]:
        moving_buffer = state.moving_buffer.copy()
        moving_buffer += (coordinate_holder.velocity + state.intent_velocity_normalised) * delta_time
        direction = CustomVec2i.zero()

        for n in [CustomVec2f.X, CustomVec2f.Y]:
            direct = CustomVec2f.zero()
            direct[n] = moving_buffer[n]
            if not self.pretend_to_move(coordinate_holder, direct, state.clear_velocity, 1):
                moving_buffer[n] = 0.0

            elif abs(moving_buffer[n]) >= 1.0:
                step = int(moving_buffer[n])
                direction[n] += step
                moving_buffer[n] -= step
                if state.clear_velocity[n]:
                    moving_buffer[n] = 0.0
                    state.intent_velocity[n] = 0
                    state.intent_velocity_normalised[n] = 0

        state.moving_buffer = moving_buffer

        return state, direction

    def inform_about_occupation(self, coordinate_holder, result, direction=None, force=1):
        if direction is not None:
            for actor in result.blocked:
                message = Message(
                    sender=coordinate_holder.name,
                    body=MessageBody(
                        message_type=MessageTypes.PUSHED_BY,
                        payload=PushedByPayload(
                            direction=direction,
                            force=force,
                        )
                    )
                )
                self._messenger.send_message(message, actor)

        for actor in result.overlapped:
            message = Message(
                sender=coordinate_holder.name,
                body=MessageBody(
                    message_type=MessageTypes.OVERLAPPED_BY,
                    payload=Payload(),
                )
            )
            self._messenger.send_message(message=message, responder=actor)

    def pretend_to_move(self, coordinate_holder: CoordinateHolderProtocol, intent_velocity: CustomVec2f, clear_velocity: CustomVec2i, force: int) -> bool:

        def sign(value):
            return (value > 0) - (value < 0)

        direction = CustomVec2i(
            0 if clear_velocity.x == 1 else sign(intent_velocity.x),
            0 if clear_velocity.y == 1 else sign(intent_velocity.y),
        )

        if direction.is_not_zero():
            to_place = coordinate_holder.coordinates + direction
            result = self._grid.is_may_be_occupied(coordinate_holder, to_place)
            self.inform_about_occupation(coordinate_holder, result, direction, force)
            return result.placed

        return True

    def try_place(self, coordinate_holder: CoordinateHolderProtocol, to_place: CustomVec2i) -> bool:
        result = self._grid.place(coordinate_holder, to_place)
        self.inform_about_occupation(coordinate_holder, result)

        return result.placed


    def try_move(self, coordinate_holder: CoordinateHolderProtocol, direction: CustomVec2i, force: int) -> bool:
        result = self._grid.move(coordinate_holder, coordinate_holder.coordinates + direction)
        self.inform_about_occupation(coordinate_holder, result, direction, force)

        return result.placed

    @staticmethod
    def get_animation_and_textures(velocity: CustomVec2, unit: UnitProtocol) -> tuple[CommonAnimations, Directions]:

        if velocity.y < 0:
            animation = CommonAnimations.RUN
            direction = Directions.FRONT
        elif velocity.y > 0:
            animation = CommonAnimations.RUN
            direction = Directions.BACK
        elif velocity.x < 0:
            animation = CommonAnimations.RUN
            direction = Directions.LEFT
        elif velocity.x > 0:
            animation = CommonAnimations.RUN
            direction = Directions.RIGHT
        else:
            direction = unit.shape.direction
            animation = CommonAnimations.IDLE

        return animation, direction
