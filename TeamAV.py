import random
from random import choices
#Conditions:
#E0S1 Feixiao/E0 FTJ Robin/E0 DTF Aven/E0S1 Topaz
#190.08 spd and 200 toughness single enemy
#Will not proc FUAs in between enemy double attacks
#Robin basic if 0 sp, otherwise, basic if skill buff active, skill if not
#Aven always basic
#Topaz basic if less than 3, skill if >= 3
#Feixiao will only ult during Concerto
# noinspection SpellCheckingInspection

def teamfrat_av(char_speeds):
    #Character Variables_____________________________________________________________
    feixiao_av = 10000/char_speeds[0]
    robin_av = 10000/char_speeds[1]
    aven_av = 10000/char_speeds[2]
    topaz_av = 10000/char_speeds[3]
    numby_av = 10000/80 #Numby 80 spd
    boss_av = 10000/190.08 #Boss 190.08 spd

    feixiao_ult_stacks = 3 + 1 #3 initial, and +1 from technique
    feixiao_fua = True #turns False after an ally procs it out of turn
    feixiao_skill_buff = 0 #atk buff, self
    feixiao_talent_buff = 0 #dmg buff, self

    robin_energy = 160 * 0.5
    robin_aria = 0 #dmg buff from skill, team
    robin_concerto = False #atk buff from ult, aa, team

    aven_energy = 110 * 0.5
    aven_fua_proc = 3 #no. of times aven can out-of-turn gain blind_bet
    blind_bet = 0 #aven's fua stacks
    unnerved = 0 #cdmg buff from ult, team

    topaz_numby_energy = 130 * 0.5
    tame = 0 #cdmg buff from lc, team
    topaz_ult_stacks = 0

    numby_energy = 0 #for the sake of keeping list order, not necessary
    numby_aa_counter = 0 #restricts numby's amount of aa to two times (counts up) per turn
    numby_action = False

    boss_toughness = 200
    boss_attack = 0 #alternates between 0 and 1, two attacks
    ally_target = 0 #Assigns character that is being randomly targeted by boss
    feixiao_aggro = 3/(3+4+6+3)
    robin_aggro = 4/(3+4+6+3)
    aven_aggro = 6/(3+4+6+3)
    topaz_aggro = 3/(3+4+6+3)

    #General Variables_____________________________________________________________
    battle_log = []
    #team_av_log = [] delete after done
    team_av = [feixiao_av, robin_av*0.35, aven_av, topaz_av, numby_av, boss_av] #Ranks characters
    action_taken = 0 #Records amount of characters that have gone before Robin for her ult

    sp = 3 #Skill points

    action_num = -1 #Orders actions, reference variable

    wbroken = False #Is boss broken or not

    while min(team_av) < 550:
        #print(team_av)
        #Feixiao_____________________________________________________________
        if team_av.index(min(team_av)) == 0:
            action_num += 1
            action_taken += 1

            #Buffs ticking down
            if feixiao_skill_buff > 0:
                feixiao_skill_buff -= 1
            if feixiao_talent_buff > 0:
                feixiao_talent_buff -= 1
            #Basic
            if sp < 1:
                sp += 1
                feixiao_ult_stacks += 0.5
                robin_energy += 2 * 1.244 #ER
                if topaz_ult_stacks > 0 and numby_aa_counter < 2: #numby aa via normal attack
                    numby_aa_counter += 1
                    if team_av[4] - (numby_av * 0.5) > min(team_av):
                        team_av[4] -= numby_av * 0.5
                    elif team_av[4] - (numby_av * 0.5) <= min(team_av):
                        team_av[4] = min(team_av)
                if boss_toughness > 0: #only activates if weakness bar positive
                    boss_toughness -= 10
                    if boss_toughness <= 0:
                        wbroken = True
                        boss_toughness = 0
                        team_av[5] += 0.25*boss_av
                    else:
                        wbroken = False
                else:
                    wbroken = True
                battle_log.append([team_av[0], 0, feixiao_ult_stacks, sp, "basic", feixiao_skill_buff,
                                   feixiao_talent_buff, robin_aria, robin_concerto, unnerved, tame, wbroken])
            #Skill
            elif sp >= 1:
                sp -= 1
                feixiao_ult_stacks += 0.5
                feixiao_fua = True
                feixiao_skill_buff = 3
                robin_energy += 2 * 1.244
                if topaz_ult_stacks > 0 and numby_aa_counter < 2:
                    numby_aa_counter += 1
                    if team_av[4] - (numby_av * 0.5) > min(team_av):
                        team_av[4] -= numby_av * 0.5
                    elif team_av[4] - (numby_av * 0.5) <= min(team_av):
                        team_av[4] = min(team_av)
                if boss_toughness > 0:
                    boss_toughness -= 20
                    if boss_toughness <= 0:
                        wbroken = True
                        boss_toughness = 0
                        team_av[5] += 0.25*boss_av
                    else:
                        wbroken = False
                else:
                    wbroken = True
                battle_log.append([team_av[0], 0, feixiao_ult_stacks, sp, "skill", feixiao_skill_buff,
                                   feixiao_talent_buff, robin_aria, robin_concerto, unnerved, tame, wbroken])
            #Ultimate
            #This is counted as a FUA
            if robin_concerto == True and feixiao_ult_stacks >= 6:
                action_num += 1
                robin_energy += 2 * 1.244

                if aven_fua_proc > 0: #FUA proc
                    aven_fua_proc -= 1
                    blind_bet += 1
                    if blind_bet > 10:
                        blind_bet = 10

                if numby_aa_counter < 2: #numby aa via fua
                    numby_aa_counter += 1
                    if team_av[4] - (numby_av * 0.5) > min(team_av):
                        team_av[4] -= numby_av * 0.5
                    elif team_av[4] - (numby_av * 0.5) <= min(team_av):
                        team_av[4] = min(team_av)

                if boss_toughness > 0:
                    boss_toughness -= 60
                    if boss_toughness <= 0:
                        wbroken = True
                        boss_toughness = 0
                        team_av[5] += 0.25*boss_av
                    else:
                        wbroken = False
                else:
                    wbroken = True
                battle_log.append([team_av[0], 0, feixiao_ult_stacks, sp, "ult", feixiao_skill_buff,
                                   feixiao_talent_buff, robin_aria, robin_concerto, unnerved, tame, wbroken])
            #FUA
            if feixiao_fua:
                action_num += 1
                feixiao_ult_stacks += 0.5
                robin_energy += 2 * 1.244

                if aven_fua_proc > 0: #FUA proc
                    aven_fua_proc -= 1
                    blind_bet += 1
                    if blind_bet > 10:
                        blind_bet = 10

                if numby_aa_counter < 2:
                    numby_aa_counter += 1
                    if team_av[4] - (numby_av * 0.5) > min(team_av):
                        team_av[4] -= numby_av * 0.5
                    elif team_av[4] - (numby_av * 0.5) <= min(team_av):
                        team_av[4] = min(team_av)

                if boss_toughness > 0:
                    boss_toughness -= 5
                    if boss_toughness <= 0:
                        wbroken = True
                        boss_toughness = 0
                        team_av[5] += 0.25*boss_av
                    else:
                        wbroken = False
                else:
                    wbroken = True
                battle_log.append([team_av[0], 0, feixiao_ult_stacks, sp, "fua", feixiao_skill_buff,
                                   feixiao_talent_buff, robin_aria, robin_concerto, unnerved, tame, wbroken])
            team_av[0] += feixiao_av

        #Robin_____________________________________________________________
        elif team_av.index(min(team_av)) == 1:
            action_num += 1
            #Buffs ticking down
            if robin_aria > 0:
                robin_aria -= 1
            robin_concerto = False

            #Basic
            if sp < 1:
                sp += 1
                robin_energy += 20 * 1.244
                feixiao_ult_stacks += 0.5
                if topaz_ult_stacks > 0 and numby_aa_counter < 2:
                    numby_aa_counter += 1
                    if team_av[4] - (numby_av * 0.5) > min(team_av):
                        team_av[4] -= numby_av * 0.5
                    elif team_av[4] - (numby_av * 0.5) <= min(team_av):
                        team_av[4] = min(team_av)
                battle_log.append([team_av[1], 1, robin_energy, sp, "basic", robin_aria,
                                   robin_concerto, unnerved, tame])
            #Basic if buff active, Skill if expired/ing
            elif sp >= 1:
                if robin_aria > 1:
                    sp += 1
                    robin_energy += 20 * 1.244
                    feixiao_ult_stacks += 0.5
                    if topaz_ult_stacks > 0 and numby_aa_counter < 2:
                        numby_aa_counter += 1
                        if team_av[4] - (numby_av * 0.5) > min(team_av):
                            team_av[4] -= numby_av * 0.5
                        elif team_av[4] - (numby_av * 0.5) <= min(team_av):
                            team_av[4] = min(team_av)
                    if sp > 5:
                        sp = 5
                    battle_log.append([team_av[1], 1, robin_energy, sp, "basic", robin_aria,
                                       robin_concerto, unnerved, tame])
                else:
                    sp -= 1
                    robin_energy += 35 * 1.244
                    robin_aria = 3
                    battle_log.append([team_av[1], 1, robin_energy, sp, "skill", robin_aria,
                                       robin_concerto, unnerved, tame])
            #Ult
            if robin_energy >= 160 and action_taken >= 3:
                action_num += 1
                robin_concerto = True
                robin_energy = 5
                action_taken = 0
                battle_log.append([team_av[1], 1, robin_energy, sp, "ult", robin_aria,
                                   robin_concerto, unnerved, tame])

                team_av[0] = team_av[1]
                team_av[2] = team_av[1]
                team_av[3] = team_av[1]

            if robin_concerto:
                team_av[1] += 10000/90
            if not robin_concerto:
                team_av[1] += robin_av
        #Aventurine_____________________________________________________________
        elif team_av.index(min(team_av)) == 2:
            action_num += 1
            action_taken += 1
            #Buffs ticking down
            if unnerved > 0:
                unnerved -= 1
            aven_fua_proc = 3

            #Basic every time
            sp += 1
            aven_energy += 20
            feixiao_ult_stacks += 0.5
            robin_energy += 2 * 1.244

            if sp > 5:
                sp = 5

            if topaz_ult_stacks > 0 and numby_aa_counter < 2:
                numby_aa_counter += 1
                if team_av[4] - (numby_av * 0.5) > min(team_av):
                    team_av[4] -= numby_av * 0.5
                elif team_av[4] - (numby_av * 0.5) <= min(team_av):
                    team_av[4] = min(team_av)

            if boss_toughness > 0:
                boss_toughness -= 10
                if boss_toughness <= 0:
                    wbroken = True
                    boss_toughness = 0
                    team_av[5] += 0.25 * boss_av
                else:
                    wbroken = False
            else:
                wbroken = True
            battle_log.append([team_av[2], 2, aven_energy, sp, "basic", robin_aria,
                                robin_concerto, unnerved, tame, wbroken])
            #Ult
            if aven_energy >= 130:
                action_num += 1
                aven_energy = 5
                unnerved = 3
                blind_bet += random.randrange(1, 8)
                if blind_bet > 10:
                    blind_bet = 10
                feixiao_ult_stacks += 0.5
                robin_energy += 2 * 1.244
                if topaz_ult_stacks > 0 and numby_aa_counter < 2:
                    numby_aa_counter += 1
                    if team_av[4] - (numby_av * 0.5) > min(team_av):
                        team_av[4] -= numby_av * 0.5
                    elif team_av[4] - (numby_av * 0.5) <= min(team_av):
                        team_av[4] = min(team_av)
                if boss_toughness > 0:
                    boss_toughness -= 30
                    if boss_toughness <= 0:
                        wbroken = True
                        boss_toughness = 0
                        team_av[5] += 0.25 * boss_av
                    else:
                        wbroken = False
                else:
                    wbroken = True
                battle_log.append([team_av[2], 2, aven_energy, sp, "ult", robin_aria,
                                   robin_concerto, unnerved, tame, wbroken])
            #FUA
            if blind_bet >= 7:
                action_num += 1
                blind_bet -= 7
                aven_energy += 7
                feixiao_ult_stacks += 0.5
                robin_energy += 2 * 1.244
                if numby_aa_counter < 2:
                    numby_aa_counter += 1
                    if team_av[4] - (numby_av * 0.5) > min(team_av):
                        team_av[4] -= numby_av * 0.5
                    elif team_av[4] - (numby_av * 0.5) <= min(team_av):
                        team_av[4] = min(team_av)

                if boss_toughness > 0:
                    boss_toughness -= (10/3) * 7 #3.3... * 7
                    if boss_toughness <= 0:
                        wbroken = True
                        boss_toughness = 0
                        team_av[5] += 0.25*boss_av
                    else:
                        wbroken = False
                else:
                    wbroken = True
                battle_log.append([team_av[2], 2, aven_energy, sp, "fua", robin_aria,
                                   robin_concerto, unnerved, tame, wbroken])
            team_av[2] += aven_av

        #Topaz_____________________________________________________________
        elif team_av.index(min(team_av)) == 3:
            action_num += 1
            action_taken += 1
            #Basic
            if sp < 3 or topaz_ult_stacks > 0:
                sp += 1
                topaz_numby_energy += 20
                robin_energy += 2 * 1.244
                feixiao_ult_stacks += 0.5
                if tame < 2:
                    tame += 1
                if aven_fua_proc > 0: #FUA proc
                    aven_fua_proc -= 1
                    blind_bet += 1
                    if blind_bet > 10:
                        blind_bet = 10
                if numby_aa_counter < 2:
                    numby_aa_counter += 1
                    if team_av[4] - (numby_av * 0.5) > min(team_av):
                        team_av[4] -= numby_av * 0.5
                    elif team_av[4] - (numby_av * 0.5) <= min(team_av):
                        team_av[4] = min(team_av)
                if boss_toughness > 0:
                    boss_toughness -= 10
                    if boss_toughness <= 0:
                        wbroken = True
                        boss_toughness = 0
                        team_av[5] += 0.25 * boss_av
                    else:
                        wbroken = False
                else:
                    wbroken = True
                battle_log.append([team_av[3], 3, topaz_numby_energy, sp, "basic", robin_aria,
                                   robin_concerto, unnerved, tame, wbroken])
            elif sp >= 3 and topaz_ult_stacks < 1:
                sp -= 1
                topaz_numby_energy += 30
                robin_energy += 2 * 1.244
                feixiao_ult_stacks += 0.5
                if tame < 2:
                    tame += 1
                if aven_fua_proc > 0: #FUA proc
                    aven_fua_proc -= 1
                    blind_bet += 1
                    if blind_bet > 10:
                        blind_bet = 10
                if numby_aa_counter < 2:
                    numby_aa_counter += 1
                    if team_av[4] - (numby_av * 0.5) > min(team_av):
                        team_av[4] -= numby_av * 0.5
                    elif team_av[4] - (numby_av * 0.5) <= min(team_av):
                        team_av[4] = min(team_av)
                if boss_toughness > 0:
                    boss_toughness -= 10
                    if boss_toughness <= 0:
                        wbroken = True
                        boss_toughness = 0
                        team_av[5] += 0.25 * boss_av
                    else:
                        wbroken = False
                else:
                    wbroken = True
                battle_log.append([team_av[3], 3, topaz_numby_energy, sp, "skill", robin_aria,
                                   robin_concerto, unnerved, tame, wbroken])
            if topaz_numby_energy >= 130:
                action_num += 1
                topaz_numby_energy = 5
                topaz_ult_stacks = 2

                battle_log.append([team_av[3], 3, topaz_numby_energy, sp, "ult", robin_aria,
                                   robin_concerto, unnerved, tame, wbroken])
            team_av[3] += topaz_av
        #Numby_____________________________________________________________
        elif team_av.index(min(team_av)) == 4:
            action_num += 1
            numby_action = True
            numby_aa_counter = 0
            robin_energy += 2 * 1.244
            feixiao_ult_stacks += 0.5
            if tame < 2:
                tame += 1
            if aven_fua_proc > 0:  # FUA proc
                aven_fua_proc -= 1
                blind_bet += 1
                if blind_bet > 10:
                    blind_bet = 10
            if boss_toughness > 0:
                boss_toughness -= 20
                if boss_toughness <= 0:
                    wbroken = True
                    boss_toughness = 0
                    team_av[5] += 0.25 * boss_av
                else:
                    wbroken = False
            else:
                wbroken = True
            battle_log.append([team_av[4], 4, numby_energy, topaz_ult_stacks, "fua", robin_aria,
                               robin_concerto, unnerved, tame, wbroken])
            if topaz_ult_stacks > 0:
                topaz_ult_stacks -= 1
            team_av[4] += numby_av
        #Boss_____________________________________________________________
        elif team_av.index(min(team_av)) == 5:
            action_num += 1
            if boss_toughness == 0:
                boss_toughness = 200
            if boss_attack == 0:
                boss_attack += 1
                #Two singular attacks in a row, will count within the same action
                #Will not put FUA attacks here for simplicity (fua will be after boss turn)
                #Which isn't that impactful on av, but may increase aven's fua stacks since
                #in actual combat, attack 1 can weakness break, and then no more fua stacks
                for i in range(2):
                    ally_target = choices([0,1,2,3],[feixiao_aggro,robin_aggro,aven_aggro,topaz_aggro])
                    if ally_target[0] == 0:
                        blind_bet += 1
                    elif ally_target[0] == 1:
                        robin_energy += 15
                        blind_bet += 1
                    elif ally_target[0] == 2:
                        aven_energy += 15
                        blind_bet += 2
                    else:
                        topaz_numby_energy += 15
                        blind_bet += 1
                battle_log.append([team_av[5], 5, boss_attack])
            elif boss_attack == 1:
                boss_attack -= 1
                #Attacks all targets
                robin_energy += 10
                aven_energy += 10
                topaz_numby_energy += 10
                blind_bet += 5
                battle_log.append([team_av[5], 5, boss_attack])
            team_av[5] += boss_av
        #Out of turn FUA attacks_____________________________________________________________
        #Feixiao FUA
        if feixiao_fua and (not battle_log[action_num][1] == 0):
            action_num += 1
            feixiao_fua = False
            feixiao_ult_stacks += 0.5
            robin_energy += 2 * 1.244

            if aven_fua_proc > 0:  # FUA proc
                aven_fua_proc -= 1
                blind_bet += 1
                if blind_bet > 10:
                    blind_bet = 10

            if numby_aa_counter < 2 and numby_action == False:
                numby_aa_counter += 1
                if team_av[4] - (numby_av * 0.5) > min(team_av):
                    team_av[4] -= numby_av * 0.5
                elif team_av[4] - (numby_av * 0.5) <= min(team_av):
                    team_av[4] = min(team_av)

            if boss_toughness > 0:
                boss_toughness -= 5
                if boss_toughness <= 0:
                    wbroken = True
                    boss_toughness = 0
                    team_av[5] += 0.25 * boss_av
                else:
                    wbroken = False
            else:
                wbroken = True
            battle_log.append([battle_log[action_num-1][0], 0, feixiao_ult_stacks, sp, "fua", feixiao_skill_buff,
                               feixiao_talent_buff, robin_aria, robin_concerto, unnerved, tame, wbroken])
        #Aven FUA
        if blind_bet >= 7:
            action_num += 1
            blind_bet -= 7
            aven_energy += 7
            feixiao_ult_stacks += 0.5
            robin_energy += 2 * 1.244
            if numby_aa_counter < 2 and numby_action == False:
                numby_aa_counter += 1
                if team_av[4] - (numby_av * 0.5) > min(team_av):
                    team_av[4] -= numby_av * 0.5
                elif team_av[4] - (numby_av * 0.5) <= min(team_av):
                    team_av[4] = min(team_av)

            if boss_toughness > 0:
                boss_toughness -= (10 / 3) * 7  # 3.3... * 7
                if boss_toughness <= 0:
                    wbroken = True
                    boss_toughness = 0
                    team_av[5] += 0.25 * boss_av
                else:
                    wbroken = False
            else:
                wbroken = True
            battle_log.append([battle_log[action_num-1][0], 2, aven_energy, sp, "fua", robin_aria,
                               robin_concerto, unnerved, tame, wbroken])
        numby_action = False

    return battle_log

#teamfrat_av([137,120.4,135.6,139.6])
combat_sim = teamfrat_av([137,120.4,135.6,139.6])
max_av = 0
for i in range(len(combat_sim)):
    print(combat_sim[i])
    if max_av < combat_sim[i][0]:
        max_av = combat_sim[i][0]
print(max_av)
#print(combat_sim)
#print(len(combat_sim))




