PROCESS_NAME = 'League of Legends.exe'
WINDOW_NAME = 'League of Legends (TM) Client'
OBJECT_SIZE = 0x3400
SPELL_SIZE = 0x40
BUFF_SIZE = 0x78

oObjectManager = 0x187015C
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

oSpellSlotLevel = 0x20
oSpellSlotCooldownExpire = 0x28

oBuffInfo = 0x8
oBuffCount = 0x74
oBuffEndTime = 0x10

oBuffInfoName = 0x8

oObjectx = oObjectPos
oObjectz = oObjectPos + 4
oObjecty = oObjectPos + 8

oLocalPlayer = 0x310D250
oViewProjMatrices = 0x3134D58
oRenderer = 0x310CD4C
oRendererWidth = 0x0
oRendererHeight = 0x4
oGameTime = 0x31047C4
