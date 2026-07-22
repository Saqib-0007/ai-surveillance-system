class LineCounter:
    """
    Counts IN/OUT crossings across a virtual line.
    """

    def __init__(self, line):

        self.line = line

        self.previous_positions = {}

        self.in_count = 0
        self.out_count = 0

    def _side(self, point):

        (x1, y1), (x2, y2) = self.line
        x, y = point

        return (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)

    def update(self, object_id, center):

        current_side = self._side(center)

        if object_id not in self.previous_positions:

            self.previous_positions[object_id] = current_side

            return {
                "crossed": False,
                "direction": None,
            }

        previous_side = self.previous_positions[object_id]

        self.previous_positions[object_id] = current_side

        if previous_side < 0 <= current_side:

            self.in_count += 1

            return {
                "crossed": True,
                "direction": "IN",
            }

        elif previous_side > 0 >= current_side:

            self.out_count += 1

            return {
                "crossed": True,
                "direction": "OUT",
            }

        return {
            "crossed": False,
            "direction": None,
        }

    def get_counts(self):

        return {
            "in": self.in_count,
            "out": self.out_count,
        }

    def reset(self):

        self.previous_positions.clear()

        self.in_count = 0
        self.out_count = 0