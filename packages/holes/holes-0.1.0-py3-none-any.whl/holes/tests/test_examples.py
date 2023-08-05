import numpy
from ..ret import stress_from_line, ret, slow_angle


def test_vertical_line():
    "Check stress calculation for vertical line"
    x, y = numpy.meshgrid(numpy.linspace(-2000, 2000, num=40),
                          numpy.linspace(-4000, 4000, num=80))

    σ_xx, σ_xy = stress_from_line(
        x1=0, y1=-1000, x2=0, y2=1000, P=5, a=1, λ=1/10, x=x, y=y)
    actual_ret = ret(σ_xx, σ_xy, C=3, L=1)
    # TO DO
    actual_theta = slow_angle(σ_xx, σ_xy)
    assert numpy.max(actual_theta) <= numpy.pi/2
