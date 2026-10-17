"""Generate a growing contribution snake as a self-contained, script-free SVG."""

import argparse
from collections import deque
from dataclasses import dataclass
from datetime import date
from html import escape
import json
import os
from pathlib import Path
import re
from urllib.request import Request, urlopen


LEVELS = {
    "NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4,
}
PALETTES = {
    "light": (["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"], "#6366f1", "#1b1f230a"),
    "dark": (["#161b22", "#01311f", "#034525", "#0f6d31", "#00c647"], "#818cf8", "#ffffff0d"),
}


@dataclass(frozen=True)
class Cell:
    x: int
    y: int
    day: str
    count: int
    level: int


def read_calendar(calendar):
    weeks = calendar["weeks"]
    if not 1 <= len(weeks) <= 60:
        raise ValueError("Expected 1 to 60 contribution weeks")
    cells, dates, coordinates = [], set(), set()
    for x, week in enumerate(weeks):
        for day in week["contributionDays"]:
            value = day["date"]
            date.fromisoformat(value)
            y, count = day["weekday"], day["contributionCount"]
            level = LEVELS[day["contributionLevel"]]
            if type(y) is not int or not 0 <= y < 7 or type(count) is not int or count < 0:
                raise ValueError("Invalid contribution cell")
            if (count == 0) != (level == 0):
                raise ValueError("Contribution count and level disagree")
            if value in dates or (x, y) in coordinates:
                raise ValueError("Duplicate contribution cell")
            dates.add(value)
            coordinates.add((x, y))
            cells.append(Cell(x, y, value, count, level))
    if not cells:
        raise ValueError("No contribution days returned")
    return len(weeks), cells


def fetch_calendar(username):
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN is required to fetch contribution data")
    query = """query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            weeks { contributionDays { date weekday contributionCount contributionLevel } }
          }
        }
      }
    }"""
    request = Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": {"login": username}}).encode(),
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json",
                 "User-Agent": "growing-contribution-snake"},
    )
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors") or not payload.get("data", {}).get("user"):
        raise ValueError("GitHub did not return a valid contribution calendar")
    return payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def make_cycle(width, height=7):
    # A simple cycle visits every date once and returns along the outside border.
    # Its vertices never repeat, so a capped body cannot collide with itself.
    cycle = [(x, y) for x in range(width)
             for y in (range(height) if x % 2 == 0 else range(height - 1, -1, -1))]
    last_y = cycle[-1][1]
    cycle.extend((width, y) for y in range(last_y, height + 1))
    cycle.extend((x, height) for x in range(width - 1, -2, -1))
    cycle.extend((-1, y) for y in range(height - 1, -1, -1))
    return cycle


def plan_path(indices, body, food, priority, growth_cap):
    """Shortest safe path to the current count tier, keeping room for growth.

    Shortcuts preserve the body's order on a Hamiltonian cycle. This leaves a
    guaranteed safe next step when no direct path around higher-count food exists.
    """
    start, size = body[0], len(indices)
    head, tail = indices[start], indices[body[-1]]
    gap = (tail - head) % size
    reserve = growth_cap - len(body) + 2
    limit = gap - reserve
    parents, queue = {start: None}, deque([start])
    while queue:
        point = queue.popleft()
        if point != start and point in food and food[point].count == priority:
            path = []
            while point != start:
                path.append(point)
                point = parents[point]
            return path[::-1]
        previous = (indices[point] - head) % size
        for dx, dy in ((1, 0), (0, -1), (0, 1), (-1, 0)):
            nxt = point[0] + dx, point[1] + dy
            if nxt not in indices or nxt in parents:
                continue
            progress = (indices[nxt] - head) % size
            if not previous < progress <= limit:
                continue
            if nxt in food and food[nxt].count > priority:
                continue
            parents[nxt] = point
            queue.append(nxt)
    return []


def simulate(width, cells, initial_length=4, max_length=20):
    cycle = make_cycle(width)
    indices = {point: i for i, point in enumerate(cycle)}
    food = {(c.x, c.y): c for c in cells if c.count > 0}
    growth_cap = min(max_length, initial_length + len(food))
    if not 2 <= initial_length <= max_length or growth_cap >= len(cycle):
        raise ValueError("Snake lengths must fit the route")
    initial = [cycle[-1 - i] for i in range(initial_length)]
    states, eaten, route = [initial], [], []

    def step(point):
        current = states[-1]
        consume = point in food and food[point].count == min(c.count for c in food.values())
        growing = consume and len(current) < max_length
        retained = current if growing else current[:-1]
        if point in retained:
            raise ValueError("Planned route would collide with the body")
        body = [point] + retained
        route.append(point)
        states.append(body)
        if consume:
            eaten.append((len(route), food.pop(point)))

    if not food:
        for point in cycle:
            step(point)
    while food:
        priority = min(cell.count for cell in food.values())
        path = plan_path(indices, states[-1], food, priority, growth_cap)
        if not path:
            path = [cycle[(indices[states[-1][0]] + 1) % len(cycle)]]
        for point in path:
            step(point)
    # Return on the safe cycle so the first four segments join the next loop.
    while states[-1][:initial_length] != initial:
        step(cycle[(indices[states[-1][0]] + 1) % len(cycle)])
    return route, states, eaten


def position_keys(points, route_frames, total_frames):
    retained = []
    for i, point in enumerate(points):
        if 0 < i < len(points) - 1:
            prev, nxt = points[i - 1], points[i + 1]
            if (point[0] - prev[0], point[1] - prev[1]) == (nxt[0] - point[0], nxt[1] - point[1]):
                continue
        retained.append((100 * i / total_frames, point))
    retained.append((100, points[route_frames]))
    return "".join(f"{t:.5f}%{{transform:translate({x * 16}px,{y * 16}px)}}"
                   for t, (x, y) in retained)


def create_svg(username, width, cells, theme, initial_length=4, max_length=20):
    colors, snake_color, border = PALETTES[theme]
    route, states, eaten = simulate(width, cells, initial_length, max_length)
    route_frames, pause_frames = len(route), 20
    total_frames = route_frames + pause_frames
    frame_ms = min(90, max(25, round(40000 / route_frames)))
    duration = total_frames * frame_ms
    epsilon = min(.001, 50 / total_frames)
    eat_times = {(c.x, c.y): frame for frame, c in eaten}
    actual_length = len(states[-1])
    styles = [
        f".food{{animation-duration:{duration}ms;animation-timing-function:linear;animation-iteration-count:infinite}}",
        f".part{{animation-duration:{duration}ms;animation-timing-function:linear;animation-iteration-count:infinite}}",
    ]
    grid, parts = [], []
    for i, cell in enumerate(cells):
        name = f"{theme}-food{i}"
        if cell.count:
            t = 100 * eat_times[(cell.x, cell.y)] / total_frames
            styles.append("@keyframes " + name + "{0%," + f"{t - epsilon:.5f}%"
                          + "{fill:" + colors[cell.level] + "}"
                          + f"{t:.5f}%,100%" + "{fill:" + colors[0] + "}}")
        grid.append(
            f'<rect class="food" x="{cell.x * 16 + 2}" y="{cell.y * 16 + 2}" '
            f'width="12" height="12" rx="2" fill="{colors[cell.level]}" '
            f'stroke="{border}" style="animation-name:{name}" data-date="{cell.day}" '
            f'data-count="{cell.count}"><title>{cell.count} contributions on {cell.day}</title></rect>'
        )
    for i in range(actual_length):
        birth = next(frame for frame, body in enumerate(states) if len(body) > i)
        points = [body[i] if len(body) > i else states[birth][i] for body in states]
        styles.append(f"@keyframes {theme}-move{i}{{{position_keys(points, route_frames, total_frames)}}}")
        animations, opacity = f"{theme}-move{i}", 1
        if birth:
            t = birth / total_frames * 100
            styles.append(f"@keyframes {theme}-grow{i}{{0%,{t - epsilon:.5f}%{{opacity:0}}"
                          f"{t:.5f}%,100%{{opacity:1}}}}")
            animations += f",{theme}-grow{i}"
            opacity = 0
        size = 14 if i == 0 else max(10, 12 - i / 15)
        x, y = points[0]
        parts.append(
            f'<rect class="part" x="{(16 - size) / 2:.2f}" y="{(16 - size) / 2:.2f}" '
            f'width="{size:.2f}" height="{size:.2f}" rx="4" fill="{snake_color}" '
            f'opacity="{opacity}" data-birth-frame="{birth}" data-extra="{str(bool(birth)).lower()}" '
            f'style="transform:translate({x * 16}px,{y * 16}px);animation-name:{animations}"/>'
        )
    progress = ["0%{transform:scaleX(0)}"]
    for index, (frame, _) in enumerate(eaten, 1):
        t = frame / total_frames * 100
        progress.append(f"{t - epsilon:.5f}%{{transform:scaleX({(index - 1) / len(eaten):.6f})}}"
                        f"{t:.5f}%{{transform:scaleX({index / len(eaten):.6f})}}")
    progress.append(f"100%{{transform:scaleX({1 if eaten else 0})}}")
    styles.append("@keyframes " + theme + "-progress{" + "".join(progress) + "}")
    styles.append(f".progress-{theme}{{transform:scaleX(0);animation:{theme}-progress {duration}ms linear infinite;transform-origin:0px 144px}}")
    styles.append('@media(prefers-reduced-motion:reduce){.part,.food,.progress{animation:none!important}.part[data-extra="true"]{opacity:0!important}}')
    title = escape(f"{username}'s growing contribution snake")
    desc = escape(f"Real GitHub contribution days. Starts with {initial_length} segments; "
                  f"eats lower contribution counts first and grows up to {max_length} segments. "
                  "Restarts after each loop.")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{(width + 3) * 16}" height="176" '
        f'viewBox="-24 -16 {(width + 3) * 16} 176" role="img" aria-labelledby="title-{theme} desc-{theme}" '
        f'data-initial-length="{initial_length}" data-max-length="{max_length}" '
        f'data-final-length="{actual_length}" data-food-count="{len(eaten)}" '
        f'data-eat-counts="{",".join(str(c.count) for _, c in eaten)}" '
        f'data-route-steps="{route_frames}" data-frame-ms="{frame_ms}">'
        f'<title id="title-{theme}">{title}</title><desc id="desc-{theme}">{desc}</desc>'
        f'<style>{"".join(styles)}</style>{"".join(grid)}{"".join(parts)}'
        f'<rect x="0" y="140" width="{width * 16}" height="8" rx="3" fill="{colors[0]}"/>'
        f'<rect class="progress progress-{theme}" x="0" y="140" width="{width * 16}" height="8" rx="3" fill="{snake_color}"/>'
        '</svg>\n'
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", required=True)
    parser.add_argument("--output-dir", default="dist")
    parser.add_argument("--calendar", type=Path, help="Local GitHub calendar JSON for development previews")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}", args.username):
        raise ValueError("Invalid GitHub username")
    calendar = json.loads(args.calendar.read_text()) if args.calendar else fetch_calendar(args.username)
    width, cells = read_calendar(calendar)
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    for theme, name in [("light", "github-contribution-grid-snake.svg"),
                        ("dark", "github-contribution-grid-snake-dark.svg")]:
        (output / name).write_text(create_svg(args.username, width, cells, theme), encoding="utf-8")
    print(f"Generated light/dark growing snakes from {len(cells)} contribution days")


if __name__ == "__main__":
    main()
