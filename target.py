import math
from world import effective_damage


def is_alive(target):
    return target.SpawnCount % 2 == 0


def hurtable(champion, target):
    return target.Team != champion.Team and target.Targetable and is_alive(target) and target.Visibility


def in_range(stats, champion, target):
    distance = math.sqrt((champion.x - target.x)**2 + (champion.y - target.y)**2)
    entity_radius = stats.get(target.Name)['radius'] * target.SizeMultiplier
    champion_radius = stats.get(champion.Name)['radius'] * champion.SizeMultiplier
    return distance - entity_radius <= champion.AtkRange + champion_radius


def can_execute(champion, target):
    damage = effective_damage(champion.BaseAtk + champion.BonusAtk, target.Armor)
    return damage >= target.Health


def select_lowest_target(stats, champion, entities):
    # todo: check if champion is stunned
    target = None
    for entity in entities.values():
        if not hurtable(champion, entity):
            continue
        if not in_range(stats, champion, entity):
            continue
        if target is None or 0 < entity.Health < target.Health:
            target = entity
    return target
