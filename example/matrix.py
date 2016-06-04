from asciify import asciify
import random
import time
import pygame

width, height = (60, 30)
add_per_frame = 5

render = asciify(width, height, "font", fontsize=16)
random.seed(time.time())

Particles = [
                [
                    random.randint(0, width),
                    random.randint(-1, height),
                    random.uniform(0.1, 1.5)
                ] for x in range(add_per_frame)
            ]
chars = list("abcdefghijklmnopqrstuvwxyz0123456789!\"$%^&*()_+-=[]{}:;@'~#|\<>?,./")

while True:
    render.checkexit()
    keys = render.listkeys()

    for num, part in enumerate(Particles):
        part[1] += part[2]
        if part[1] > height+1:
            del Particles[num]

        colorrand = (random.randint(60, 255), random.randint(150, 255), random.randint(1, 100))
        render.setString(part[0], part[1], random.choice(chars), color=colorrand)

    Particles.extend([
                        [
                            random.randint(0, width),
                            random.randint(-1, height),
                            random.uniform(0.1, 1.5)
                        ] for x in range(add_per_frame)
                    ])
    render.text(0, 0, "THE MATRIX EXAMPLE", center=(1, 1))

    render.update(30)
