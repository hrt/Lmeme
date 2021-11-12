import math
from world import effective_damage


def hurtable(champion, entity):
    return entity.Team != champion.Team and entity.Targetable and entity.SpawnCount % 2 == 0 and entity.Visibility


def in_range(stats, champion, entity):
    distance = math.sqrt((champion.x - entity.x)**2 + (champion.y - entity.y)**2)
    entity_radius = stats.get(entity.Name)['radius'] * entity.SizeMultiplier
    champion_radius = stats.get(champion.Name)['radius'] * champion.SizeMultiplier
    return distance - entity_radius <= champion.AtkRange + champion_radius


def can_execute(champion, entity):
    damage = effective_damage(champion.BaseAtk + champion.BonusAtk, entity.Armor)
    return damage >= entity.Health


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
