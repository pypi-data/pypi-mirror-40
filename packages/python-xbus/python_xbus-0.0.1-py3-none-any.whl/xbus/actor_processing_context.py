from .envelope_receiver import EnvelopeReceiver

from . import xbus_pb2


async def receive_envelope(conn, position, receiver):
    async for fragment in xbus_nrpc.EnvelopeStorageClient(conn).ReadEnvelope(
            position):
        await receiver.receive(fragment)


class ActorProcessingContext:
    def __init__(self, actor, request):
        self.actor = actor
        self.request = request
        self.success = False
        self.detached = False
        self.error = None

    def detach(self):
        self.detached = True

    async def success(self):
        self.success = True
        if self.detached:
            await self.actor.processing_success(self.request.context)

    async def error(self, err):
        self.error = err
        if self.detached:
            await self.actor.processing_end(self.request.context, str(err))

    def read_envelope(self, input_name):
        for input_ in self.request.inputs:
            if input_.name == input_name:
                receiver = EnvelopeReceiver(input_name, input_.envelope)
                if receiver.reception_status == xbus_pb2.EnvelopeAck.RECEIVING:
                    receiver.task = asyncio.ensure_future(
                        receive_envelope(self.conn, input_.position, receiver))
                return receiver

    async def read_envelope_complete(self, input_name, timeout):
        er = self.read_envelope(input_name)
        return await er.complete(timeout)
