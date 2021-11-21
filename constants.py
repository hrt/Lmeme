PROCESS_NAME = 'League of Legends.exe'

oObjectManager = 0x186CD20
oObjectMapRoot = 0x28
oObjectMapNodeNetId = 0x10
oObjectMapNodeObject = 0x14

OBJECT_SIZE = 0x3400
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
oObjectLevel = 0x339C
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
oObjectSpawnCount = 0x2A0
oObjectSpellBook = 0x27e4
oObjectSpellBookArray = 0x488
oObjectBuffManager = 0x21B8
oObjectBuffManagerEntriesStart = oObjectBuffManager + 0x10
oObjectBuffManagerEntriesEnd = oObjectBuffManager + 0x14

SPELL_SIZE = 0x30
oSpellSlotLevel = 0x20
oSpellSlotCooldownExpire = 0x28

BUFF_SIZE = 0x78
oBuffInfo = 0x8
oBuffCount = 0x74
oBuffEndTime = 0x10
oBuffInfoName = 0x8

oObjectx = oObjectPos
oObjectz = oObjectPos + 0x4
oObjecty = oObjectPos + 0x8

oLocalPlayer = 0x310990C
oViewProjMatrices = 0x31322A8
oRenderer = 0x310991C
oRendererWidth = 0x0
oRendererHeight = 0x4
oGameTime = 0x3101384
