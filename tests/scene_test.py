import unittest

from scene import Scene

scene = Scene()


class TestScene(unittest.TestCase):
    def test_square_coords_rad_one(self):
        self.assertListEqual(
            sorted(scene._get_square_coords((0, 0), 1)),
            sorted(
                [
                    (-1, -1),
                    (0, -1),
                    (1, -1),
                    (-1, 0),
                    (1, 0),
                    (-1, 1),
                    (0, 1),
                    (1, 1),
                ],
            ),
        )

    def test_square_coords_rad_two(self):
        print(
            scene._get_square_coords((0, 0), 2),
        )

        self.assertListEqual(
            sorted(scene._get_square_coords((0, 0), 2)),
            sorted(
                [
                    (-2, -2),
                    (-1, -2),
                    (0, -2),
                    (1, -2),
                    (2, -2),
                    (-2, -1),
                    (-2, 0),
                    (-2, 1),
                    (-2, 2),
                    (2, -1),
                    (2, 0),
                    (2, 1),
                    (2, 2),
                    (-1, 2),
                    (0, 2),
                    (1, 2),
                ]
            ),
        )


if __name__ == "__main__":
    unittest.main()
