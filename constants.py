from collections import namedtuple

Object = namedtuple('Object', 'AbilityPower, Armor, AtkRange, AtkSpeedMulti, AtkSpeedMod, BaseAtk, BonusAtk, Crit, CritMulti, Health, Lvl, MagicRes, Mana, MaxHealth, MoveSpeed, Team, Targetable, NetworkID, Visibility, SpawnCount, Name, x, y, z, SizeMultiplier')
PROCESS_NAME = 'League of Legends.exe'
WINDOW_NAME = 'League of Legends (TM) Client'
OBJECT_SIZE = 0x3400

oObjectManager = 0x187015C      # \x8B\x0D\x00\x00\x00\x00\x89\x7C\x24\x14 xx????xxxx
                                # \x8B\x0D\x00\x00\x00\x00\x56\x50\xE8\x00\x00\x00\x00\x8B\xF0 xx????xxx????xx
oObjectMapRoot = 0x28
oObjectMapNodeNetId = 0x10
oObjectMapNodeObject = 0x14

oObjectAbilityPower = 0x1788
oObjectArmor = 0x12E4
oObjectAtkRange = 0x1304
oObjectAtkSpeedMulti = 0x12B8
oObjectAtkSpeedMod = 0x128C
oObjectBaseAtk = 0x12BC
oObjectBonusAtk = 0x1234
oObjectCrit = 0x12E0
oObjectCritMulti = 0x12D0
oObjectHealth = 0xDB4
oObjectMaxHealth = oObjectHealth + 0x10
oObjectLvl = 0x339C
oObjectMagicRes = 0x12EC
oObjectMana = 0x2B4
oObjectMoveSpeed = 0x12FC
oObjectPos = 0x1F4
oObjectTeam = 0x4C
oObjectTargetable = 0xD1C
oObjectNetworkID = 0xCC
oObjectMinBBox = 0x0
oObjectVisibility = 0x28C
oObjectName = 0x2BE4
oObjectSizeMultiplier = 0x12D4

oObjectSpellBook = 0x27f8
oObjectSrcIndex = 0x02AC
oObjectSpawnCount = 0x2A0

oObjectx = oObjectPos
oObjectz = oObjectPos + 4
oObjecty = oObjectPos + 8

oLocalPlayer = 0x310D250        # aBlueHero \x8B\x3D\x00\x00\x00\x00\x3B\xF7\x75 xx????xxx
oViewProjMatrices = 0x3134D58   # \xB9\x00\x00\x00\x00\x0F\x10\x80 x????xxx
                                # \x68\x00\x00\x00\x00\x51\x8B\x00 x????xxx
                                # \x68\x00\x00\x00\x00\x8D\x84\x24\x00\x00\x00\x00\x50\x8B\x44\x24\x1C x????xxx????xxxxx
oRenderer = 0x310CD4C           # aWidth \xA1\x00\x00\x00\x00\x53\x8B\x1D\x00\x00\x00\x00\x56\x57\x8B\xF9 x????xxx????xxxx
oRendererWidth = 0x0
oRendererHeight = 0x4

oGameTime = 0x31047C4           # \xF3\x0F\x5C\x0D\x00\x00\x00\x00\x0F\x2F\xC1\xF3 xxxx????xxxx

oUnderMouseObject = 0x182B0E8
