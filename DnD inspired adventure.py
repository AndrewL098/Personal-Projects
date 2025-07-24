# Random fantasy adventure
import random 
import time

#                           method, hp, atck, def, speed, luck   50
party_options = {"Swordmaster": ["aura", 15, 10, 10, 10,  5],
                 "Mage":   ["magic", 9, 16, 10,  8,  7],
                 "Monk" :        ["ki",   15, 12, 7,  13,  3],
                 "Priest":       ["holy", 15, 8,  8,   8,  11],
                 "Tank":         ["aura", 25, 0,  25,  0,  0],
                 "Assassin":     ["aura", 5, 15, 0, 15, 15 ]}

beginner_items = {"enchanting stone":["+10 attack stat", 30],
                  "armor plate": ["+10 def stat", 30],
                  "apple":["+10 hp stat",30]}

epic_Swordmaster_items = {"Equipment Enchantment": ["Swordmaster", "x1.5 all stats",35],
                           "Dagger Talisman": ["Swordmaster", "+15 luck",25],
                           "Inspiration": ["Swordmaster", "Everyone in the party can attack twice during a turn",70]}

epic_Mage_items = {"Daedalus Golem Staff": ["Mage", "x3 attack stat",40],
                         "Ring Of Wisdom": ["Mage","Reduces effectiveness of resistances",50],
                         "Wide Guard":["Mage","Party's total defense stat is doubled",60]}

epic_Monk_items = {"Bracers Of Defense": ["Monk","x2 def and x1.5 hp stats",40],
                   "Book Of Enlightenment": ["Monk","x1.5 luck and x2 attack stats",40],
                   "Full Counter": ["Monk","Completely negates the first attack",55]}

epic_Tank_items = {"Tower Shield":["Tank", "x2 def stat",30],
                   "Draconic Armor": ["Tank","x2 hp and x1.5 def stats",40],
                   "Taunt":["Tank","x4 def stat, but the monster will only attack the Tank",60]}

epic_Priest_items = {"Four Leaf Clover Staff": ["Priest","x3 luck stat",30],
                     "Holy Robe": ["Priest","x3 hp stat",40],
                     "Holy Domain": ["Priest","Party regains 10% hp each turn",60]}

epic_Assassin_items = {"Shadow Daggers": ["Assassin","x2 attack and x1.5 luck stat",40],
                       "Windrider's Boots": ["Assassin","x2 speed stat",20],
                       "Shadow Sneak":["Assassin","guarantees the party will crit on the first hit",70] }

ALL_EPIC_ITEMS = epic_Swordmaster_items | epic_Mage_items | epic_Monk_items | epic_Tank_items | epic_Priest_items | epic_Assassin_items

Legendary_items = {"Dragon Slayer": ["Sword that once cut down a dragon",100],  # x3.5 all stats x.5 anti aura resist
                   "Dragon Archmage": ["Magic that rivals the draconic tongue", 100], #x5 attack   x.8 anti magic resist
                   "Buddha":["True Enlightment",100], # x1.5 luck x3 attack
                   "Pope":["Capable of Divine Miracles",100], # + 50hp +50% regen
                   "Svalinn":["A shield capable of shielding the user from the sun", 100],  # 3x hp 3x def
                   "Void": ["Become one with the shadows",100]} #33% evasion 2x attack

def party_select():
    #choosing your party
    print("You may only have 3 members in your party.")
    print(f"Here is a list of potential party members: \n {list(party_options)}")
    global party
    party = []
    party_stats = {}
    while len(party_stats) < 3:  
        choice = input("Which member would you like to add to your party: ").strip().title()
        if choice not in list(party_options):
            print("Please input a valid party member")
        elif choice in list(party_stats):
            print("No repeat party members")
        else: 
            party.append(choice)
            party_stats[choice] = party_options[choice]
    # Regen stat will be set to one here, changeable
    party_stats["Regen"] = 0
    print(f"Party stats (attack method,hp,atk,def,spe,luck): {party_stats}")
    return party_stats
    # party is only a list of all the names of the party members 
    # party_stats is all of the info, names, stats of individuals, any anti resist, and any other special abilities


#displays a shop and will return updated stats of the party members 
def shop(money, round, party_stats):  # will return new party stats and bank account
    
    shopping = True
    if round == 1:    # beginner items 

        while shopping:
            print("=" * 110)
            print("                  Beginner Items                  ")
            for i in beginner_items:
                display = i + "(" + beginner_items[i][0] + ")"
                display = display.center(40)
                print(f"{display} : {beginner_items[i][1]} gold")
            print("=" * 110)


            print(f"You have {money} gold")
            item_choice = input("Which item would you like to buy (q to quit): ").strip().lower()
            if item_choice == "q":
                shopping = False
                return party_stats, money
            elif item_choice not in ["enchanting stone", "armor plate", "apple"]:
                print("Please input a valid item.")

            elif item_choice == "enchanting stone" and money >= 30: # +10 attack, 30 gold
                money -= 30
                while True:
                    try:   
                        member = int(input(f"Who would you like to equip the {item_choice}? Party Member (1, 2, or 3): "))
                        break
                    except: print("Please input 1, 2, or 3")
                member = party[(member - 1)] # changes party member 1 into the name of party member 1
                party_stats[member][2] = party_stats[member][2] + 10

            elif item_choice == "armor plate" and money >= 15: # +10 def, 30 gold
                money -= 30
                while True:
                    try:   
                        member = int(input(f"Who would you like to equip the {item_choice}? Party Member (1, 2, or 3): "))
                        break
                    except: print("Please input 1, 2, or 3")
                member = party[(member - 1)] # changes party member 1 into the name of party member 1
                party_stats[member][3] = party_stats[member][3] + 10
            
            elif item_choice == "apple" and money >= 15: # +10 hp, 30 gold
                money -= 30
                while True:
                    try:   
                        member = int(input(f"Who would you like to equip the {item_choice}? Party Member (1, 2, or 3): "))
                        break
                    except: print("Please input 1, 2, or 3")
                member = party[(member - 1)] # changes party member 1 into the name of party member 1
                party_stats[member][1] = party_stats[member][1] + 10
            else: print("You are too poor")

    elif round == 2:  # epic items
        pool_o_items = {} # we are going to pool the possible items, so we can do random.choice on it
        for i in party:   # # updates the pool of items to be epic items from pool
            if i == "Swordmaster":
                pool_o_items = pool_o_items | epic_Swordmaster_items
            elif i == "Mage":
                pool_o_items = pool_o_items | epic_Mage_items
            elif i == "Monk":
                pool_o_items = pool_o_items | epic_Monk_items
            elif i == "Priest":
                pool_o_items = pool_o_items | epic_Priest_items
            elif i == "Tank":
                pool_o_items = pool_o_items | epic_Tank_items
            elif i == "Assassin":
                pool_o_items = pool_o_items | epic_Assassin_items

        while shopping:
            random_epic_items = random.choices(list(pool_o_items), k = 3) # list of the names of the items
            random_epic_items_des = {} # description of the randomized epic items and gold value
            while True: # shopping for each set of (3) items, will break loop to get 3 new items

                for i in random_epic_items:
                    random_epic_items_des[i] = ALL_EPIC_ITEMS[i]
                    
                print("="*110)#============================================================================
                display = "EPIC ITEMS"
                print(display.center(110))
                for i in random_epic_items_des:
                    display = f"{i} ({random_epic_items_des[i][0]}) ({random_epic_items_des[i][1]})"
                    display = display.center(100)
                    print(f"{display} : {random_epic_items_des[i][2]} gold")
                print("="*110)#=============================================================================

                # Stats updates
                print(f"You have {money} gold")
                item_choice = input("Which item would you like to buy (q to quit or r to reroll): ").strip().title()
                if item_choice == "Q":
                    return party_stats, money
                if random_epic_items == []:
                    return party_stats, money
                elif item_choice == "R" and money >= 10:
                    money -= 10
                    break # by breaking this loop, it will get 3 new? items  
                elif item_choice == "R" and money < 10:
                    print("You are can not afford to reroll")
                elif (item_choice not in list(random_epic_items_des)):
                    print("Please input a valid item")

                # Time for 18 elif statements to determine stat changes from each item CRYYYYYYYY
                elif item_choice == "Equipment Enchantment" and money >= epic_Swordmaster_items["Equipment Enchantment"][2]: # 1.5x all stats -35g
                    money -= epic_Swordmaster_items["Equipment Enchantment"][2]
                    for i in range(1,6):
                        party_stats["Swordmaster"][i] = party_stats["Swordmaster"][i] * 1.5
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)
                
                elif item_choice == "Dagger Talisman" and money >= epic_Swordmaster_items["Dagger Talisman"][2]: # +15 luck -25g
                    money -= epic_Swordmaster_items["Dagger Talisman"][2]
                    party_stats["Swordmaster"][5] += 15
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)

                elif item_choice == "Inspiration" and money >= epic_Swordmaster_items["Inspiration"][2]: # +15 luck -25g
                    money -= epic_Swordmaster_items["Inspiration"][2]
                    party_stats["Inspiration"] = True
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)
                
                elif item_choice == "Daedalus Golem Staff" and money >= epic_Mage_items["Daedalus Golem Staff"][2]: #  3x attack -40g
                    money -= epic_Mage_items["Daedalus Golem Staff"][2]
                    party_stats["Mage"][2] = party_stats["Mage"][2] * 3
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)

                elif item_choice == "Ring Of Wisdom" and money >= epic_Mage_items["Ring Of Wisdom"][2]: #  resistances are less effective	-50
                    money -= epic_Mage_items["Ring Of Wisdom"][2]
                    party_stats["Anti Magic Resist"] = 0.5 #Magic Resistances are half as effective 
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)

                elif item_choice == "Wide Guard" and money >= epic_Mage_items["Wide Guard"][2]: #  party def total gets doubled
                    money -= epic_Mage_items["Ring Of Wisdom"][2]
                    party_stats["Wide Guard"] = True
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)
                
                elif item_choice == "Bracers Of Defense" and money >= epic_Monk_items["Bracers Of Defense"][2]: #  x2 def x1.5 hp 40g
                    money -= epic_Monk_items["Bracers Of Defense"][2]
                    party_stats["Monk"][3]  = party_stats["Monk"][3] * 2
                    party_stats["Monk"][3]  = party_stats["Monk"][1] * 1.5
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)

                elif item_choice == "Book Of Enlightenment" and money >= epic_Monk_items["Book Of Enlightenment"][2]: #  1.5x luck 2x attack 40g
                    money -= epic_Monk_items["Book Of Enlightenment"][2]
                    party_stats["Monk"][3]  = party_stats["Monk"][3] * 1.5
                    party_stats["Monk"][3]  = party_stats["Monk"][2] * 2
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)

                elif item_choice == "Full Counter" and money >= epic_Monk_items["Full Counter"][2]: #  completely negates monster’s first attack 70g
                    money -= epic_Monk_items["Full Counter"][2]
                    party_stats["Full Counter"] = True 
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)

                elif item_choice == "Tower Shield" and money >= epic_Tank_items["Tower Shield"][2]: #  2x def -30g
                    money -= epic_Tank_items["Tower Shield"][2]
                    party_stats["Tank"][3] = party_stats["Tank"][3] * 2
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)

                elif item_choice == "Draconic Armor" and money >= epic_Tank_items["Draconic Armor"][2]: #  2x hp 1.5x def -40g
                    money -= epic_Tank_items["Draconic Armor"][2]
                    party_stats["Tank"][3] = party_stats["Tank"][3] * 1.5
                    party_stats["Tank"][1] = party_stats["Tank"][3] * 2
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)

                elif item_choice == "Taunt" and money >= epic_Tank_items["Taunt"][2]: #  tuant ability - 60g
                    money -= epic_Tank_items["Taunt"][2]
                    party_stats["Taunt"] = True
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)

                elif item_choice == "Four Leaf Clover Staff" and money >= epic_Priest_items["Four Leaf Clover Staff"][2]: #  3x luck 30g
                    money -= epic_Priest_items["Four Leaf Clover Staff"][2]
                    party_stats["Priest"][5] = party_stats["Priest"][5] * 3
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)

                elif item_choice == "Holy Robe" and money >= epic_Priest_items["Holy Robe"][2]: #  3x hp 40
                    money -= epic_Priest_items["Holy Robe"][2]
                    party_stats["Priest"][1] = party_stats["Priest"][1] * 3
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)
                
                elif item_choice == "Holy Domain" and money >= epic_Priest_items["Holy Domain"][2]: #  Party regains 10% of hp each turn  60g
                    money -= epic_Priest_items["Holy Domain"][2]
                    party_stats["Regen"] = party_stats["Regen"] + 0.1
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)
                
                elif item_choice == "Shadow Daggers" and money >= epic_Assassin_items["Shadow Daggers"][2]: #2x attack x1.5 luck 40g
                    money -= epic_Assassin_items["Shadow Daggers"][2]
                    party_stats["Assassin"][2] = party_stats["Assassin"][2] * 2
                    party_stats["Assassin"][5] = party_stats["Assassin"][5] * 1.5
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)

                elif item_choice == "Windrider's Boots" and money >= epic_Assassin_items["Windrider's Boots"][2]: #3x speed 20g
                    money -= epic_Assassin_items["Windrider's Boots"][2]
                    party_stats["Assassin"][4] = party_stats["Assassin"][4] * 3
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)

                elif item_choice == "Shadow Sneak" and money >= epic_Assassin_items["Shadow Sneak"][2]: # guarantee party crit on first hit 70
                    money -= epic_Assassin_items["Shadow Sneak"][2]
                    party_stats["Shadow Sneak"] = True
                    del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
                    del random_epic_items_des[item_choice]
                    random_epic_items.remove(item_choice)
                
                else: 
                    print("You are too poor")

    elif round == 3: # legendary items
        pool_o_items = {} # we are going to pool the possible items, so we can do random.choice on it
        for i in party:   # # updates the pool of items to be epic items from pool
            if i == "Swordmaster":
                pool_o_items["Dragon Slayer"] = ["Sword that once cut down a dragon",100]
            elif i == "Mage":
                pool_o_items["Dragon Archmage"] = ["Magic that rivals the draconic tongue", 100]
            elif i == "Monk":
                pool_o_items["Buddha"] = ["True Enlightment",100]
            elif i == "Priest":
                pool_o_items["Pope"] = ["Capable of Divine Miracles",100]
            elif i == "Tank":
                pool_o_items["Svalinn"]= ["A shield capable of shielding the user from the sun", 100]
            elif i == "Assassin":
                pool_o_items["Void"]= ["Become one with the shadows",100]

        while True: 
                    
            print("="*110)#============================================================================
            display = "LEGENDARY ITEMS/CLASS UPGRADES"
            print(display.center(110))
            for i in pool_o_items:
                display = f"{i} ({pool_o_items[i][0]})"
                display = display.center(100)
                print(f"{display} : {pool_o_items[i][1]} gold")
            print("="*110)#=============================================================================

            print(f"You have {money} gold")
            item_choice = input("Which item would you like to buy (q to quit): ").strip().title()

            if item_choice == "Q":
                return party_stats, money

            elif item_choice not in list(pool_o_items):
                print("Please input a valid option")

            elif item_choice == "Dragon Slayer" and money >= pool_o_items["Dragon Slayer"][1]: #x 3.5 all stats x.5 anti aura resist
                money -= pool_o_items["Dragon Slayer"][1]
                for i in range(1,6):
                        party_stats["Swordmaster"][i] = party_stats["Swordmaster"][i] * 3.5

                party_stats["Anti Aura Resist"] = 0.5
                del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
            
            elif item_choice == "Dragon Archmage" and money >= pool_o_items["Dragon Archmage"][1]: # x5 attack x.8 anti magic resist
                money -= pool_o_items["Dragon Archmage"][1]
                party_stats["Mage"][2] = party_stats["Mage"][2] * 5
                if "Anti Magic Resist" not in party_stats:
                    party_stats["Anti Magic Resist"] = 0.75
                else:
                    party_stats["Anti Magic Resist"] = party_stats["Anti Magic Resist"] * 0.8 
                del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
            
            elif item_choice == "Buddha" and money >= pool_o_items["Buddha"][1]: # x3 attack x1.5 luck
                money -= pool_o_items["Buddha"][1]
                party_stats["Monk"][5] = party_stats["Monk"][5] * 1.5
                party_stats["Monk"][2] = party_stats["Monk"][2] * 3
                del pool_o_items[item_choice] # gets rid of the item so they can't buy it again

            elif item_choice == "Pope" and money>= pool_o_items["Pope"][1]: # x4 hp 50% regen
                money -= pool_o_items["Pope"][1]
                party_stats["Priest"][1] = party_stats["Priest"][1] * 4
                party_stats["Regen"] += 0.5
                del pool_o_items[item_choice] # gets rid of the item so they can't buy it again

            elif item_choice == "Svalinn" and money >= pool_o_items["Svalinn"][1]: #x3 hp x3 def
                money -= pool_o_items["Svalinn"][1]
                party_stats["Tank"][3] = party_stats["Tank"][3] * 3
                party_stats["Tank"][1] = party_stats["Tank"][1] * 3
                del pool_o_items[item_choice] # gets rid of the item so they can't buy it again
            
            elif item_choice == "Void" and money >= pool_o_items["Void"][1]:
                money -= pool_o_items["Void"][1]
                party_stats["Void"] = True
                del pool_o_items[item_choice] # gets rid of the item so they can't buy it again

            else:
                print("You are too poor")

#random blessings or curses
blessings_curses = {"Blessing of Reincarnation": " +1 retry attempt",
                    "Blessing of Wealth": "gain gold",
                    "Blessing of Life": "2% life regen per turn (stackable)",
                    "Curse of Binding": "Unable to buy more items from the shop for the round",
                    "Curse of Poverty": "lose gold",
                    "Draconic Curse": "+10% stats for all monsters"}

def holy_roulette(holypower,party_stats, money): #return party stats and holypower and money
    print("=" * 110)
    print("Welcome to roulette table for Deities!")
    print("Spend your holy power to either grant a blessing or grant a curse onto your party")
    print("Each spin will take 25 holypower")
    print("Tip: The party's luck stat can influence the results")
    print("=" * 110)

    luck = party_stats[party[0]][5] + party_stats[party[1]][5] + party_stats[party[2]][5]
    shop_bind = False # set curse of binding to be false
    gamble_choice = "Y"
    

    while True:

        while True:
            gamble_choice = input("Would you like to spin? (Y/N): ").upper().strip()
            if gamble_choice in ["Y","N"]:
                break
                
            else:
                print("Please input Y or N")
        
        if gamble_choice == 'N':
            break

        if (gamble_choice == 'Y') and (holypower <= 0 ):
            print("You do not have enough holy power")
            break

        holypower -= 25
        print(f"You now have {holypower} holy power")
        if luck < 50:
            gamble_outcome = random.choice(["Blessing of Reincarnation", "Blessing of Wealth","Blessing of Life", "Curse of Binding", "Curse of Poverty","Draconic Curse"])
            print("...")
            print(f"You have granted the {gamble_outcome} ({blessings_curses[gamble_outcome]})")

        else:
            gamble_outcome = random.choice(["Blessing of Reincarnation", "Blessing of Wealth","Blessing of Life"])
            print("...")
            print(f"You have granted the {gamble_outcome} ({blessings_curses[gamble_outcome]})")
        
        if gamble_outcome == "Blessing of Reincarnation":
            global retry
            retry += 1

        elif gamble_outcome == "Blessing of Wealth":
            temp_money = random.randint(50,75)
            print(f"You ganined {temp_money} gold")
            money += temp_money

        elif gamble_outcome == "Blessing of Life":
            party_stats["Regen"] += 0.02

        elif gamble_outcome  == "Curse of Binding":
            shop_bind = True

        elif gamble_outcome == "Curse of Poverty":
            temp_money = random.randint(50,75)
            print(f"You lost {temp_money} gold")

            money -= temp_money
        
        elif gamble_outcome == "Draconic Curse":
            global monster_multi
            monster_multi += 0.1

        print("=" * 110)
        
    return party_stats,holypower, money, shop_bind


#Calculates the total stats of the party, accounting for resistances of monsters, anti resistance, and special abilities 
# Monster stat's order -> [hp, attack, def, speed, luck, magic resist, aura resist]
#                           0,      1,   2,     3,    4,            5,           6,
# Total party stat order  [hp, attack, def, speed, luck]
def total_party_stat(party_stats, monster_stat,crit):
    total_party_stat = [] #final list of the party's total stat
    
    for i in range(1,6):
        if i == 2: # attack stat calculations
            tot_attack = 0 # represents the total attack stat
            for i in range(3): # iterates through each member
                if party[i] == "Mage":
                    if ("Anti Magic Resist" in party_stats) and crit == False: # then we have to apply resistance reduction
                        tot_attack = tot_attack + party_stats["Mage"][2] / (monster_stat[5] * party_stats["Anti Magic Resist"])

                    elif ("Anti Magic Resist"  not in party_stats) and crit == False:
                        tot_attack = tot_attack + party_stats["Mage"][2] / monster_stat[5]

                    elif crit == True:
                        tot_attack = tot_attack + (party_stats["Mage"][2]) * 2

                elif (party[i] == "Swordmaster") or (party[i] == "Assassin"):
                    if ("Anti Aura Resist" in party_stats) and crit == False: # then we have to apply resistance reduction
                        tot_attack = tot_attack + party_stats[party[i]][2] / (monster_stat[5] * party_stats["Anti Aura Resist"])

                    elif ("Anti Aura Resist"  not in party_stats) and crit == False:
                        tot_attack = tot_attack + party_stats[party[i]][2] / monster_stat[5]

                    elif crit == True:
                        tot_attack = tot_attack + (party_stats[party[i]][2]) * 2

                else:
                    if crit == False:
                        tot_attack += party_stats[party[i]][2]
                    elif crit == True:
                        tot_attack += (party_stats[party[i]])[2] * 2
            
            tot_attack = round(tot_attack,2)
            total_party_stat.append(tot_attack)

        elif (i == 3) and ("Tank" in party) and ("Taunt" in party_stats): 
            total_party_stat.append(round(party_stats["Tank"][3] * 4,2))

        else:
            temp_tot = 0 # temporary total of one stat
            temp_tot = party_stats[party[0]][i] + party_stats[party[1]][i] + party_stats[party[2]][i]
            temp_tot = round(temp_tot,2)
            total_party_stat.append(temp_tot)

    if "Wide Guard" in party_stats:
        total_party_stat[2] = round(total_party_stat[2] * 2,2)
    
    return total_party_stat

#battle sequence
# Monster stat's order -> [hp, attack, def, speed, luck, magic resist, aura resist]
#                           0,      1,   2,     3,    4,            5,           6,
# Total party stat order  [hp, attack, def, speed, luck]
def battle_golem(party_stats,money,holypower):
    monster_stat = [75,15 , 13, 1, 1, 1.25, 1.25 ]
    print("Your party encountered an elemental golem!")

    for i in range(len(monster_stat)): # applies the monster stat multiplier
        monster_stat[i] = monster_stat[i] * monster_multi
    crit = False #sets inital value for crits
    temp_party_stats = total_party_stat(party_stats,monster_stat,crit) #transfers temp values so actual party_stats are changed
     
    temp_hp = temp_party_stats[0] # temp hp for party

    death = False
    turn = 0 

    battling = True
    while battling:

        turn += 1
        def party_attack():
            # roll to see if you crit
            roll = random.randint(1,100) # 3% crit chance, each point in luck stat increases your roll
            roll += (temp_party_stats[4]/2)
            if roll >= 97:
                crit = True
            else:
                crit = False
            
            if "Shadow Sneak" in party_stats:
                crit = True

            tempattack = total_party_stat(party_stats,monster_stat, crit)[1] # temp attack stat for the party
             

            tempdmg = (tempattack - monster_stat[2] ) + random.randint(-5,5)
            if tempdmg < 0:
                tempdmg = 0 # to prevent healing the monster if the party does too little dmg
            monster_stat[0] -= tempdmg # monster will take the first hit
            if crit:
                print("The party landed a crit!!!")
            print(f"Elemental Golem hp: {monster_stat[0]:.1f}")
            
            if monster_stat[0] <= 0:
                
                print("The party has slained the Elemental Golem")
                nonlocal money
                nonlocal holypower

                money += 100
                holypower += 100
                return money, holypower, death 
            else: return money, holypower, death


        def golem_attack(turn):
            # Then monster attacks
            nonlocal temp_hp
            nonlocal death
            chance = random.random()
            if chance <= 0.33 and ("Void" in party_stats): # evasion
                print("Your party evaded an attack")
            if turn == 1 and ("Full Counter" in party_stats): # full counter, first turn, you don't take damage
                return money, holypower, death 
            else: # damage calcs
                tempdmg = monster_stat[1] - (temp_party_stats[2])/3 + random.randint(-5,10)
                if tempdmg < 0:
                    tempdmg = 0 # to prevent the monster from healing the party because they did too little dmg
                temp_hp -= tempdmg

                if (temp_hp + temp_party_stats[0] * party_stats["Regen"]) > temp_party_stats[0]:
                    temp_hp = temp_party_stats[0]
                else: temp_hp += temp_party_stats[0] * party_stats["Regen"]

                print(f"Party's total hp: {temp_hp:.1f}")

                if temp_hp <= 0: # check if party died
                    print("The party has perished")
                    death = True
                    return 0,0,death
            return money, holypower, death 
                
        if monster_stat[3] <= temp_party_stats[3]: # party moves first 

            money, holypower, death = party_attack()
            if "Inspiration" in party_stats: # Inspiration lets party attack twice
                money, holypower, death = party_attack
            if monster_stat[0] <= 0: # check if monster is dead
                return money, holypower, death
            if turn < 50:
                time.sleep(0.2)

            money, holypower, death = golem_attack(turn)
            if temp_hp <= 0: # check if party is dead
                return money, holypower, death
            if turn < 50:
                time.sleep(0.2)


        else: # party goes second
            money, holypower, death = golem_attack(turn)
            if temp_hp <= 0: # check if party is dead
                return money, holypower, death
            if turn < 50:
                time.sleep(0.2)


            money, holypower, death = party_attack()
            if "Inspiration" in party_stats: # Inspiration lets party attack twice
                money, holypower, death = party_attack
            if monster_stat[0] <= 0: # check if monster is dead
                return money, holypower, death
            if turn < 50:
                time.sleep(0.2)




def battle_wyvern(party_stats,money,holypower):
    monster_stat = [150 , 50 , 75, 45, 0, 2, 2]
    print("Your party encountered a undead wyvern!")

    for i in range(len(monster_stat)): # applies the monster stat multiplier
        monster_stat[i] = monster_stat[i] * monster_multi
    crit = False #sets inital value for crits
    temp_party_stats = total_party_stat(party_stats,monster_stat,crit) #transfers temp values so actual party_stats are changed
     
    temp_hp = temp_party_stats[0] # temp hp for party

    death = False
    turn = 0 

    battling = True
    while battling:

        turn += 1
        def party_attack(turn):
            # roll to see if you crit
            roll = random.randint(1,100) # 3% crit chance, each point in luck stat increases your roll
            roll += (temp_party_stats[4]/2)
            if roll >= 97:
                crit = True
            else:
                crit = False
            if "Shadow Sneak" in party_stats:
                crit = True

            tempattack = total_party_stat(party_stats,monster_stat, crit)[1] # temp attack stat for the party
             
            if crit:
                tempdmg = tempattack
            else:
                tempdmg = (tempattack - monster_stat[2] ) + random.randint(-5,5)
                if tempdmg < 0:
                    tempdmg = 0 # to prevent healing the monster if the party does too little dmg
            monster_stat[0] -= tempdmg  # monster will take the first hit

            if (crit == False): #Crit or priest will prevent healing

                if (monster_stat[0] + (turn * 0.01) * 100 * monster_multi) > 100:
                    monster_stat[0] = 100        
                    print("The Undead Wyvern healed full hp")                           # Undead Wyvern gets incremental healing, gotta kill it fast
                else:
                    monster_stat[0] += (turn * 0.05) * 100 * monster_multi
                    print(f"The Undead Wyvern healed {((turn * 0.05) * 100 * monster_multi):.2f}")

            if crit:
                print("The party landed a crit!!!")
            print(f"Undead Wyvern hp: {monster_stat[0]:.1f}")
            
            if monster_stat[0] <= 0:
                
                print("The party has slained the Undead Wyvern")
                nonlocal money
                nonlocal holypower

                money += 100
                holypower += 100
                return money, holypower, death 
            else: return money, holypower, death


        def wyvern_attack(turn):
            # Then monster attacks
            nonlocal temp_hp
            nonlocal death
            chance = random.random()
            if chance <= 0.33 and ("Void" in party_stats):
                print("Your party evaded an attack")
            if turn == 1 and ("Full Counter" in party_stats): # full counter, first turn, you don't take damage
                return money, holypower, death 
            else:
                if (chance*turn) >= 0.9:
                    tempdmg = monster_stat[1]
                    print("The Undead Wyvern landed a crit!!!")
                else: 
                    tempdmg = monster_stat[1] - (temp_party_stats[2])/5 + random.randint(-5,10)

                if tempdmg < 0:
                    tempdmg = 0 # to prevent healing the party if the monster does too little dmg
                temp_hp -= tempdmg 
                
                if (chance*turn) < 0.9: # if monster crits, it prevents heaing
                    if (temp_hp + temp_party_stats[0] * party_stats["Regen"]) > 0:# regen
                        temp_hp = temp_party_stats[0]                             # makes sure you don't regenerate more than your total hp stat
                        print("The Party regenerated back to full hp")                        
                    else: 
                        temp_hp += temp_party_stats[0] * party_stats["Regen"] # regen
                        print(f"Party regenerated {temp_party_stats[0] * party_stats["Regen"]} hp")

                print(f"Party's total hp: {temp_hp:.1f}")
                if temp_hp <= 0:
                    print("The party has perished")
                    death = True
                    return 0,0,death
            return money, holypower, death
                
        if monster_stat[3] <= temp_party_stats[3]: # party moves first 
            money, holypower, death = party_attack(turn)
            if "Inspiration" in party_stats: # Inspiration lets party attack twice
                money, holypower, death = party_attack
            if monster_stat[0] <= 0: # check if monster is dead
                return money, holypower, death
            if turn < 50:
                time.sleep(0.2)

            money, holypower, death = wyvern_attack(turn)
            if temp_hp <= 0: # check if party is dead
                return money, holypower, death
            if turn < 50:
                time.sleep(0.2)


        else: # party goes second
            money, holypower, death = wyvern_attack(turn)
            if temp_hp <= 0: # check if party is dead
                return money, holypower, death
            money, holypower, death = party_attack(turn)
            if "Inspiration" in party_stats: # Inspiration lets party attack twice
                money, holypower, death = party_attack
            if monster_stat[0] <= 0: # check if monster is dead
                return money, holypower, death

def battle_dragon(party_stats,money, holypower):
    monster_stat = [1500 , 750 , 1000, 45, 0, 10, 10 ]
    print("Your party entered the Dragon's den")

    for i in range(len(monster_stat)): # applies the monster stat multiplier
        monster_stat[i] = monster_stat[i] * monster_multi
    crit = False #sets inital value for crits
    temp_party_stats = total_party_stat(party_stats,monster_stat,crit) #transfers temp values so actual party_stats are changed
    temp_hp = temp_party_stats[0] # temp hp for party

    death = False
    turn = 0 

    battling = True
    while battling:

        turn += 1
        def party_attack(turn):
            # roll to see if you crit
            roll = random.randint(1,100) # 3% crit chance, each point in luck stat increases your roll
            roll += (temp_party_stats[4]/2)
            if roll >= 97:
                crit = True
            else:
                crit = False
            if "Shadow Sneak" in party_stats:
                crit = True

            tempattack = total_party_stat(party_stats,monster_stat, crit)[1] # temp attack stat for the party
             
            if crit:
                tempdmg = tempattack
            else:
                tempdmg = (tempattack - monster_stat[2] ) + random.randint(-5,5)
                if tempdmg < 0:
                    tempdmg = 0 # to prevent healing the monster if the party does too little dmg
            monster_stat[0] -= tempdmg  # monster will take the first hit
            
            if crit:
                print("The party landed a crit!!!")
            print(f"Dragon hp: {monster_stat[0]:.1f}")
            
            if monster_stat[0] <= 0:
                
                print("The party has slained the Dragon")
                nonlocal money
                nonlocal holypower

                money += 100
                holypower += 100
                return money, holypower, death 
            else: return money, holypower, death


        def dragon_attack(turn):
            # Then monster attacks
            nonlocal temp_hp
            nonlocal death
            chance = random.random()
            if chance <= 0.33 and ("Void" in party_stats):
                print("Your party evaded an attack")
            if turn == 1 and ("Full Counter" in party_stats): # full counter, first turn, you don't take damage
                return money, holypower, death 
            else:
                chance = random.randint(1,100)
                if (turn*2) >= chance: # checks if dragon crits
                    tempdmg = monster_stat[1]
                    print("The Dragon landed a crit!!!")
                else:
                    tempdmg = monster_stat[1] - (temp_party_stats[2])/6 + random.randint(-5,10)
                if tempdmg < 0:
                    tempdmg = 0 # to prevent healing the party if the monster does too little dmg
                temp_hp -= tempdmg 

                if (turn*2) < chance: # if it doesn't crit, then the party cannot heal
                    if (temp_hp + temp_party_stats[0] * party_stats["Regen"]) > 0:
                        temp_hp = temp_party_stats[0]
                        print("Party regenerated back to full hp")         # makes sure you don't regenerate more than your total hp stat
                    else: 
                        temp_hp += temp_party_stats[0] * party_stats["Regen"] # regen
                        print(f"Party regenerated {temp_party_stats[0] * party_stats["Regen"]} hp")

                print(f"Party's total hp: {temp_hp:.1f}")
                if temp_hp <= 0:
                    print("The party has perished")
                    death = True
                    return 0,0,death
            return money, holypower, death
                
        if monster_stat[3] <= temp_party_stats[3]: # party moves first 
            money, holypower, death = party_attack(turn)
            if monster_stat[0] <= 0: # check if monster is dead
                return money, holypower, death
            if turn < 50:
                time.sleep(0.2)

            money, holypower, death = dragon_attack(turn)
            if temp_hp <= 0: # check if party is dead
                return money, holypower, death
            if turn < 50:
                time.sleep(0.2)


        else: # party goes second
            money, holypower, death = dragon_attack(turn)
            if temp_hp <= 0: # check if party is dead
                return money, holypower, death
            if turn < 50:
                time.sleep(0.2)

            money, holypower, death = party_attack(turn)
            if monster_stat[0] <= 0: # check if monster is dead
                return money, holypower, death
            if turn < 50:
                time.sleep(0.2)



def main():

    money = 100
    holypower = 100
    death = False

    print("=" * 110)
    print("You are a minor god")
    print("To gain faith, you must cultivate heroes with great achievements")
    print("With each achievement, you restore more holy power, allowing you to grant more blessings")
    print("")   
    
    def menu(money, party_stats, holypower, round):
        print("Once you vist the shop or the blessing alter, you may not revisit it")
        while True:
            user_choice = input("Would to like to go to the shop first or the blessing alter first: ").strip().lower()
            if user_choice == "shop": # they chose to shop first
                party_stats, money = shop(money, round, party_stats)
                print(f"Your party's total stats (hp,atk,def,speed, luck): {total_party_stat(party_stats,[200 , 55 , 0, 45, 10, 1, 1 ],False)}")
                party_stats, holypower, money, shop_bind = holy_roulette(holypower, party_stats, money)
                break
            elif user_choice == "blessing alter": # they chose to bless first
                party_stats, holypower, money, shop_bind = holy_roulette(holypower, party_stats, money)
                print(f"Your party's total stats (hp,atk,def,speed, luck): {total_party_stat(party_stats,[200 , 55 , 0, 45, 10, 1, 1 ],False)}")
                if shop_bind: # checks for curse of binding
                    print("Curse of Binding prevents you from visiting the shop")
                else:
                    party_stats, money = shop(money, round, party_stats)
                break
            else: 
                print("Please input shop or blessing alter")
        
        return money, party_stats, holypower


    party_stats = party_select()
    print("=" * 110)
    print(f"You party members: {party}") 
    round = 1
    money, party_stats, holypower = menu(money, party_stats, holypower, round)
    print(f"Your party's total stats (hp,atk,def,speed, luck): {total_party_stat(party_stats,[200 , 55 , 0, 45, 10, 1, 1 ],False)}")
    money, holypower, death = battle_golem(party_stats,money,holypower)

    global retry 
    if death and retry > 0: #checks if your party died and lets you retry if needed
        retry -= 1
        print("With the powers of reincarnation, you get another attempt!")
        print("Some stats of your current party have transferred to your new life")
        print(f"You have {retry} attempts left")
        return True, False
    
    if death: # GAME OVER
        return False, False
        
    round = 2
    money, party_stats, holypower = menu(money, party_stats, holypower, round)
    print(f"Your party's total stats (hp,atk,def,speed, luck): {total_party_stat(party_stats,[200 , 55 , 0, 45, 10, 1, 1 ],False)}")
    money, holypower, death = battle_wyvern(party_stats,money, holypower)
    if death and retry >0:
        retry -= 1
        print("With the powers of reincarnation, you get another attempt!")
        print("Some stats of your current party have transferred to your new life")
        print(f"You have {retry} attempts left")
        print("=" * 110)
        return True, False

    if death: # GAME OVER
        return False, False
    
    round = 3
    money, party_stats, holypower = menu(money, party_stats, holypower, round)
    print(party_stats)
    money, holypower, death = battle_dragon(party_stats,money, holypower)
    if death and retry >0:
        retry -= 1
        print("With the powers of reincarnation, you get another attempt!")
        print("Some stats of your current party have transferred to your new life")
        print(f"You have {retry} attempts left")
        print("=" * 110)
        global monster_multi
        monster_multi = 1
        return True, False

    if death: # GAME OVER
        return False, False
    else:
        return False, True




if __name__ == "__main__":
    retry = 0 #number of times you can retry 
    monster_multi = 1 # monster stat increase
    running = True
    while running:
        running, win = main()
    if win:
        print("CONGRATS YOUR PARTY HAS SLAYED THE DRAGON!!!")
        print("YOU HAVE GAINED A MAJOR ACHIEVEMENT!!!")
        print("YOU HAVE ASCENED TO A GREATER DEITY!!!")
