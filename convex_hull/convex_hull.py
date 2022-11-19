# %%

import numpy as np
import matplotlib.pyplot as plt
from shapely import geometry


# %%

class ConvexHull:
    def __init__(self) -> None:
        pass

    # Return -ve for right turn
    def __angle_between(self, v0: np.array, v1: np.array): return np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))

    def __incremental_tangent(self, pol1, pol2, leftInd: int, rightInd: int, offset: bool = 1):
        """
        Gives lower (offset = 1) and upper (offset = -1) tangent
        Points should be in clockwise order
        """
        while True:
            if self.__angle_between((pol1[leftInd])-(pol1[(leftInd-offset)%len(pol1)]), (pol2[rightInd])-(pol1[leftInd]))*offset < 0:
                leftInd -= offset
                leftInd %= len(pol1)
            elif self.__angle_between((pol2[rightInd])-(pol1[leftInd]), (pol2[(rightInd+offset)%len(pol2)])-(pol2[rightInd]))*offset < 0:
                rightInd += offset
                rightInd %= len(pol2)
            else:
                break

        return leftInd, rightInd

    def __remove_colinear(self, points: list):
        points.insert(0, points[len(points)-1])
        points.append(points[1])

        filtered = []
        for i in range(1, len(points)-1):
            ang = self.__angle_between(points[i] - points[i-1], points[i+1] - points[i])
            if ang != 0.:
                filtered.append(points[i])

        return filtered

    def __form_points(self, p1, p2, lt_left: int, lt_right: int, ut_left: int, ut_right: int):
        i = ut_left
        final_points = []

        while True:
            final_points.append(p1[i % len(p1)])
            if ((i % len(p1)) is lt_left): break
            i += 1

        i = lt_right

        while True:
            final_points.append(p2[i % len(p2)])
            if ((i % len(p2)) is ut_right): break
            i += 1

        return self.__remove_colinear(final_points)

    def __merge_step(self, pol1, pol2):
        pol1_x = [i[0] for i in pol1]
        pol2_x = [i[0] for i in pol2]
        pol1_rightmost_ind = pol1_x.index(max(pol1_x))
        pol2_leftmost_ind = pol2_x.index(min(pol2_x))

        lt_left, lt_right = self.__incremental_tangent(pol1, pol2, pol1_rightmost_ind, pol2_leftmost_ind, 1)
        ut_left, ut_right = self.__incremental_tangent(pol1, pol2, pol1_rightmost_ind, pol2_leftmost_ind, -1)

        return self.__form_points(pol1, pol2, lt_left, lt_right, ut_left, ut_right)

    def solve(self, points):
        if(len(points) <= 5):
            x, y = geometry.Polygon(points).convex_hull.exterior.coords.xy
            return ((np.asarray([x, y]).T)[:len(x)-1])[::-1]

        points = sorted(points, key=list[0])

        left = self.solve(points[:len(points)//2])
        right = self.solve(points[len(points)//2:])

        return self.__merge_step(left, right)
