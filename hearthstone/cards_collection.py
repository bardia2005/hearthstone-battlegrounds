import random
from .card import MinionCard
from .spell import SpellCard, WeaponCard


# ============== SPELL EFFECTS ==============

def coin_effect(owner, game, target):
    owner.mana = min(owner.mana + 1, 10)
    game.add_log(f"{owner.name} gains 1 mana crystal this turn!")

def fireball_effect(owner, game, target):
    if target:
        target.take_damage(6, game)
        game.add_log(f"Fireball deals 6 damage!")

def frostbolt_effect(owner, game, target):
    if target:
        target.take_damage(3, game)
        if hasattr(target, 'frozen'):
            target.frozen = True
            game.add_log(f"Frostbolt deals 3 damage and freezes {target.name}!")
        else:
            game.add_log(f"Frostbolt deals 3 damage!")

def arcane_intellect_effect(owner, game, target):
    owner.draw_card(game, 2)

def polymorph_effect(owner, game, target):
    if target and hasattr(target, 'name'):
        enemy = game.get_opponent(owner)
        if target in enemy.board:
            idx = enemy.board.index(target)
            from .minion import Minion
            sheep = Minion("Sheep", 1, 1)
            enemy.board[idx] = sheep
            game.add_log(f"{target.name} is transformed into a Sheep!")

def flamestrike_effect(owner, game, target):
    enemy = game.get_opponent(owner)
    for minion in enemy.board:
        minion.take_damage(4, game)
    game.add_log("Flamestrike deals 4 damage to all enemy minions!")

def holy_nova_effect(owner, game, target):
    enemy = game.get_opponent(owner)
    for minion in enemy.board:
        minion.take_damage(2, game)
    for minion in owner.board:
        minion.heal(2)
    owner.heal(2)
    game.add_log("Holy Nova deals 2 damage to enemies, heals friendlies for 2!")

def holy_light_effect(owner, game, target):
    if target:
        healed = target.heal(8) if hasattr(target, 'heal') else 0
        game.add_log(f"Holy Light restores {healed} health!")

def consecration_effect(owner, game, target):
    enemy = game.get_opponent(owner)
    enemy.take_damage(2, game)
    for minion in enemy.board:
        minion.take_damage(2, game)
    game.add_log("Consecration deals 2 damage to all enemies!")

def swipe_effect(owner, game, target):
    enemy = game.get_opponent(owner)
    if target:
        target.take_damage(4, game)
    for minion in enemy.board:
        if minion != target:
            minion.take_damage(1, game)
    if target != enemy:
        enemy.take_damage(1, game)
    game.add_log("Swipe deals 4 damage to target, 1 to all other enemies!")

def sprint_effect(owner, game, target):
    owner.draw_card(game, 4)

def assassinate_effect(owner, game, target):
    if target and hasattr(target, 'health'):
        target.health = 0
        game.add_log(f"Assassinate destroys {target.name}!")

def backstab_effect(owner, game, target):
    if target and hasattr(target, 'health'):
        if target.health == target.max_health:
            target.take_damage(2, game)
            game.add_log(f"Backstab deals 2 damage to {target.name}!")
        else:
            game.add_log("Backstab can only target undamaged minions!")

def execute_effect(owner, game, target):
    if target and hasattr(target, 'health'):
        if target.health < target.max_health:
            target.health = 0
            game.add_log(f"Execute destroys {target.name}!")
        else:
            game.add_log("Execute can only target damaged minions!")

def shield_block_effect(owner, game, target):
    owner.gain_armor(5, game)
    owner.draw_card(game, 1)

def blessing_of_kings_effect(owner, game, target):
    if target and hasattr(target, 'buff'):
        target.buff(4, 4, game)

def power_word_shield_effect(owner, game, target):
    if target and hasattr(target, 'buff'):
        target.buff(0, 2, game)
        owner.draw_card(game, 1)

def shadow_word_pain_effect(owner, game, target):
    if target and hasattr(target, 'attack') and target.attack <= 3:
        target.health = 0
        game.add_log(f"Shadow Word: Pain destroys {target.name}!")
    else:
        game.add_log("Target must have 3 or less attack!")

def shadow_word_death_effect(owner, game, target):
    if target and hasattr(target, 'attack') and target.attack >= 5:
        target.health = 0
        game.add_log(f"Shadow Word: Death destroys {target.name}!")
    else:
        game.add_log("Target must have 5 or more attack!")

def mind_control_effect(owner, game, target):
    if target and hasattr(target, 'name'):
        enemy = game.get_opponent(owner)
        if target in enemy.board and len(owner.board) < 7:
            enemy.board.remove(target)
            owner.board.append(target)
            target.can_attack = False
            game.add_log(f"Mind Control steals {target.name}!")

def silence_effect(owner, game, target):
    if target and hasattr(target, 'silence'):
        target.silence(game)


# ============== BATTLECRY EFFECTS ==============

def elven_archer_battlecry(owner, game, target):
    if target:
        target.take_damage(1, game)
        game.add_log(f"Elven Archer deals 1 damage!")

def nightblade_battlecry(owner, game, target):
    enemy = game.get_opponent(owner)
    enemy.take_damage(3, game)
    game.add_log(f"Nightblade deals 3 damage to enemy hero!")

def darkscale_healer_battlecry(owner, game, target):
    owner.heal(2)
    for minion in owner.board:
        minion.heal(2)
    game.add_log("Darkscale Healer restores 2 health to all friendlies!")

def fire_elemental_battlecry(owner, game, target):
    if target:
        target.take_damage(3, game)
        game.add_log(f"Fire Elemental deals 3 damage!")

def defender_of_argus_battlecry(owner, game, target):
    idx = len(owner.board) - 1
    for minion in owner.board:
        if minion.name == "Defender of Argus":
            idx = owner.board.index(minion)
            break
    if idx > 0:
        owner.board[idx-1].buff(1, 1, game)
        owner.board[idx-1].taunt = True
    if idx < len(owner.board) - 1:
        owner.board[idx+1].buff(1, 1, game)
        owner.board[idx+1].taunt = True
    game.add_log("Defender of Argus buffs adjacent minions!")

def shattered_sun_cleric_battlecry(owner, game, target):
    if target and hasattr(target, 'buff') and target in owner.board:
        target.buff(1, 1, game)

def abusive_sergeant_battlecry(owner, game, target):
    if target and hasattr(target, 'attack'):
        target.attack += 2
        game.add_log(f"{target.name} gains +2 attack this turn!")

def ironforge_rifleman_battlecry(owner, game, target):
    if target:
        target.take_damage(1, game)
        game.add_log(f"Ironforge Rifleman deals 1 damage!")

def stormpike_commando_battlecry(owner, game, target):
    if target:
        target.take_damage(2, game)
        game.add_log(f"Stormpike Commando deals 2 damage!")

def acidic_swamp_ooze_battlecry(owner, game, target):
    enemy = game.get_opponent(owner)
    if enemy.weapon:
        game.add_log(f"{enemy.weapon.name} is destroyed!")
        enemy.weapon = None

def big_game_hunter_battlecry(owner, game, target):
    if target and hasattr(target, 'attack') and target.attack >= 7:
        target.health = 0
        game.add_log(f"Big Game Hunter destroys {target.name}!")


# ============== DEATHRATTLE EFFECTS ==============

def loot_hoarder_deathrattle(owner, game):
    owner.draw_card(game)

def harvest_golem_deathrattle(owner, game):
    from .minion import Minion
    if len(owner.board) < 7:
        damaged_golem = Minion("Damaged Golem", 2, 1)
        owner.board.append(damaged_golem)
        game.add_log("Harvest Golem summons a 2/1 Damaged Golem!")

def cairne_bloodhoof_deathrattle(owner, game):
    from .minion import Minion
    if len(owner.board) < 7:
        baine = Minion("Baine Bloodhoof", 4, 5)
        owner.board.append(baine)
        game.add_log("Cairne summons Baine Bloodhoof!")

def sylvanas_deathrattle(owner, game):
    enemy = game.get_opponent(owner)
    if enemy.board:
        stolen = random.choice(enemy.board)
        enemy.board.remove(stolen)
        if len(owner.board) < 7:
            owner.board.append(stolen)
            game.add_log(f"Sylvanas steals {stolen.name}!")

def tirion_deathrattle(owner, game):
    from .spell import Weapon
    owner.weapon = Weapon("Ashbringer", 5, 3)
    game.add_log("Tirion equips Ashbringer!")

def sludge_belcher_deathrattle(owner, game):
    from .minion import Minion
    if len(owner.board) < 7:
        slime = Minion("Slime", 1, 2, taunt=True)
        owner.board.append(slime)
        game.add_log("Sludge Belcher summons a 1/2 Slime with Taunt!")


# ============== HERO POWERS ==============

def mage_hero_power(owner, game, target):
    if target:
        target.take_damage(1, game)
        game.add_log(f"Fireblast deals 1 damage!")

def warrior_hero_power(owner, game, target):
    owner.gain_armor(2, game)

def priest_hero_power(owner, game, target):
    if target:
        healed = target.heal(2) if hasattr(target, 'heal') else 0
        game.add_log(f"Lesser Heal restores {healed} health!")

def hunter_hero_power(owner, game, target):
    enemy = game.get_opponent(owner)
    enemy.take_damage(2, game)
    game.add_log("Steady Shot deals 2 damage to enemy hero!")

def paladin_hero_power(owner, game, target):
    from .minion import Minion
    if len(owner.board) < 7:
        recruit = Minion("Silver Hand Recruit", 1, 1)
        owner.board.append(recruit)
        game.add_log("Reinforce summons a 1/1 Silver Hand Recruit!")

def warlock_hero_power(owner, game, target):
    owner.take_damage(2, game)
    owner.draw_card(game)
    game.add_log("Life Tap: Draw a card, take 2 damage!")


# ============== CARD COLLECTIONS ==============

def get_basic_minions():
    return [
        MinionCard("Wisp", 0, 1, 1, "A wisp of nothing"),
        MinionCard("Murloc Raider", 1, 2, 1, "Mrglglgl!"),
        MinionCard("Bloodfen Raptor", 2, 3, 2, "Basic beast"),
        MinionCard("River Crocolisk", 2, 2, 3, "Lurks in rivers"),
        MinionCard("Magma Rager", 3, 5, 1, "Glass cannon"),
        MinionCard("Chillwind Yeti", 4, 4, 5, "Solid stats"),
        MinionCard("Sen'jin Shieldmasta", 4, 3, 5, "Taz'dingo!", taunt=True),
        MinionCard("Boulderfist Ogre", 6, 6, 7, "Big and dumb"),
        MinionCard("War Golem", 7, 7, 7, "Perfectly balanced"),
        MinionCard("Core Hound", 7, 9, 5, "Fiery beast"),
        MinionCard("Stonetusk Boar", 1, 1, 1, "Charge!", charge=True),
        MinionCard("Bluegill Warrior", 2, 2, 1, "Mrglglgl!", charge=True),
        MinionCard("Wolfrider", 3, 3, 1, "For the Horde!", charge=True),
        MinionCard("Kor'kron Elite", 4, 4, 3, "Charge!", charge=True),
        MinionCard("Goldshire Footman", 1, 1, 2, "Ready for action!", taunt=True),
        MinionCard("Frostwolf Grunt", 2, 2, 2, "For the Frostwolves!", taunt=True),
        MinionCard("Ironfur Grizzly", 3, 3, 3, "Rawr!", taunt=True),
        MinionCard("Lord of the Arena", 6, 6, 5, "Big taunt", taunt=True),
    ]


def get_special_minions():
    return [
        MinionCard("Elven Archer", 1, 1, 1, "Battlecry: Deal 1 damage", battlecry=elven_archer_battlecry),
        MinionCard("Nightblade", 5, 4, 4, "Battlecry: Deal 3 to enemy hero", battlecry=nightblade_battlecry),
        MinionCard("Darkscale Healer", 5, 4, 5, "Battlecry: Heal all friendlies for 2", battlecry=darkscale_healer_battlecry),
        MinionCard("Fire Elemental", 6, 6, 5, "Battlecry: Deal 3 damage", rarity="Rare", battlecry=fire_elemental_battlecry),
        MinionCard("Defender of Argus", 4, 2, 3, "Battlecry: Give adjacent +1/+1 and Taunt", rarity="Rare", battlecry=defender_of_argus_battlecry),
        MinionCard("Shattered Sun Cleric", 3, 3, 2, "Battlecry: Give a friendly +1/+1", battlecry=shattered_sun_cleric_battlecry),
        MinionCard("Abusive Sergeant", 1, 1, 1, "Battlecry: Give a minion +2 Attack", battlecry=abusive_sergeant_battlecry),
        MinionCard("Ironforge Rifleman", 3, 2, 2, "Battlecry: Deal 1 damage", battlecry=ironforge_rifleman_battlecry),
        MinionCard("Stormpike Commando", 5, 4, 2, "Battlecry: Deal 2 damage", battlecry=stormpike_commando_battlecry),
        MinionCard("Acidic Swamp Ooze", 2, 3, 2, "Battlecry: Destroy enemy weapon", battlecry=acidic_swamp_ooze_battlecry),
        MinionCard("Big Game Hunter", 5, 4, 2, "Battlecry: Destroy a minion with 7+ Attack", rarity="Epic", battlecry=big_game_hunter_battlecry),
        MinionCard("Loot Hoarder", 2, 2, 1, "Deathrattle: Draw a card", deathrattle=loot_hoarder_deathrattle),
        MinionCard("Harvest Golem", 3, 2, 3, "Deathrattle: Summon a 2/1 Golem", deathrattle=harvest_golem_deathrattle),
        MinionCard("Sludge Belcher", 5, 3, 5, "Taunt. Deathrattle: Summon 1/2 Slime", rarity="Rare", taunt=True, deathrattle=sludge_belcher_deathrattle),
        MinionCard("Argent Squire", 1, 1, 1, "Divine Shield", divine_shield=True),
        MinionCard("Scarlet Crusader", 3, 3, 1, "Divine Shield", divine_shield=True),
        MinionCard("Argent Commander", 6, 4, 2, "Charge, Divine Shield", rarity="Rare", charge=True, divine_shield=True),
        MinionCard("Sunwalker", 6, 4, 5, "Taunt, Divine Shield", rarity="Rare", taunt=True, divine_shield=True),
        MinionCard("Young Dragonhawk", 1, 1, 1, "Windfury", windfury=True),
        MinionCard("Raging Worgen", 3, 3, 3, "Windfury", windfury=True),
        MinionCard("Windfury Harpy", 6, 4, 5, "Windfury", windfury=True),
        MinionCard("Emperor Cobra", 3, 2, 3, "Poisonous", rarity="Rare", poisonous=True),
        MinionCard("Patient Assassin", 2, 1, 1, "Stealth, Poisonous", rarity="Epic", stealth=True, poisonous=True),
        MinionCard("Worgen Infiltrator", 1, 2, 1, "Stealth", stealth=True),
        MinionCard("Jungle Panther", 3, 4, 2, "Stealth", stealth=True),
        MinionCard("Stranglethorn Tiger", 5, 5, 5, "Stealth", rarity="Rare", stealth=True),
    ]


def get_legendary_minions():
    return [
        MinionCard("Cairne Bloodhoof", 6, 4, 5, "Deathrattle: Summon Baine", rarity="Legendary", deathrattle=cairne_bloodhoof_deathrattle),
        MinionCard("Sylvanas Windrunner", 6, 5, 5, "Deathrattle: Steal a random enemy", rarity="Legendary", deathrattle=sylvanas_deathrattle),
        MinionCard("Tirion Fordring", 8, 6, 6, "Divine Shield, Taunt. Deathrattle: Equip Ashbringer", rarity="Legendary", divine_shield=True, taunt=True, deathrattle=tirion_deathrattle),
        MinionCard("Ragnaros the Firelord", 8, 8, 8, "Can't attack. Deal 8 damage to random enemy at end of turn", rarity="Legendary"),
        MinionCard("Ysera", 9, 4, 12, "At end of turn, add a Dream Card", rarity="Legendary"),
        MinionCard("Alexstrasza", 9, 8, 8, "Battlecry: Set a hero's health to 15", rarity="Legendary"),
        MinionCard("Deathwing", 10, 12, 12, "Battlecry: Destroy all other minions and discard your hand", rarity="Legendary"),
        MinionCard("Leeroy Jenkins", 5, 6, 2, "Charge. Battlecry: Summon two 1/1 Whelps for opponent", rarity="Legendary", charge=True),
    ]


def get_spell_cards():
    return [
        SpellCard("The Coin", 0, coin_effect, "Gain 1 mana crystal this turn"),
        SpellCard("Arcane Intellect", 3, arcane_intellect_effect, "Draw 2 cards"),
        SpellCard("Fireball", 4, fireball_effect, "Deal 6 damage", requires_target=True),
        SpellCard("Frostbolt", 2, frostbolt_effect, "Deal 3 damage and Freeze", requires_target=True),
        SpellCard("Polymorph", 4, polymorph_effect, "Transform a minion into a 1/1 Sheep", rarity="Rare", requires_target=True, target_type="minion"),
        SpellCard("Flamestrike", 7, flamestrike_effect, "Deal 4 damage to all enemy minions"),
        SpellCard("Holy Nova", 5, holy_nova_effect, "Deal 2 to enemies, heal friendlies for 2"),
        SpellCard("Holy Light", 2, holy_light_effect, "Restore 8 health", requires_target=True),
        SpellCard("Consecration", 4, consecration_effect, "Deal 2 damage to all enemies"),
        SpellCard("Swipe", 4, swipe_effect, "Deal 4 to target, 1 to all other enemies", requires_target=True),
        SpellCard("Sprint", 7, sprint_effect, "Draw 4 cards", rarity="Rare"),
        SpellCard("Assassinate", 5, assassinate_effect, "Destroy an enemy minion", requires_target=True, target_type="enemy_minion"),
        SpellCard("Backstab", 0, backstab_effect, "Deal 2 damage to undamaged minion", requires_target=True, target_type="minion"),
        SpellCard("Execute", 2, execute_effect, "Destroy a damaged enemy minion", requires_target=True, target_type="enemy_minion"),
        SpellCard("Shield Block", 3, shield_block_effect, "Gain 5 Armor. Draw a card"),
        SpellCard("Blessing of Kings", 4, blessing_of_kings_effect, "Give a minion +4/+4", requires_target=True, target_type="minion"),
        SpellCard("Power Word: Shield", 1, power_word_shield_effect, "Give a minion +2 Health. Draw a card", requires_target=True, target_type="minion"),
        SpellCard("Shadow Word: Pain", 2, shadow_word_pain_effect, "Destroy a minion with 3 or less Attack", requires_target=True, target_type="minion"),
        SpellCard("Shadow Word: Death", 3, shadow_word_death_effect, "Destroy a minion with 5 or more Attack", rarity="Rare", requires_target=True, target_type="minion"),
        SpellCard("Mind Control", 10, mind_control_effect, "Take control of an enemy minion", rarity="Epic", requires_target=True, target_type="enemy_minion"),
        SpellCard("Silence", 0, silence_effect, "Silence a minion", requires_target=True, target_type="minion"),
    ]


def get_weapon_cards():
    return [
        WeaponCard("Fiery War Axe", 3, 3, 2, "A warrior's best friend"),
        WeaponCard("Arcanite Reaper", 5, 5, 2, "Big axe", rarity="Rare"),
        WeaponCard("Truesilver Champion", 4, 4, 2, "Heal 2 when attacking", rarity="Rare"),
        WeaponCard("Assassin's Blade", 5, 3, 4, "Sneaky stabby"),
        WeaponCard("Eaglehorn Bow", 3, 3, 2, "Hunter weapon"),
    ]


def create_starter_deck(hero_class: str = "neutral"):
    """Create a balanced starter deck with 30 cards"""
    basic = get_basic_minions()
    special = get_special_minions()
    spells = get_spell_cards()[1:]  # Exclude The Coin
    
    deck = []
    
    # Add 2 copies of basic minions (12 cards)
    for card in basic[:6]:
        deck.append(card.copy())
        deck.append(card.copy())
    
    # Add 2 copies of special minions (8 cards)
    for card in special[:4]:
        deck.append(card.copy())
        deck.append(card.copy())
    
    # Add 2 copies of spells (10 cards)
    for card in spells[:5]:
        deck.append(card.copy())
        deck.append(card.copy())
    
    random.shuffle(deck)
    return deck[:30]


def create_random_deck():
    """Create a random deck with 30 cards"""
    all_cards = get_basic_minions() + get_special_minions() + get_spell_cards()[1:] + get_weapon_cards()
    
    deck = []
    for _ in range(30):
        card = random.choice(all_cards)
        deck.append(card.copy())
    
    random.shuffle(deck)
    return deck


def create_aggro_deck():
    """Create an aggressive deck focused on early game"""
    low_cost = [c for c in get_basic_minions() + get_special_minions() if c.mana_cost <= 3]
    charge_minions = [c for c in get_basic_minions() + get_special_minions() if hasattr(c, 'charge') and c.charge]
    
    deck = []
    for card in charge_minions:
        deck.append(card.copy())
        deck.append(card.copy())
    
    while len(deck) < 30:
        card = random.choice(low_cost)
        deck.append(card.copy())
    
    random.shuffle(deck)
    return deck[:30]


def create_control_deck():
    """Create a control deck with late game power"""
    high_cost = [c for c in get_basic_minions() + get_special_minions() if c.mana_cost >= 4]
    taunt_minions = [c for c in get_basic_minions() + get_special_minions() if hasattr(c, 'taunt') and c.taunt]
    removal_spells = [get_spell_cards()[i] for i in [3, 11, 13, 17, 18, 19] if i < len(get_spell_cards())]
    
    deck = []
    for card in taunt_minions[:4]:
        deck.append(card.copy())
        deck.append(card.copy())
    
    for card in removal_spells[:3]:
        deck.append(card.copy())
        deck.append(card.copy())
    
    while len(deck) < 30:
        card = random.choice(high_cost)
        deck.append(card.copy())
    
    random.shuffle(deck)
    return deck[:30]
