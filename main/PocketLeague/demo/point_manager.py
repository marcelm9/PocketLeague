from .point import Point

class PointManager:
    points = []
    index = 0

    def add_point(position):
        new_point = Point(f"Point {PointManager.index}", position)
        PointManager.points.append(new_point)
        PointManager.index += 1

    def clear():
        PointManager.points.clear()

    def get_points() -> list[Point]:
        return PointManager.points
