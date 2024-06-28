from dataclasses import dataclass
import math
import random

import pygame


@dataclass
class Particle:
    pos: list[int, int]
    vec: tuple[int, int]
    color: tuple
    duration: float
    radius_start: int
    radius_end: int
    time_passed: float = 0


class ParticleManager:

    __particles: list[Particle] = []

    def create_particle(pos, vec, color, duration, radius_start, radius_end):
        ParticleManager.__particles.append(
            Particle(list(pos), vec, color, duration, radius_start, radius_end)
        )

    def create_explosion(
        pos, particle_count, explosion_power, color, max_duration, radius_start
    ):
        for _ in range(particle_count):
            r = random.random() * math.pi * 2
            ParticleManager.__particles.append(
                Particle(
                    list(pos),
                    [
                        math.sin(r) * explosion_power * random.random(),
                        math.cos(r) * explosion_power * random.random(),
                    ],
                    color,
                    max_duration * (random.random() / 2 + ((2 - 1) / 2)), # generates factor between 0.5 and 1
                    radius_start,
                    radius_end=0,
                )
            )

    def clear():
        ParticleManager.__particles.clear()

    def update(dt, dt_s):
        ParticleManager.__particles = [
            p for p in ParticleManager.__particles if p.time_passed < p.duration
        ]
        for p in ParticleManager.__particles:
            p.time_passed += dt_s
            p.pos[0] += p.vec[0] * dt
            p.pos[1] += p.vec[1] * dt

    def draw(surface: pygame.Surface):
        for p in ParticleManager.__particles:
            pygame.draw.circle(
                surface,
                p.color,
                p.pos,
                min(1, p.time_passed / p.duration) * (p.radius_end - p.radius_start)
                + p.radius_start,
            )
