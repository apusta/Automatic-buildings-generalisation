class Scale:
    SCALE10K = '10000'
    SCALE25K = '25000'

class Mode:
    UNION = 'union'
    TYPIFICATION = 'typification'


class Context:
    def __init__(self, scale, mode):
        self.scale = self._set_scale(scale)
        self.mode = self._set_mode(mode)

    def _set_scale(self, scale):
        if scale == Scale.SCALE10K or scale == Scale.SCALE25K:
            return scale

        raise Exception('use proper scale!')

    def _set_mode(self, mode):
        if mode == Mode.UNION or mode == Mode.TYPIFICATION:
            if self.scale == Scale.SCALE10K and mode == Mode.TYPIFICATION:
                raise Exception('with 10k scale you can use only union mode')
            return mode

        raise Exception('use proper mode')
