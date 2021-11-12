import constants
import numpy as np
from pymem.exception import MemoryReadError
from utils import bool_from_buffer, float_from_buffer, int_from_buffer, linked_insert, Node


def read_object(mem, address):
    try:
        # this sometimes hangs?!
        data = mem.read_bytes(address, constants.OBJECT_SIZE)
    except MemoryReadError:
        return None

    params = {}
    for field in constants.Object._fields:
        offset = getattr(constants, 'oObject{field}'.format(field=field))
        params[field] = float_from_buffer(data, offset)
    try:
        params['Name'] = mem.read_string(int_from_buffer(data, constants.oObjectName), 50)
    except (MemoryReadError, UnicodeDecodeError):
        return None

    params['NetworkID'] = int_from_buffer(data, constants.oObjectNetworkID)
    params['Lvl'] = int_from_buffer(data, constants.oObjectLvl)
    params['Team'] = int_from_buffer(data, constants.oObjectTeam)
    params['SpawnCount'] = int_from_buffer(data, constants.oObjectSpawnCount)
    params['Targetable'] = bool_from_buffer(data, constants.oObjectTargetable)
    params['Visibility'] = bool_from_buffer(data, constants.oObjectVisibility)

    return constants.Object(**params)


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
        elif o.Name in stats.names():
            champions[o.NetworkID] = o
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


def effective_damage(damage, armour):
    if armour >= 0:
        return damage * 100. / (100. + armour)
    return damage * (2. - (100. / (100. - armour)))
