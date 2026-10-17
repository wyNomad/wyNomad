import importlib.util
import json
from pathlib import Path
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
            cycle, states, eaten = SNAKE.simulate(width, cells)
            self.assertEqual(len(cycle), len(set(cycle)))
            for a, b in zip(cycle, cycle[1:] + cycle[:1]):
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

    def test_growth_occurs_only_when_a_contribution_is_eaten(self):
        cells = [SNAKE.Cell(0, 0, "2026-01-01", 0, 0),
                 SNAKE.Cell(1, 3, "2026-01-02", 12, 4)]
        _, states, eaten = SNAKE.simulate(2, cells)
        self.assertEqual(len(eaten), 1)
        growth_frame = eaten[0][0]
        self.assertTrue(all(len(body) == 4 for body in states[:growth_frame]))
        self.assertTrue(all(len(body) == 5 for body in states[growth_frame:]))
        self.assertEqual(states[0][0], states[-1][0])

    def test_empty_year_stays_at_initial_length(self):
        _, states, eaten = SNAKE.simulate(53, [])
        self.assertEqual(eaten, [])
        self.assertTrue(all(len(body) == 4 for body in states))

    def test_svg_contains_capped_body_with_delayed_births_in_both_themes(self):
        cells = [SNAKE.Cell(x, y, "2026-01-01", 1, 1)
                 for x in range(6) for y in range(7)]
        namespace = {"s": "http://www.w3.org/2000/svg"}
        for theme in ("light", "dark"):
            svg = SNAKE.create_svg("wyNomad", 6, cells, theme)
            root = ET.fromstring(svg)
            parts = [el for el in root.findall("s:rect", namespace) if el.get("class") == "part"]
            self.assertEqual(len(parts), 20)
            self.assertEqual([int(el.get("data-birth-frame")) for el in parts[:4]], [0] * 4)
            births = [int(el.get("data-birth-frame")) for el in parts[4:]]
            self.assertTrue(all(a < b for a, b in zip([0] + births, births)))
            self.assertTrue(all(el.get("opacity") == "0" for el in parts[4:]))
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
