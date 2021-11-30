import datetime
import random
import string
from xmlrpc.server import SimpleXMLRPCServer
from enum import Enum


class Type(Enum):
    Normal = 1
    Fire = 2
    Water = 3
    Electric = 4
    Grass = 5
    Ice = 6
    Fighting = 7
    Poison = 8
    Ground = 9
    Flying = 10
    Psychic = 11
    Bug = 12
    Rock = 13
    Ghost = 14
    Dragon = 15
    Dark = 16
    Steel = 17
    Fairy = 18


# TypeChart.Chart[attackType][enemyType] -> syntax for checking pokemon dependencies
class TypeChart:
    Normal = {Type.Normal: 1, Type.Fire: 1, Type.Water: 1, Type.Electric: 1, Type.Grass: 1, Type.Ice: 1,
              Type.Fighting: 1, Type.Poison: 1, Type.Ground: 1, Type.Flying: 1, Type.Psychic: 1, Type.Bug: 1,
              Type.Rock: 0.5, Type.Ghost: 0, Type.Dragon: 1, Type.Dark: 1, Type.Steel: 0.5, Type.Fairy: 1}

    Fire = {Type.Normal: 1, Type.Fire: 0.5, Type.Water: 0.5, Type.Electric: 1, Type.Grass: 2, Type.Ice: 2,
            Type.Fighting: 1, Type.Poison: 1, Type.Ground: 1, Type.Flying: 1, Type.Psychic: 1, Type.Bug: 2,
            Type.Rock: 0.5, Type.Ghost: 1, Type.Dragon: 0.5, Type.Dark: 1, Type.Steel: 2, Type.Fairy: 1}

    Water = {Type.Normal: 1, Type.Fire: 2, Type.Water: 0.5, Type.Electric: 1, Type.Grass: 0.5, Type.Ice: 1,
             Type.Fighting: 1, Type.Poison: 1, Type.Ground: 2, Type.Flying: 1, Type.Psychic: 1, Type.Bug: 1,
             Type.Rock: 2, Type.Ghost: 1, Type.Dragon: 0.5, Type.Dark: 1, Type.Steel: 1, Type.Fairy: 1}

    Electric = {Type.Normal: 1, Type.Fire: 1, Type.Water: 2, Type.Electric: 0.5, Type.Grass: 0.5, Type.Ice: 1,
                Type.Fighting: 1, Type.Poison: 1, Type.Ground: 0, Type.Flying: 2, Type.Psychic: 1, Type.Bug: 1,
                Type.Rock: 1, Type.Ghost: 1, Type.Dragon: 0.5, Type.Dark: 1, Type.Steel: 1, Type.Fairy: 1}

    Grass = {Type.Normal: 1, Type.Fire: 0.5, Type.Water: 2, Type.Electric: 1, Type.Grass: 0.5, Type.Ice: 1,
             Type.Fighting: 1, Type.Poison: 0.5, Type.Ground: 2, Type.Flying: 0.5, Type.Psychic: 1, Type.Bug: 0.5,
             Type.Rock: 2, Type.Ghost: 1, Type.Dragon: 0.5, Type.Dark: 1, Type.Steel: 0.5, Type.Fairy: 1}

    Ice = {Type.Normal: 1, Type.Fire: 0.5, Type.Water: 0.5, Type.Electric: 1, Type.Grass: 2, Type.Ice: 0.5,
           Type.Fighting: 1, Type.Poison: 1, Type.Ground: 2, Type.Flying: 2, Type.Psychic: 1, Type.Bug: 1,
           Type.Rock: 1, Type.Ghost: 1, Type.Dragon: 2, Type.Dark: 1, Type.Steel: 0.5, Type.Fairy: 1}

    Fighting = {Type.Normal: 2, Type.Fire: 1, Type.Water: 1, Type.Electric: 1, Type.Grass: 1, Type.Ice: 2,
                Type.Fighting: 1, Type.Poison: 0.5, Type.Ground: 1, Type.Flying: 0.5, Type.Psychic: 0.5, Type.Bug: 0.5,
                Type.Rock: 2, Type.Ghost: 0, Type.Dragon: 1, Type.Dark: 2, Type.Steel: 2, Type.Fairy: 0.5}

    Poison = {Type.Normal: 1, Type.Fire: 1, Type.Water: 1, Type.Electric: 1, Type.Grass: 2, Type.Ice: 1,
              Type.Fighting: 1, Type.Poison: 0.5, Type.Ground: 0.5, Type.Flying: 1, Type.Psychic: 1, Type.Bug: 1,
              Type.Rock: 0.5, Type.Ghost: 0.5, Type.Dragon: 1, Type.Dark: 1, Type.Steel: 0, Type.Fairy: 2}

    Ground = {Type.Normal: 1, Type.Fire: 2, Type.Water: 1, Type.Electric: 2, Type.Grass: 0.5, Type.Ice: 1,
              Type.Fighting: 1, Type.Poison: 2, Type.Ground: 1, Type.Flying: 0, Type.Psychic: 1, Type.Bug: 0.5,
              Type.Rock: 2, Type.Ghost: 1, Type.Dragon: 1, Type.Dark: 1, Type.Steel: 2, Type.Fairy: 1}

    Flying = {Type.Normal: 1, Type.Fire: 1, Type.Water: 1, Type.Electric: 0.5, Type.Grass: 2, Type.Ice: 1,
              Type.Fighting: 2, Type.Poison: 1, Type.Ground: 1, Type.Flying: 1, Type.Psychic: 1, Type.Bug: 2,
              Type.Rock: 0.5, Type.Ghost: 1, Type.Dragon: 1, Type.Dark: 1, Type.Steel: 0.5, Type.Fairy: 1}

    Psychic = {Type.Normal: 1, Type.Fire: 1, Type.Water: 1, Type.Electric: 1, Type.Grass: 1, Type.Ice: 1,
               Type.Fighting: 2, Type.Poison: 2, Type.Ground: 1, Type.Flying: 1, Type.Psychic: 0.5, Type.Bug: 1,
               Type.Rock: 1, Type.Ghost: 1, Type.Dragon: 1, Type.Dark: 0, Type.Steel: 0.5, Type.Fairy: 1}

    Bug = {Type.Normal: 1, Type.Fire: 0.5, Type.Water: 1, Type.Electric: 1, Type.Grass: 2, Type.Ice: 1,
           Type.Fighting: 0.5, Type.Poison: 0.5, Type.Ground: 1, Type.Flying: 0.5, Type.Psychic: 2, Type.Bug: 1,
           Type.Rock: 1, Type.Ghost: 0.5, Type.Dragon: 1, Type.Dark: 2, Type.Steel: 0.5, Type.Fairy: 0.5}

    Rock = {Type.Normal: 1, Type.Fire: 2, Type.Water: 1, Type.Electric: 1, Type.Grass: 1, Type.Ice: 2,
            Type.Fighting: 0.5, Type.Poison: 1, Type.Ground: 0.5, Type.Flying: 2, Type.Psychic: 1, Type.Bug: 2,
            Type.Rock: 1, Type.Ghost: 1, Type.Dragon: 1, Type.Dark: 1, Type.Steel: 0.5, Type.Fairy: 1}

    Ghost = {Type.Normal: 0, Type.Fire: 1, Type.Water: 1, Type.Electric: 1, Type.Grass: 1, Type.Ice: 1,
             Type.Fighting: 1, Type.Poison: 1, Type.Ground: 1, Type.Flying: 1, Type.Psychic: 2, Type.Bug: 1,
             Type.Rock: 1, Type.Ghost: 2, Type.Dragon: 1, Type.Dark: 0.5, Type.Steel: 1, Type.Fairy: 1}

    Dragon = {Type.Normal: 1, Type.Fire: 1, Type.Water: 1, Type.Electric: 1, Type.Grass: 1, Type.Ice: 1,
              Type.Fighting: 1, Type.Poison: 1, Type.Ground: 1, Type.Flying: 1, Type.Psychic: 1, Type.Bug: 1,
              Type.Rock: 1, Type.Ghost: 1, Type.Dragon: 2, Type.Dark: 1, Type.Steel: 0.5, Type.Fairy: 0}

    Dark = {Type.Normal: 1, Type.Fire: 1, Type.Water: 1, Type.Electric: 1, Type.Grass: 1, Type.Ice: 1,
            Type.Fighting: 0.5, Type.Poison: 1, Type.Ground: 1, Type.Flying: 1, Type.Psychic: 2, Type.Bug: 1,
            Type.Rock: 1, Type.Ghost: 2, Type.Dragon: 1, Type.Dark: 0.5, Type.Steel: 1, Type.Fairy: 0.5}

    Steel = {Type.Normal: 1, Type.Fire: 0.5, Type.Water: 0.5, Type.Electric: 0.5, Type.Grass: 1, Type.Ice: 2,
             Type.Fighting: 1, Type.Poison: 1, Type.Ground: 1, Type.Flying: 1, Type.Psychic: 1, Type.Bug: 1,
             Type.Rock: 2, Type.Ghost: 1, Type.Dragon: 1, Type.Dark: 1, Type.Steel: 0.5, Type.Fairy: 2}

    Fairy = {Type.Normal: 1, Type.Fire: 0.5, Type.Water: 1, Type.Electric: 1, Type.Grass: 1, Type.Ice: 1,
             Type.Fighting: 2, Type.Poison: 0.5, Type.Ground: 1, Type.Flying: 1, Type.Psychic: 1, Type.Bug: 1,
             Type.Rock: 1, Type.Ghost: 1, Type.Dragon: 2, Type.Dark: 2, Type.Steel: 0.5, Type.Fairy: 1}

    Chart = {Type.Normal: Normal, Type.Fire: Fire, Type.Water: Water, Type.Electric: Electric, Type.Grass: Grass,
             Type.Ice: Ice, Type.Fighting: Fighting, Type.Poison: Poison, Type.Ground: Ground, Type.Flying: Flying,
             Type.Psychic: Psychic, Type.Bug: Bug, Type.Rock: Rock, Type.Ghost: Ghost, Type.Dragon: Dragon,
             Type.Dark: Dark, Type.Steel: Steel, Type.Fairy: Fairy}


class MoveType(Enum):
    Status = 1
    Physical = 2
    Special = 3


class Move:
    def __init__(self, name: string, attackType: Type, category: MoveType, power: int, acc: int):
        self.name = name
        self.type = attackType
        self.category = category
        self.power = power
        self.accuracy = acc


class PokemonData:
    def __init__(self, name: string, pokemonType: list[Type], hpMax: int, attack: int, defense: int, spAtk: int,
                 spDef: int, speed: int, moves: list[Move]):
        self.name = name
        self.pokemonType = pokemonType
        self.hpMax = hpMax
        self.attack = attack
        self.defense = defense
        self.spAtk = spAtk
        self.spDef = spDef
        self.speed = speed
        self.moves = moves


class Pokemon:
    def __init__(self, data: PokemonData):
        self.data = data
        self.hpCurrent = data.hpMax


# class PlayerContext:
#     def __init__(self, name: string, password: string):
#         self.playerName = name
#         self.password = password
#
#     def LogIn(self, password: string):
#         if self.password == password:
#             return True
#         return False


class Player:
    def __init__(self, playerId: int):
        self.playerId = playerId
        self.pokemons = []
        self.activePokemonIndex = 0
        self.InGame = False
        self.Ready = False

    def AddPokemon(self, pokemon: Pokemon):
        if len(self.pokemons) < 4:
            self.pokemons.append(pokemon)

    def SetActivePokemon(self, index: int):
        self.activePokemonIndex = index

    def GetActivePokemon(self):
        return self.pokemons[self.activePokemonIndex]


class ServerContext:
    def __init__(self):
        self.totalNumberOfGames = 0
        self.runningGames = []
        self.totalNumberOfPlayers = 0
        self.freedPlayerIds = []

    def SetPokmonDB(self, pokmons):
        self.pokmonsData=pokmons

    def RegisterGame(self, name: string, password: string, player1: Player):
        newGame = Game(name, password, player1)
        self.totalNumberOfGames += 1
        self.runningGames.append(newGame)
        return newGame

    def UnregisterGame(self, gameName):
        for game in self.runningGames:
            if game.gameName == gameName:
                self.runningGames.remove(game)

    def RegisterPlayer(self):
        freeId = self.__GetFreePlayerId()

        player = Player(freeId)
        return player

    def UnregisterPlayer(self,playerId):
        self.freedPlayerIds.append(playerId)

    def __GetFreePlayerId(self):
        if len(self.freedPlayerIds) == 0:
            self.totalNumberOfPlayers += 1
            return self.totalNumberOfPlayers-1
        else:
            freeId = self.freedPlayerIds[0]
            del self.freedPlayerIds[0]
            return freeId

    def GetGameByName(self, gameName):
        for game in self.runningGames:
            if game.gameName == gameName:
                return game
        return False


class Game:
    def __init__(self, name: string, password: string, player1: Player):
        self.gameName = name
        self.password = password
        self.player1 = player1
        self.player2 = Player(-100)
        self.state = 0
        self.messages = []
        self.firstPlayerTurn = random.choice([True, False])
        self.lastAttackTime = datetime.datetime.now()

    def GetPlayerById(self, playerId: int):
        if self.player1.playerId == playerId:
            return self.player1
        if self.player2.playerId == playerId:
            return self.player2

    def GetOtherPlayer(self, playerId: int):
        if self.player1.playerId == playerId:
            return self.player2
        if self.player2.playerId == playerId:
            return self.player1
        return None

    def AddSecondPlayer(self,player2: Player):
        self.player2 = player2

    def AddMessage(self, messageText:string):
        self.messages.append(Message(messageText, self.state))

    def CheckIfTurn(self, playerId: int):
        # print(self.firstPlayerTurn)
        # print(not self.firstPlayerTurn)
        # print(self.player1.playerId == playerId)
        # print(self.player2.playerId == playerId)

        if self.player1.playerId == playerId and self.firstPlayerTurn:
            return True
        if self.player2.playerId == playerId and (not self.firstPlayerTurn):
            return True
        return False

    def GetNeededMessages(self,state:int):
        retMessages = []
        for m in self.messages:
            if m.state > state:
                retMessages.append(m.message)
        return retMessages

Context = ServerContext()


class CreateNewOrJoinGameResponse:
    def __init__(self, successful: bool, playerId: int = -1, gameName: string = "", errorMessage: string = ""):
        self.successful = successful
        self.playerId = playerId
        self.gameName = gameName
        self.errorMessage = errorMessage


def TryCreateNewGame(gameName: string, gamePassword: string):
    if Context.GetGameByName(gameName)!=False:
        print("Failed to create new game; Name already taken...")
        response = CreateNewOrJoinGameResponse(False, errorMessage="Game with name " + gameName + " already exists!")
        return response

    player = Context.RegisterPlayer()
    player.InGame = True
    game = Context.RegisterGame(gameName, gamePassword, player)
    print("Successfully Created Game")
    response = CreateNewOrJoinGameResponse(True, player.playerId, game.gameName)
    return response


def TryJoinGame(gameName: string, gamePassword: string):
    game = Context.GetGameByName(gameName)
    if game == False:
        print("Failed to join game! \n\n No such game exists...")
        response = CreateNewOrJoinGameResponse(False, errorMessage="Failed to join game! \n\n No game with name "+gameName+" exists...")
        return response
    
    if game.password != gamePassword:
        print("Failed to join game! \n\n Incorrect password...")
        response = CreateNewOrJoinGameResponse(False, errorMessage="Failed to join game! \n\n Incorrect password...")
        return response
    if not game.player2.playerId == -100:
        response = CreateNewOrJoinGameResponse(False, errorMessage="Failed to join game! \n\n Game already full...")
        return response
    
    player = Context.RegisterPlayer()
    player.InGame = True
    game.AddSecondPlayer(player)
    print("Successfully Joined Game")
    response = CreateNewOrJoinGameResponse(True, player.playerId, game.gameName)
    return response


class PokmonDataResponse:
    def __init__(self,name: string, type: string):
        self.name = name
        self.type = type


def GetAllPokmonList():
    pokmons = Context.pokmonsData
    response = []
    for pokmon in pokmons:
        types = ""
        for type in pokmon.pokemonType:
            types = types+", "+type.name
        response.append(PokmonDataResponse(pokmon.name, types))
    return response


class PlayerReadyResponse:
    def __init__(self, inGame, Ready):
        self.inGame=inGame
        self.Ready=Ready


def CheckIfSecondPlayerReady(gameName, playerId):
    otherPlayer = Context.GetGameByName(gameName).GetOtherPlayer(playerId)
    if otherPlayer is None:
        return PlayerReadyResponse(False, False)
    return PlayerReadyResponse(otherPlayer.InGame, otherPlayer.Ready)


def SetPlayerPokmons(gameName, playerId, pokmons):
    player = Context.GetGameByName(gameName).GetPlayerById(playerId)
    if player.Ready:
        return True
    print(pokmons)
    for pok in pokmons:
        for pokmon in Context.pokmonsData:
            if pokmon.name == pok:
                player.AddPokemon(Pokemon(pokmon))
    player.Ready = True
    return True


class GetPokmonAttacksResponse:
    def __init__(self, successful: bool, attacksList, errorMessage: string = ""):
        self.successful = successful
        self.attacksList = attacksList
        self.errorMessage = errorMessage


def TryGetPokmonAttacks(playerId, gameName):
    attackList = GetPlayerPokemon(gameName, playerId).data.moves
    attackListResponse = []
    for attack in attackList:
        attackListResponse.append(attack.name)
    response = GetPokmonAttacksResponse(True, attackListResponse)
    return response


class PokmonAttackResponse:
    def __init__(self, successful: bool, message, errorMessage: string = ""):
        self.successful = successful
        self.message = message
        self.errorMessage = errorMessage


def TryPerformAttack(gameName, playerId, attackId):
    game = Context.GetGameByName(gameName)
    nowTime = datetime.datetime.now()
    difference = (nowTime - game.lastAttackTime).total_seconds()
    print(difference)
    if difference < 4:
        return False

    game.lastAttackTime = nowTime

    response = PokmonAttackResponse(True, "Attack Successful")
    game.state += 1
    attackingPokmon = GetPlayerPokemon(gameName, playerId)
    defendingPokmon = game.GetOtherPlayer(playerId).GetActivePokemon()

    game.AddMessage(attackingPokmon.data.name + " uses " + attackingPokmon.data.moves[attackId].name + "!")

    if (random.uniform(0, 100) - attackingPokmon.data.moves[attackId].accuracy) > 0:
        game.AddMessage("But it missed...")
    else:
        [damageFloat, bonus] = CalculateAttackDamage(attackingPokmon, attackId, defendingPokmon)
        damage = int(round(damageFloat))

        defendingPokmon.hpCurrent -= damage



        if bonus == 0:
            game.AddMessage("But it had no effect...")
        elif bonus < 1:
            game.AddMessage("It's not very effective...")
        elif bonus > 1:
            game.AddMessage("It's super effective")

        if defendingPokmon.hpCurrent <= 0:
            defendingPokmon.hpCurrent = 0
            game.AddMessage(defendingPokmon.data.name+" fainted...")

    game.firstPlayerTurn = not game.firstPlayerTurn

    return response


def CalculateAttackDamage(attackingPokmon, attackId, defendingPokmon):
    move = attackingPokmon.data.moves[attackId]
    P = move.power
    A = 0
    D = 0
    if move.category == MoveType.Physical:
        A = attackingPokmon.data.attack
        D = attackingPokmon.data.defense
    else:
        A = attackingPokmon.data.spAtk
        D = attackingPokmon.data.spDef
    rand = random.uniform(0.85, 1.0)
    STAB = 1
    typeBonus = 1
    for attType in attackingPokmon.data.pokemonType:
        if attType == move.type:
            STAB = 1.5
    for defType in defendingPokmon.data.pokemonType:
        typeBonus *= TypeChart.Chart[move.type][defType]
    damage = (2+(3*P*(A/D))/50)*rand*STAB*typeBonus
    return [damage, typeBonus]


def GetPlayerPokemon(gameName: string, playerId: int):
    return Context.GetGameByName(gameName).GetPlayerById(playerId).GetActivePokemon()


class GetPokmonAttacksDescriptionResponse:
    def __init__(self, successful: bool, description, errorMessage: string = ""):
        self.successful = successful
        self.description = description
        self.errorMessage = errorMessage


def TryGetPokmonAttacksDescription(playerId, gameName, id):
    attack = GetPlayerPokemon(gameName, playerId).data.moves[id]
    description = attack.name+"\n"+attack.type.name+" / "+attack.category.name+"\nAcc: "+str(attack.accuracy)+", Pow: "+str(attack.power)
    print(description)
    response = GetPokmonAttacksDescriptionResponse(True, description)
    return response


class Message:
    def __init__(self, message: string, state: int):
        self.message = message
        self.state = state


class BattlePageData:
    def __init__(self, turn: bool, messages: list[string], myPokmonName: string, otherPokmonName: string, playerHp: int, otherHp: int, playerMaxHp: int, otherMaxHp: int, state: int):
        self.turn = turn
        self.messages = messages
        self.myPokmonName = myPokmonName
        self.otherPokmonName = otherPokmonName
        self.playerHp = playerHp
        self.otherHp = otherHp
        self.playerMaxHp = playerMaxHp
        self.otherMaxHp = otherMaxHp
        self.state = state


def GetBattlePageData(playerId, gameName, state):
    game = Context.GetGameByName(gameName)
    if game.state <= state:
        return False
    response = BattlePageData(game.CheckIfTurn(playerId), game.GetNeededMessages(state),
                              game.GetPlayerById(playerId).GetActivePokemon().data.name, game.GetOtherPlayer(playerId).GetActivePokemon().data.name,
                              game.GetPlayerById(playerId).GetActivePokemon().hpCurrent, game.GetOtherPlayer(playerId).GetActivePokemon().hpCurrent,
                              game.GetPlayerById(playerId).GetActivePokemon().data.hpMax, game.GetOtherPlayer(playerId).GetActivePokemon().data.hpMax,
                              game.state)
    return response


def TryGetChosenPokmonList(gameName, playerId):
    player = Context.GetGameByName(gameName).GetPlayerById(playerId)
    pokmons = player.pokemons
    response = []
    for pokmon in pokmons:
        if pokmon.hpCurrent <= 0:
            continue

        types = ""
        for type in pokmon.data.pokemonType:
            types = types + ", " + type.name
        response.append(PokmonDataResponse(pokmon.data.name, types))
    return response


def TrySetActivePokmon(gameName, playerId, pokmonName, OnDeathSwitch):
    game = Context.GetGameByName(gameName)
    player = game.GetPlayerById(playerId)
    for idx, val in enumerate(player.pokemons):
        if val.data.name == pokmonName:
            player.SetActivePokemon(idx)
    game.state += 1
    if not OnDeathSwitch:
        game.firstPlayerTurn = not game.firstPlayerTurn
    return True


if __name__ == '__main__':
    print("Loading initial values...")
    print("Loading moves...")
    Tackle = Move("Tackle", Type.Normal, MoveType.Physical, 40, 100)
    KnockOff = Move("Knock Off", Type.Dark, MoveType.Physical, 65, 100)
    ArmThrust = Move("Arm Thrust", Type.Fighting, MoveType.Physical, 15, 100)
    VitalThrow = Move("Cross Chop", Type.Fighting, MoveType.Physical, 70, 100)

    SludgeBomb = Move("Sludge Bomb", Type.Poison, MoveType.Special, 90, 100)
    Assurance = Move("Assurance", Type.Dark, MoveType.Physical, 60, 100)
    Smog = Move("Smog", Type.Poison, MoveType.Special, 30, 70)

    Scratch = Move("Scratch", Type.Normal, MoveType.Physical, 40, 100)
    Astonish = Move("Astonish", Type.Ghost, MoveType.Physical, 30, 100)
    Bulldoze = Move("Bulldoze", Type.Ground, MoveType.Physical, 60, 100)
    EarthPower = Move("Earth Power", Type.Ground, MoveType.Special, 90, 100)

    ShadowSneak = Move("Shadow Sneak", Type.Ghost, MoveType.Physical, 40, 100)
    Hex = Move("Hex", Type.Ghost, MoveType.Special, 65, 100)
    HiddenPower = Move("Hidden Power", Type.Normal, MoveType.Special, 60, 100)

    ThunderShock = Move("Thunder Shock", Type.Electric, MoveType.Special, 40, 100)
    GearGrind = Move("Gear Grind", Type.Steel, MoveType.Physical, 50, 100)
    ViseGrip = Move("Vise Grip", Type.Normal, MoveType.Physical, 55, 100)
    FlashCannon = Move("Flash Cannon", Type.Steel, MoveType.Special, 80, 100)

    Ember = Move("Ember", Type.Fire, MoveType.Special, 40, 100)
    FlameCharge = Move("Flame Charge", Type.Fire, MoveType.Physical, 50, 100)
    HeadSmash = Move("Head Smash", Type.Rock, MoveType.Physical, 150, 80)

    WaterGun = Move("Water Gun", Type.Water, MoveType.Special, 40, 100)
    IcePunch = Move("Ice Punch", Type.Ice, MoveType.Physical, 75, 100)
    AquaTail = Move("Aqua Tail", Type.Water, MoveType.Physical, 90, 90)

    Absorb = Move("Absorb", Type.Grass, MoveType.Special, 20, 100)
    MegaDrain = Move("Mega Drain", Type.Grass, MoveType.Special, 40, 100)
    Payback = Move("Payback", Type.Dark, MoveType.Physical, 50, 100)

    Nuzzle = Move("Nuzzle", Type.Electric, MoveType.Physical, 20, 100)
    QuickAttack = Move("Quick Attack", Type.Normal, MoveType.Physical, 40, 100)
    Spark = Move("Spark", Type.Electric, MoveType.Physical, 65, 100)
    DisarmingVoice = Move("Disarming Voice", Type.Fairy, MoveType.Special, 40, 1000)

    Confusion = Move("Confusion", Type.Psychic, MoveType.Special, 50, 100)
    Swift = Move("Swift", Type.Normal, MoveType.Special, 60, 1000)
    AncientPower = Move("Ancient Power", Type.Rock, MoveType.Special, 60, 100)
    PsychoCut = Move("Psycho Cut", Type.Psychic, MoveType.Physical, 70, 100)

    PowderSnow = Move("Powder Snow", Type.Ice, MoveType.Special, 40, 100)
    IceShard = Move("Ice Shard", Type.Ice, MoveType.Physical, 40, 100)
    IceFang = Move("Ice Fang", Type.Ice, MoveType.Physical, 65, 95)

    Twister = Move("Twister", Type.Dragon, MoveType.Special, 40, 100)
    DragonRush = Move("Twister", Type.Dragon, MoveType.Physical, 100, 75)
    Slam = Move("Slam", Type.Normal, MoveType.Physical, 80, 75)

    Snarl = Move("Snarl", Type.Dark, MoveType.Special, 55, 95)
    PlayRough = Move("Play Rough", Type.Fairy, MoveType.Physical, 90, 90)

    Covet = Move("Covet", Type.Normal, MoveType.Physical, 60, 100)
    Round = Move("Round", Type.Normal, MoveType.Special, 60, 100)



    print("Loading pokemon...")
    Makuhita = PokemonData("Makuhita", [Type.Fighting], 72, 60, 30, 20, 30, 25, [Tackle, KnockOff, ArmThrust, VitalThrow])
    Koffing = PokemonData("Koffing", [Type.Poison], 40, 65, 95, 60, 45, 35, [Tackle, SludgeBomb, Assurance, Smog])
    Diglett = PokemonData("Diglett", [Type.Ground], 10, 55, 30, 35, 45, 90, [Scratch, Astonish, Bulldoze, EarthPower])
    Shuppet = PokemonData("Shuppet", [Type.Ghost], 44, 75, 35, 63, 33, 45, [KnockOff, ShadowSneak, Hex, HiddenPower])
    Klink = PokemonData("Klink", [Type.Steel], 40, 55, 70, 45, 60, 30, [ThunderShock, GearGrind, ViseGrip, FlashCannon])
    Tepig = PokemonData("Tepig", [Type.Fire], 65, 63, 45, 45, 45, 45, [Tackle, Ember, FlameCharge, HeadSmash])
    Squirtle = PokemonData("Squirtle", [Type.Water], 44, 48, 65, 50, 64, 43, [Tackle, WaterGun, IcePunch, AquaTail])
    Seedot = PokemonData("Seedot", [Type.Grass], 40, 40, 50, 30, 30, 30, [Tackle, Absorb, MegaDrain, Payback])
    Pikachu = PokemonData("Pikachu", [Type.Electric], 35, 55, 40, 50, 50, 90, [Nuzzle, QuickAttack, Spark, DisarmingVoice])
    Wobbuffet = PokemonData("Wobbuffet", [Type.Psychic], 190, 33, 58, 33, 58, 33, [Confusion, Swift, AncientPower, PsychoCut])
    Snorunt = PokemonData("Snorunt", [Type.Ice], 50, 50, 50, 50, 50, 50, [Astonish, PowderSnow, IceShard, IceFang])
    Dratini = PokemonData("Dratini", [Type.Dragon], 41, 64, 45, 50, 50, 50, [Twister, AquaTail, DragonRush, Slam])
    Purrloin = PokemonData("Purrloin", [Type.Dark], 41, 50, 37, 50, 37, 66, [Scratch, Assurance, Snarl, PlayRough])
    Jigglypuff = PokemonData("Jigglypuff", [Type.Normal, Type.Fairy], 115, 45, 20, 45, 25, 20, [DisarmingVoice, Covet, Round, PlayRough])

    Context.SetPokmonDB([Makuhita, Koffing, Diglett, Shuppet, Klink, Tepig, Squirtle, Seedot, Pikachu, Wobbuffet, Snorunt, Dratini, Purrloin, Jigglypuff])

    print("Starting...")
    server = SimpleXMLRPCServer(("localhost", 5000))
    # Space to register functions server.register_function(functionName)
    server.register_function(TryCreateNewGame)
    server.register_function(TryJoinGame)
    server.register_function(GetAllPokmonList)
    server.register_function(CheckIfSecondPlayerReady)
    server.register_function(SetPlayerPokmons)
    server.register_function(TryGetPokmonAttacks)
    server.register_function(TryPerformAttack)
    server.register_function(TryGetPokmonAttacksDescription)
    server.register_function(GetBattlePageData)
    server.register_function(TryGetChosenPokmonList)
    server.register_function(TrySetActivePokmon)

    server.serve_forever()



