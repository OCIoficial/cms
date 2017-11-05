#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2010-2012 Giovanni Mascellani <mascellani@poisson.phc.unipi.it>
# Copyright © 2010-2017 Stefano Maggiolo <s.maggiolo@gmail.com>
# Copyright © 2010-2012 Matteo Boscariol <boscarim@hotmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from cms.grading.ScoreType import ScoreTypeGroup


# Dummy function to mark translatable string.
def N_(message):
    return message


def find_first(lst, pred):
    for idx, val in enumerate(lst):
        if pred(val):
            return idx
    return len(lst)


def piecewise_linear_function(x, points):
    points = [[0, 0]] + points

    idx = find_first(points, lambda point: point[0] > x)

    if idx == len(points):
        return points[-1][1]

    x0 = points[idx - 1][0]
    x1 = points[idx][0]

    y0 = points[idx - 1][1]
    y1 = points[idx][1]

    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


class GroupPiecewiseLinear(ScoreTypeGroup):
    """The score of a submission is a function of the percentage P of correct cases.
    The function is defined piecewise as a continuous function depending on the interval
    on which P lies. In each interval the function is defined as a linear function.

    Parameters are [[m, t, [P1, S1], [P2, S2]], ... ] (see ScoreTypeGroup),
    (P1, S1), (P2, S2) ... are the points where the function changes slope.

    """

    def get_public_outcome(self, outcome, _):
        """See ScoreTypeGroup."""
        if outcome >= 1.0:
            return N_("Correct")
        return N_("Not correct")

    def reduce(self, outcomes, parameters):
        """See ScoreTypeGroup."""
        points = sorted(parameters[2:])
        P = sum(outcome >= 1.0 for outcome in outcomes) / len(outcomes)
        return piecewise_linear_function(P, points)
