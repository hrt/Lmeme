import constants
import numpy as np
from pymem.exception import MemoryReadError
from collections import namedtuple
from utils import bool_from_buffer, float_from_buffer, int_from_buffer, linked_insert, Node

Object = namedtuple('Object', 'name, ability_power, armor, attack_range, attack_speed_multiplier, attack_speed_modifier, base_attack, bonus_attack, crit, crit_multiplier, health, magic_resist, mana, max_health, movement_speed, size_multiplier, x, y, z, network_id, level, team, spawn_count, targetable, visibility, spells')
Spell = namedtuple('Spell', 'level, time')

def read_spells(mem, data):
    # pointers at address + ObjSpellBook
    # Q 0
    # W 4
    # E 8
    # R C
    # D 10
    # F 14
    # todo
    pass


def read_object(mem, address):
    try:
        # this sometimes hangs?!
        data = mem.read_bytes(address, constants.OBJECT_SIZE)
    except MemoryReadError:
        return None

    params = {}
    try:
        params['name'] = mem.read_string(int_from_buffer(data, constants.oObjectName), 50)
    except (MemoryReadError, UnicodeDecodeError):
        return None
    params['ability_power'] = float_from_buffer(data, constants.oObjectAbilityPower)
    params['armor'] = float_from_buffer(data, constants.oObjectArmor)
    params['attack_range'] = float_from_buffer(data, constants.oObjectAtkRange)
    params['attack_speed_multiplier'] = float_from_buffer(data, constants.oObjectAtkSpeedMulti)
    params['attack_speed_modifier'] = float_from_buffer(data, constants.oObjectAtkSpeedMod)
    params['base_attack'] = float_from_buffer(data, constants.oObjectBaseAtk)
    params['bonus_attack'] = float_from_buffer(data, constants.oObjectBonusAtk)
    params['crit'] = float_from_buffer(data, constants.oObjectCrit)
    params['crit_multiplier'] = float_from_buffer(data, constants.oObjectCritMulti)
    params['magic_resist'] = float_from_buffer(data, constants.oObjectMagicRes)
    params['mana'] = float_from_buffer(data, constants.oObjectMana)
    params['health'] = float_from_buffer(data, constants.oObjectHealth)
    params['max_health'] = float_from_buffer(data, constants.oObjectMaxHealth)
    params['movement_speed'] = float_from_buffer(data, constants.oObjectMoveSpeed)
    params['size_multiplier'] = float_from_buffer(data, constants.oObjectSizeMultiplier)
    params['x'] = float_from_buffer(data, constants.oObjectx)
    params['y'] = float_from_buffer(data, constants.oObjecty)
    params['z'] = float_from_buffer(data, constants.oObjectz)

    params['network_id'] = int_from_buffer(data, constants.oObjectNetworkID)
    params['level'] = int_from_buffer(data, constants.oObjectLevel)
    params['team'] = int_from_buffer(data, constants.oObjectTeam)
    params['spawn_count'] = int_from_buffer(data, constants.oObjectSpawnCount)

    params['targetable'] = bool_from_buffer(data, constants.oObjectTargetable)
    params['visibility'] = bool_from_buffer(data, constants.oObjectVisibility)

    params['spells'] = read_spells(mem, data)
    return Object(**params)


def find_objects(mem, blacklist, stats, max_count=800):
    # Given a memory interface, blacklist of addresses and champion stats
    # we will iterate through objects in memory and read them
    # if the read fails then we will add the address to the blacklist
    object_pointers = mem.read_uint(mem.base_address + constants.oObjectManager)
    root_node = Node(mem.read_uint(object_pointers + constants.oObjectMapRoot), None)
    addresses_seen = set()
    current_node = root_node
    pointers = []
    count = 0
    while current_node is not None and count < max_count:
        if current_node.address in blacklist or current_node.address in addresses_seen:
            current_node = current_node.next
            continue
        addresses_seen.add(current_node.address)
        try:
            data = mem.read_bytes(current_node.address, 0x18)
            count += 1
        except MemoryReadError:
            blacklist.add(current_node.address)
        else:
            for i in range(3):
                child_address = int_from_buffer(data, i * 4)
                if child_address in addresses_seen:
                    continue
                linked_insert(current_node, child_address)
            net_id = int_from_buffer(data, constants.oObjectMapNodeNetId)
            if net_id - 0x40000000 <= 0x100000:
                # help reduce redundant objects
                pointers.append(int_from_buffer(data, constants.oObjectMapNodeObject))
        current_node = current_node.next

    champions = {}
    for pointer in pointers:
        if not pointer or pointer in blacklist:
            continue
        o = read_object(mem, pointer)
        if o is None:
            blacklist.add(pointer)
        elif o.name.lower() in stats.names():
            champions[o.network_id] = o
    return champions


def find_local_net_id(mem):
    local_player = mem.read_uint(mem.base_address + constants.oLocalPlayer)
    return mem.read_int(local_player + constants.oObjectNetworkID)


def find_game_time(mem):
    return mem.read_float(mem.base_address + constants.oGameTime)


def list_to_matrix(floats):
    m = np.array(floats)
    return m.reshape(4, 4)


def find_view_proj_matrix(mem):
    data = mem.read_bytes(mem.base_address + constants.oRenderer, 0x8)
    width = int_from_buffer(data, constants.oRendererWidth)
    height = int_from_buffer(data, constants.oRendererHeight)

    data = mem.read_bytes(mem.base_address + constants.oViewProjMatrices, 128)
    view_matrix = list_to_matrix([float_from_buffer(data, i * 4) for i in range(16)])
    proj_matrix = list_to_matrix([float_from_buffer(data, 64 + (i * 4)) for i in range(16)])
    view_proj_matrix = np.matmul(view_matrix, proj_matrix)
    return view_proj_matrix.reshape(16), width, height


def world_to_screen(view_proj_matrix, width, height, x, y, z):
    # pasted / translated world to screen math
    clip_coords_x = x * view_proj_matrix[0] + y * view_proj_matrix[4] + z * view_proj_matrix[8] + view_proj_matrix[12]
    clip_coords_y = x * view_proj_matrix[1] + y * view_proj_matrix[5] + z * view_proj_matrix[9] + view_proj_matrix[13]
    clip_coords_w = x * view_proj_matrix[3] + y * view_proj_matrix[7] + z * view_proj_matrix[11] + view_proj_matrix[15]

    if clip_coords_w < 1.:
        clip_coords_w = 1.

    M_x = clip_coords_x / clip_coords_w
    M_y = clip_coords_y / clip_coords_w

    out_x = (width / 2. * M_x) + (M_x + width / 2.)
    out_y = -(height / 2. * M_y) + (M_y + height / 2.)

    if 0 <= out_x <= width and 0 <= out_y <= height:
        return out_x, out_y

    return None, None
