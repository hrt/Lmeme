import math


def is_alive(target):
    return target.SpawnCount % 2 == 0


def hurtable(champion, target):
    return target.Team != champion.Team and target.Targetable and is_alive(target) and target.Visibility


def basic_attacks_needed(champion, target):
    damage = champion.BaseAtk + champion.BonusAtk
    if target.Armor >= 0:
        effective_damage = damage * 100. / (100. + target.Armor)
    else:
        effective_damage = damage * (2. - (100. / (100. - target.Armor)))
    return target.Health / effective_damage


def in_range(stats, champion, target):
    distance = math.sqrt((champion.x - target.x)**2 + (champion.y - target.y)**2)
    entity_radius = stats.get(target.Name)['radius'] * target.SizeMultiplier
    champion_radius = stats.get(champion.Name)['radius'] * champion.SizeMultiplier
    return distance - entity_radius <= champion.AtkRange + champion_radius


def select_lowest_target(stats, champion, entities):
    # todo: check if champion is stunned
    target = None
    min_autos = None
    for entity in entities.values():
        if not hurtable(champion, entity):
            continue
        if not in_range(stats, champion, entity):
            continue
        autos = basic_attacks_needed(champion, entity)
        if target is None or 0 < autos < min_autos:
            target = entity
            min_autos = autos
    return target
