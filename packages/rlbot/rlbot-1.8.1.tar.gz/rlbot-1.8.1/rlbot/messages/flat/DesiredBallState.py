# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers

class DesiredBallState(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsDesiredBallState(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = DesiredBallState()
        x.Init(buf, n + offset)
        return x

    # DesiredBallState
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # DesiredBallState
    def Physics(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from .DesiredPhysics import DesiredPhysics
            obj = DesiredPhysics()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def DesiredBallStateStart(builder): builder.StartObject(1)
def DesiredBallStateAddPhysics(builder, physics): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(physics), 0)
def DesiredBallStateEnd(builder): return builder.EndObject()
