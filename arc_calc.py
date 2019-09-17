import math
from scipy.optimize import newton


class CircleArc:
    fields = {
        'radius',
        'sagitta',
        'chord',
        'length',
        'angle'
    }

    def __init__(self, **kwargs):

        if len(kwargs) != 2 or not set(kwargs.keys()).issubset(self.fields):
            raise Exception(f"Keyword arguments must be two of: {', '.join(self.fields)}")

        self._results = kwargs

    def _angle(self):
        if self._results.get('angle') is not None:
            return

        radius = self._results.get('radius')
        chord = self._results.get('chord')
        length = self._results.get('length')

        if radius and chord:
            self._results['angle'] = 2 * math.asin((chord / 2) / radius)

        elif radius and length:
            self._results['angle'] = length / radius

    def _chord(self):
        if self._results.get('chord') is not None:
            return

        radius = self._results.get('radius')
        sagitta = self._results.get('sagitta')
        angle = self._results.get('angle')

        if radius and sagitta:
            self._results['chord'] = 2 * math.sqrt(radius ** 2 - (radius - sagitta) ** 2)

        elif angle and radius:
            self._results['chord'] = 2 * math.sin(angle / 2) * radius

    def _length(self):
        if self._results.get('length') is not None:
            return

        radius = self._results.get('radius')
        angle = self._results.get('angle')

        if angle and radius:
            self._results['length'] = angle * radius

    def _radius(self):
        if self._results.get('radius') is not None:
            return

        angle = self._results.get('angle')
        chord = self._results.get('chord')
        length = self._results.get('length')
        sagitta = self._results.get('sagitta')

        if sagitta and angle:
            self._results['radius'] = (
                    sagitta / (1 - math.cos(angle / 2))
            )

        elif sagitta and length:
            self._results['radius'] = newton(
                lambda r: math.cos(length / (2 * r)) - ((r - sagitta) / r),
                length / math.pi
            )

        elif chord and length:
            self._results['radius'] = newton(
                lambda r: (math.sin((length / 2) / r) - ((chord / 2) / r)),
                length / math.pi
            )

        elif sagitta and chord:
            self._results['radius'] = (sagitta ** 2 + (chord / 2) ** 2) / (2 * sagitta)

    def _sagitta(self):
        if self._results.get('sagitta') is not None:
            return

        chord = self._results.get('chord')
        radius = self._results.get('radius')

        if radius and chord:
            self._results['sagitta'] = radius - math.sqrt(
                radius ** 2 - (chord / 2) ** 2
            )

    def calc(self):
        while len(self._results) < 5:
            for func in [
                self._angle,
                self._chord,
                self._length,
                self._radius,
                self._sagitta
            ]:
                func()

        if self._results['sagitta'] > self._results['radius']:
            self._results['angle'] = (math.pi * 2) - self._results['angle']
            self._results['length'] = (
                (math.pi * 2 * self._results['radius'])  - self._results['length']
            )

        return {k: round(v, 4) for k, v in self._results.items()}

