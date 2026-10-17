import importlib.util
import json
from pathlib import Path
import random
import sys
import unittest
import xml.etree.ElementTree as ET


SPEC = importlib.util.spec_from_file_location("growing_snake", Path(__file__).with_name("generate_snake.py"))
SNAKE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SNAKE
SPEC.loader.exec_module(SNAKE)


class GrowingSnakeTests(unittest.TestCase):
    def test_route_and_body_do_not_cross_on_odd_or_even_calendars(self):
        for width in (1, 2, 3, 52, 53, 54):
            cells = [SNAKE.Cell(x, y, "2026-01-01", 1, 1)
                     for x in range(width) for y in range(7)]
            route, states, eaten = SNAKE.simulate(width, cells)
            heads = [states[0][0]] + route
            for a, b in zip(heads, heads[1:]):
                self.assertEqual(abs(a[0] - b[0]) + abs(a[1] - b[1]), 1)
            self.assertEqual({(cell.x, cell.y) for _, cell in eaten},
                             {(cell.x, cell.y) for cell in cells})
            previous = states[0]
            for body in states[1:]:
                self.assertEqual(len(body), len(set(body)))
                self.assertLessEqual(len(body), 20)
                self.assertIn(len(body) - len(previous), (0, 1))
                self.assertEqual(body[1:], previous[:len(body) - 1])
                previous = body
            self.assertEqual(states[-1][:4], states[0])

    def test_low_counts_are_eaten_first_even_when_high_counts_block_the_way(self):
        cells = [SNAKE.Cell(x, y, "2026-01-01", 1 if (x, y) == (1, 3) else 20, 1)
                 for x in range(3) for y in range(7)]
        _, states, eaten = SNAKE.simulate(3, cells)
        self.assertEqual([cell.count for _, cell in eaten], [1] + [20] * 20)
        self.assertTrue(all(len(body) == len(set(body)) for body in states))

    def test_mixed_counts_are_sorted_with_no_missing_or_repeated_food(self):
        for width in (2, 7, 53):
            rng = random.Random(width)
            cells = [SNAKE.Cell(x, y, "2026-01-01", rng.randint(1, 8), 1)
                     for x in range(width) for y in range(7) if rng.random() < .6]
            _, states, eaten = SNAKE.simulate(width, cells)
            self.assertEqual([cell.count for _, cell in eaten], sorted(c.count for c in cells))
            self.assertEqual(len({(c.x, c.y) for _, c in eaten}), len(cells))
            self.assertTrue(all(len(body) == len(set(body)) for body in states))

    def test_same_count_uses_a_shorter_safe_route_than_column_scanning(self):
        cells = [SNAKE.Cell(30, 0, "2026-01-01", 1, 1)]
        _, _, eaten = SNAKE.simulate(53, cells)
        self.assertLess(eaten[0][0], SNAKE.make_cycle(53).index((30, 0)) + 1)

    def test_each_four_contributions_earns_one_segment(self):
        cells = [SNAKE.Cell(0, 0, "2026-01-01", 0, 0),
                 SNAKE.Cell(1, 3, "2026-01-02", 12, 4)]
        _, states, eaten = SNAKE.simulate(2, cells)
        self.assertEqual(len(eaten), 1)
        growth_frame = eaten[0][0]
        self.assertTrue(all(len(body) == 4 for body in states[:growth_frame]))
        self.assertEqual([len(body) for body in states[growth_frame:growth_frame + 3]], [5, 6, 7])
        self.assertEqual(len(states[-1]), 7)
        self.assertEqual(states[0][0], states[-1][0])

    def test_growth_remainders_carry_across_days(self):
        cells = [SNAKE.Cell(0, 0, "2026-01-01", 1, 1),
                 SNAKE.Cell(2, 0, "2026-01-02", 2, 1),
                 SNAKE.Cell(3, 0, "2026-01-03", 4, 2)]
        _, states, eaten = SNAKE.simulate(6, cells)
        self.assertEqual([c.count for _, c in eaten], [1, 2, 4])
        self.assertTrue(all(len(b) == 4 for b in states[:eaten[-1][0]]))
        self.assertEqual(len(states[-1]), 5)

    def test_sparse_calendar_does_not_force_a_column_scan_or_long_trip_home(self):
        cells = [SNAKE.Cell(30, 0, "2026-01-01", 1, 1),
                 SNAKE.Cell(29, 0, "2026-01-02", 2, 1)]
        route, states, eaten = SNAKE.simulate(53, cells)
        self.assertEqual(eaten[0][0], 31)
        self.assertLess(len(route), 100)
        self.assertEqual(states[-1][:4], states[0])

    def test_whole_route_validation_rejects_collision_and_reordered_food(self):
        cells = [SNAKE.Cell(1, 0, "2026-01-01", 4, 1),
                 SNAKE.Cell(2, 0, "2026-01-02", 8, 2)]
        route, states, eaten = SNAKE.simulate(6, cells)
        expected = [c for _, c in eaten]
        self.assertIsNone(SNAKE.replay_route([states[0][1]] + route, states[0], cells, 20, expected))
        self.assertIsNone(SNAKE.replay_route(route, states[0], cells, 20, expected[::-1]))

    def test_empty_year_stays_at_initial_length(self):
        _, states, eaten = SNAKE.simulate(53, [])
        self.assertEqual(eaten, [])
        self.assertTrue(all(len(body) == 4 for body in states))

    def test_svg_contains_capped_body_with_delayed_births_in_both_themes(self):
        cells = [SNAKE.Cell(x, y, "2026-01-01", 4, 1)
                 for x in range(6) for y in range(7)]
        namespace = {"s": "http://www.w3.org/2000/svg"}
        for theme in ("light", "dark"):
            svg = SNAKE.create_svg("wyNomad", 6, cells, theme)
            root = ET.fromstring(svg)
            parts = [el for el in root.findall("s:rect", namespace) if el.get("class") == "part"]
            self.assertEqual(len(parts), 20)
            self.assertEqual(root.get("data-contributions-per-segment"), "4")
            self.assertTrue(all(el.get("fill") == SNAKE.PALETTES[theme][1] for el in parts))
            self.assertEqual([int(el.get("data-birth-frame")) for el in parts[:4]], [0] * 4)
            births = [int(el.get("data-birth-frame")) for el in parts[4:]]
            self.assertTrue(all(a < b for a, b in zip([0] + births, births)))
            self.assertTrue(all(el.get("opacity") == "0" for el in parts[4:]))
            counts = list(map(int, root.get("data-eat-counts").split(",")))
            self.assertEqual(counts, sorted(counts))
            self.assertIn("prefers-reduced-motion", svg)
            self.assertNotIn("<script", svg)
            self.assertNotIn("http://", svg.replace('xmlns="http://www.w3.org/2000/svg"', ''))

    def test_invalid_or_duplicate_calendar_is_rejected(self):
        day = {"date": "2026-01-01", "weekday": 4,
               "contributionCount": 2, "contributionLevel": "FIRST_QUARTILE"}
        calendar = {"weeks": [{"contributionDays": [day]}]}
        self.assertEqual(SNAKE.read_calendar(calendar)[1][0].count, 2)
        for bad in ({"weeks": []}, {"weeks": [{"contributionDays": [day, day]}]}):
            with self.assertRaises(ValueError):
                SNAKE.read_calendar(bad)
        bad = json.loads(json.dumps(calendar))
        bad["weeks"][0]["contributionDays"][0]["contributionCount"] = 0
        with self.assertRaises(ValueError):
            SNAKE.read_calendar(bad)


if __name__ == "__main__":
    unittest.main()
