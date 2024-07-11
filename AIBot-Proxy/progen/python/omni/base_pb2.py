# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: base.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nbase.proto\x12\x13\x43ore.Engine.Network\";\n\x07\x42\x61seReq\x12\x0f\n\x07protoId\x18\x01 \x01(\x05\x12\x11\n\trequestId\x18\x02 \x01(\x05\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\"\x84\x01\n\x07\x42\x61seRsp\x12\x0f\n\x07protoId\x18\x01 \x01(\x05\x12\x31\n\terrorCode\x18\x02 \x01(\x0e\x32\x1e.Core.Engine.Network.ErrorCode\x12\x12\n\nresponseId\x18\x03 \x01(\x05\x12\x13\n\x0bnotifySeqId\x18\x04 \x01(\x03\x12\x0c\n\x04\x64\x61ta\x18\x05 \x01(\x0c*\x94/\n\tErrorCode\x12\n\n\x06\x45rr_OK\x10\x00\x12\x0f\n\x0b\x45rr_Default\x10\x01\x12\x14\n\x10\x45rr_GmCommondReq\x10\x02\x12\x18\n\x14\x45rr_CannotFindPlayer\x10\x03\x12\x16\n\x12\x45rr_InvalidCommand\x10\x04\x12\x15\n\x11\x45rr_PlayerJoinReq\x10\x05\x12\x17\n\x13\x45rr_ManageCastleReq\x10\x06\x12\x1a\n\x16\x45rr_LevelUpWrongCastle\x10\x07\x12\x16\n\x12\x45rr_PendingItemReq\x10\x08\x12\x0e\n\nErr_BagReq\x10\t\x12\x14\n\x10\x45rr_EditSquadReq\x10\n\x12\x12\n\x0e\x45rr_TeamDefeat\x10\x0b\x12\x15\n\x11\x45rr_OrderSquadReq\x10\x0c\x12\x1e\n\x1a\x45rr_BattlePlayerCommandReq\x10\r\x12\x19\n\x15\x45rr_SellItemNotEnough\x10\x0e\x12\x1b\n\x17\x45rr_SellItemWrongItemId\x10\x0f\x12\x19\n\x15\x45rr_LevelUpFullCastle\x10\x10\x12\x1e\n\x1a\x45rr_LevelUpCastleWrongTeam\x10\x11\x12!\n\x1d\x45rr_LevelUpCastleResNotEnough\x10\x12\x12\'\n#Err_MoveCrystalTargetWrongTargetIdx\x10\x13\x12\x1c\n\x18\x45rr_MoveCrystalWrongTeam\x10\x14\x12!\n\x1d\x45rr_MoveCrystalNotFindCrystal\x10\x15\x12 \n\x1c\x45rr_LordSelectWrongGameState\x10\x16\x12\x1d\n\x19\x45rr_LordSelectWrongLordId\x10\x17\x12\x1f\n\x1b\x45rr_LordSelectWrongLockFlag\x10\x18\x12\x1d\n\x19\x45rr_BuyPendingItemSoldOut\x10\x19\x12\x1f\n\x1b\x45rr_BuyPendingItemNotEnough\x10\x1a\x12#\n\x1f\x45rr_RefreshPendingItemNotEnough\x10\x1b\x12\x15\n\x11\x45rr_AmbushHasPath\x10\x1c\x12\x18\n\x14\x45rr_AmbushWrongState\x10\x1d\x12\x15\n\x11\x45rr_AmbushWrongAp\x10\x1e\x12!\n\x1d\x45rr_AmbushFightNoAmbushPlayer\x10\x1f\x12#\n\x1f\x45rr_AmbushFightNoAmbushedPlayer\x10 \x12#\n\x1f\x45rr_AmbushFightWrongAmbushState\x10!\x12%\n!Err_AmbushFightWrongAmbushedState\x10\"\x12\x1f\n\x1b\x45rr_AmbushFightWrongGridIdx\x10#\x12&\n\"Err_AttackEntityWrongAttackerState\x10$\x12&\n\"Err_AttackEntityWrongDefenderState\x10%\x12$\n Err_AttackEntityWrongAttackerPos\x10&\x12 \n\x1c\x45rr_AttackEntityNotNeighbour\x10\'\x12\x1e\n\x1a\x45rr_AttackEntityRepeatJoin\x10(\x12\x1e\n\x1a\x45rr_AttackEntityCannotJoin\x10)\x12\x1a\n\x16\x45rr_AttackEntityAmbush\x10*\x12\x1d\n\x19\x45rr_BornSquadWrongGridIdx\x10+\x12\x1a\n\x16\x45rr_BornSquadHasEntity\x10,\x12!\n\x1d\x45rr_BornSquadNotCrystalBelong\x10-\x12\x1a\n\x16\x45rr_BornSquadHasBattle\x10.\x12\x1b\n\x17\x45rr_BornSquadWrongState\x10/\x12\x19\n\x15\x45rr_CardLevelNotExist\x10\x30\x12\x1a\n\x16\x45rr_CardLevelNotEnough\x10\x31\x12\x15\n\x11\x45rr_CardLevelFull\x10\x32\x12\x1c\n\x18\x45rr_EconomyLevelNotExist\x10\x33\x12\x1d\n\x19\x45rr_EconomyLevelNotEnough\x10\x34\x12\x18\n\x14\x45rr_EconomyLevelFull\x10\x35\x12\x1a\n\x16\x45rr_JoinFightWrongType\x10\x36\x12\x1f\n\x1b\x45rr_JoinFightWrongDefendIdx\x10\x37\x12\x19\n\x15\x45rr_JoinFightWrongPos\x10\x38\x12\x1d\n\x19\x45rr_JoinFightNotNeighbour\x10\x39\x12\x1b\n\x17\x45rr_JoinFightWrongState\x10:\x12\x1a\n\x16\x45rr_JoinFightNotBattle\x10;\x12\x1b\n\x17\x45rr_JoinFightRepeatJoin\x10<\x12\x1e\n\x1a\x45rr_LevelUpEntityWrongType\x10=\x12\x19\n\x15\x45rr_LevelUpEntityFull\x10>\x12\x1e\n\x1a\x45rr_LevelUpEntityNotEnough\x10?\x12\x1f\n\x1b\x45rr_LoadingCancelWrongState\x10@\x12\x1d\n\x19\x45rr_MoveAttackControlBuff\x10\x41\x12\x1c\n\x18\x45rr_MoveAttackWrongState\x10\x42\x12\x1e\n\x1a\x45rr_MoveAttackWrongGridIdx\x10\x43\x12\x1a\n\x16\x45rr_MoveAttackWrongPos\x10\x44\x12\x18\n\x14\x45rr_MoveAttackAmbush\x10\x45\x12\x1c\n\x18\x45rr_MoveAttackRepeatJoin\x10\x46\x12\x1b\n\x17\x45rr_MoveAttackWrongPath\x10G\x12\x1d\n\x19\x45rr_MoveAttackRpNotEnough\x10H\x12\x1e\n\x1a\x45rr_MovePawnOutOfTerritory\x10I\x12\x19\n\x15\x45rr_MovePawnWrongType\x10J\x12\x17\n\x13\x45rr_MovePawnOnlyOne\x10K\x12\x1b\n\x17\x45rr_MovePawnWrongPlayer\x10L\x12#\n\x1f\x45rr_MovePawnPopularityNotEnough\x10M\x12\x19\n\x15\x45rr_ReRollControlBuff\x10N\x12\x18\n\x14\x45rr_ReRollWrongState\x10O\x12\x15\n\x11\x45rr_ReRollHasPath\x10P\x12\x19\n\x15\x45rr_ReRollApNotEnough\x10Q\x12\x1d\n\x19\x45rr_ReviveSquadWrongState\x10R\x12\x1d\n\x19\x45rr_ReviveSquadTimeBefore\x10S\x12\x1c\n\x18\x45rr_ReviveSquadNotEnough\x10T\x12\x17\n\x13\x45rr_ScoutWrongState\x10U\x12\x14\n\x10\x45rr_ScoutHasPath\x10V\x12\x14\n\x10\x45rr_ScoutWrongAp\x10W\x12\x15\n\x11\x45rr_ScoutWrongPos\x10X\x12\x10\n\x0c\x45rr_ScoutFar\x10Y\x12\x18\n\x14\x45rr_ScoutWrongTarget\x10Z\x12\x17\n\x13\x45rr_TeleportWrongAp\x10[\x12\x18\n\x14\x45rr_TeleportWrongPos\x10\\\x12\x1a\n\x16\x45rr_TeleportWrongState\x10]\x12\x17\n\x13\x45rr_TeleportHasPath\x10^\x12\x1b\n\x17\x45rr_TeleportNotInCastle\x10_\x12\x1b\n\x17\x45rr_TeleportWrongTarget\x10`\x12\x14\n\x10\x45rr_TeleportInCd\x10\x61\x12\x1b\n\x17\x45rr_UsePortalWrongState\x10\x62\x12\x1c\n\x18\x45rr_UsePortalControlBuff\x10\x63\x12\x18\n\x14\x45rr_UsePortalHasPath\x10\x64\x12\x19\n\x15\x45rr_UsePortalWrongPos\x10\x65\x12\x19\n\x15\x45rr_UsePortalNotExist\x10\x66\x12\x15\n\x11\x45rr_SkillNotExist\x10g\x12\x18\n\x14\x45rr_SkillWrongDataId\x10h\x12\x14\n\x10\x45rr_SkillHasPath\x10i\x12\x18\n\x14\x45rr_SkillControlBuff\x10j\x12\x17\n\x13\x45rr_SkillWrongState\x10k\x12\x16\n\x12\x45rr_SkillNotEnough\x10l\x12\x11\n\rErr_SkillInCd\x10m\x12\x13\n\x0f\x45rr_SkillUseOut\x10n\x12\x19\n\x15\x45rr_ButcherWrongParam\x10o\x12\x1c\n\x18\x45rr_ButcherIllegalTarget\x10p\x12\x1f\n\x1b\x45rr_ButcherWrongTargetState\x10q\x12\x1d\n\x19\x45rr_ButcherWrongTargetPos\x10r\x12\x1d\n\x19\x45rr_ButcherWrongOriginIdx\x10s\x12\x1d\n\x19\x45rr_ButcherTargetInCastle\x10t\x12\x19\n\x15\x45rr_ButcherOutOfRange\x10u\x12\x18\n\x14\x45rr_ButcherNoStayPos\x10v\x12\x18\n\x14\x45rr_RewindWrongParam\x10w\x12\x1b\n\x17\x45rr_RewindUnableSummons\x10x\x12\x19\n\x15\x45rr_GeneralWrongParam\x10y\x12\x1c\n\x18\x45rr_GeneralWrongPawnType\x10z\x12\x1c\n\x18\x45rr_GeneralFullPawnLevel\x10{\x12\x1d\n\x19\x45rr_GeneralWrongPawnLevel\x10|\x12\x18\n\x14\x45rr_ShadowWrongParam\x10}\x12\x1b\n\x17\x45rr_ShadowUnableSummons\x10~\x12\x18\n\x14\x45rr_ShadowNoBornGrid\x10\x7f\x12\x1b\n\x16\x45rr_ShadowNoTargetGrid\x10\x80\x01\x12\x19\n\x14\x45rr_ShadowOutOfRange\x10\x81\x01\x12\x19\n\x14\x45rr_HackerWrongParam\x10\x82\x01\x12\x1b\n\x16\x45rr_HackerWrongGridIdx\x10\x83\x01\x12\x1e\n\x19\x45rr_HackerWrongVisionGrid\x10\x84\x01\x12 \n\x1b\x45rr_HackerWrongTeleportGrid\x10\x85\x01\x12\x1f\n\x1a\x45rr_HackerWrongOutOfRange1\x10\x86\x01\x12\x1f\n\x1a\x45rr_HackerWrongOutOfRange2\x10\x87\x01\x12\x17\n\x12\x45rr_HackerNoCastle\x10\x88\x01\x12\x17\n\x12\x45rr_HackerHasOther\x10\x89\x01\x12\x17\n\x12\x45rr_HackerInBattle\x10\x8a\x01\x12\x1a\n\x15\x45rr_IceWallWrongParam\x10\x8b\x01\x12\x1e\n\x19\x45rr_IceWallWrongTargetIdx\x10\x8c\x01\x12\x19\n\x14\x45rr_IceWallUnablePut\x10\x8d\x01\x12\x19\n\x14\x45rr_PortalWrongParam\x10\x8e\x01\x12!\n\x1c\x45rr_PortalWrongTargetGridIdx\x10\x8f\x01\x12\x17\n\x12\x45rr_PortalWrongPos\x10\x90\x01\x12\x18\n\x13\x45rr_PortalHasCastle\x10\x91\x01\x12\x17\n\x12\x45rr_PortalHasOther\x10\x92\x01\x12\x19\n\x14\x45rr_PortalOutOfRange\x10\x93\x01\x12\x1c\n\x17\x45rr_PotentialWrongParam\x10\x94\x01\x12!\n\x1c\x45rr_PotentialWrongTargetType\x10\x95\x01\x12\x18\n\x13\x45rr_PotentialFullAp\x10\x96\x01\x12\"\n\x1d\x45rr_PotentialWrongTargetState\x10\x97\x01\x12\x1c\n\x17\x45rr_PotentialOutOfRange\x10\x98\x01\x12\x1c\n\x17\x45rr_SacrificeWrongParam\x10\x99\x01\x12\x1c\n\x17\x45rr_SacrificeWrongState\x10\x9a\x01\x12!\n\x1c\x45rr_SacrificeWrongTargetType\x10\x9b\x01\x12\x1c\n\x17\x45rr_SacrificeOutOfRange\x10\x9c\x01\x12\x19\n\x14\x45rr_TerrorWrongParam\x10\x9d\x01\x12\x1e\n\x19\x45rr_TerrorWrongTargetType\x10\x9e\x01\x12\x1f\n\x1a\x45rr_TerrorWrongTargetState\x10\x9f\x01\x12\x19\n\x14\x45rr_TerrorOutOfRange\x10\xa0\x01\x12\x1a\n\x15\x45rr_SurrenderNotStart\x10\xa1\x01\x12\x1c\n\x17\x45rr_SurrenderIsInterval\x10\xa2\x01\x12\x1b\n\x16\x45rr_SurrenderNotEnough\x10\xa3\x01\x12\x16\n\x11\x45rr_TechLevelFull\x10\xa4\x01\x12!\n\x1c\x45rr_PlayerTeleportWrongState\x10\xa5\x01\x12\x1e\n\x19\x45rr_PlayerTeleportHasPath\x10\xa6\x01\x12\x1e\n\x19\x45rr_PlayerTeleportHasBuff\x10\xa7\x01\x12 \n\x1b\x45rr_PlayerTeleportHasEntity\x10\xa8\x01\x12#\n\x1e\x45rr_PlayerTeleportNotTerritory\x10\xa9\x01\x12%\n Err_PlayerTeleportWrongTerritory\x10\xaa\x01\x12#\n\x1e\x45rr_PlayerTeleportWrongGridIdx\x10\xab\x01\x12\x1b\n\x16\x45rr_PlayerTeleportInCd\x10\xac\x01\x12 \n\x1b\x45rr_PlayerTeleportHasBattle\x10\xad\x01\x12\"\n\x1d\x45rr_PlayerTeleportApNotEnough\x10\xae\x01\x12 \n\x1b\x45rr_PlayerTeleportWrongGrid\x10\xaf\x01\x12 \n\x1b\x45rr_GeneralWrongPawnRainbow\x10\xb0\x01\x12$\n\x1f\x45rr_ChronoAssistanceWrongTarget\x10\xb1\x01\x12#\n\x1e\x45rr_ChronoAssistanceWrongParam\x10\xb2\x01\x12#\n\x1e\x45rr_ChronoAssistanceWrongState\x10\xb3\x01\x12\x1a\n\x15\x45rr_IceWallOutOfRange\x10\xb4\x01\x12\x1a\n\x15\x45rr_IceWallWrongState\x10\xb5\x01\x12\x18\n\x13\x45rr_IceWallOutOfMap\x10\xb6\x01\x12!\n\x1c\x45rr_SellItemWrongRainbowCard\x10\xb7\x01\x12\x1c\n\x17\x45rr_RadishWrongPosition\x10\xb8\x01\x12\x1a\n\x15\x45rr_SwitchRainbowSame\x10\xb9\x01\x12\x1e\n\x19\x45rr_SkillAimPosOutOfRange\x10\xba\x01\x12 \n\x1b\x45rr_CollectRadishWrongState\x10\xbb\x01\x12\x1d\n\x18\x45rr_GrowRadishWrongState\x10\xbc\x01\x12\x18\n\x13\x45rr_AmbushCheckFail\x10\xbd\x01\x12\x1f\n\x1a\x45rr_SkillChargeNotEnoughHp\x10\xbe\x01\x12\x1d\n\x18\x45rr_SkillScoutWrongParam\x10\xbf\x01\x12\x1f\n\x1a\x45rr_SkillScoutWrongGridIdx\x10\xc0\x01\x12\x1f\n\x1a\x45rr_SkillGarrisonHasCastle\x10\xc1\x01\x12\x1d\n\x18\x45rr_SkillGarrisonHasBuff\x10\xc2\x01\x12\x15\n\x10\x45rr_UrbanRelease\x10\xc3\x01\x12\x1b\n\x16\x45rr_SkillNotHasPrepare\x10\xc4\x01\x12\x16\n\x11\x45rr_SkillSoulLink\x10\xc5\x01\x12\x16\n\x11\x45rr_SkillYoNeSoul\x10\xc6\x01\x12\x19\n\x14\x45rr_CommonParamError\x10\xac\x02\x12\x17\n\x12\x45rr_CommonOutOfMap\x10\xad\x02\x12\x18\n\x13\x45rr_CommonHasCastle\x10\xae\x02\x12\x19\n\x14\x45rr_CommonGridFilled\x10\xaf\x02\x12\x19\n\x14\x45rr_CommonOutOfRange\x10\xb0\x02\x12\x1d\n\x18\x45rr_GunCarrierWrongParam\x10\xb1\x02\x12 \n\x1b\x45rr_GunCarrierUnableSummons\x10\xb2\x02\x12\x1f\n\x1a\x45rr_GunCarrierNoTargetGrid\x10\xb3\x02\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'base_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ERRORCODE']._serialized_start=232
  _globals['_ERRORCODE']._serialized_end=6268
  _globals['_BASEREQ']._serialized_start=35
  _globals['_BASEREQ']._serialized_end=94
  _globals['_BASERSP']._serialized_start=97
  _globals['_BASERSP']._serialized_end=229
# @@protoc_insertion_point(module_scope)