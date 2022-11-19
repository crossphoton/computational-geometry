# %%
import numpy as np
import matplotlib.pyplot as plt
from shapely import geometry

plt.rcParams["figure.figsize"] = [7.50, 7.50]
plt.rcParams["figure.autolayout"] = True

from convex_hull import ConvexHull

# %%

num_points = np.random.randint(3, 200)
points = np.random.rand(num_points, 2) * 50

a = ConvexHull()
convex_ans = list(a.solve(points))
convex_ans.append(convex_ans[0])


def draw_coords(points, convex_hull):
    hull_lib_x, hull_lib_y = geometry.Polygon(
        [[p[0], p[1]] for p in points]).convex_hull.exterior.coords.xy

    fig, axes = plt.subplots()
    plt.subplot()

    xs = [point[0] for point in points]
    ys = [point[1] for point in points]


    x = [p[0] for p in convex_hull]
    y = [p[1] for p in convex_hull]
    plt.plot(x, y, "r")
    plt.plot(hull_lib_x, hull_lib_y, "g:")
    plt.scatter(xs, ys)
    plt.show()

draw_coords(points, convex_ans)

