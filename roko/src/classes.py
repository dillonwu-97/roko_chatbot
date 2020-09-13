from emora_stdm import DialogueFlow, KnowledgeBase, Macro
from enum import Enum, auto
import json
from dialogues import spec_Dict, dict_genre, mpMiniGames_dict, mpCharacter_dict, underChar_dict,\
acVillager_dict, smashStage_dict, smashfighter_dict,descripSpec_Dict, mkartChar_dict,\
leagueChamp_dict, dotaHeros_dict, r6sOperator_dict, overHero_dict,\
r6sMode_dict, pokeType_dict,leagueMode_dict, mkartCourse_dict,overMode_dict,\
r6sOperator_dict, dotaMode_dict, acThings_dict, underRoute_dict, censor, pokeChar_dict, \
personaP_dict,personaBoss_dict, borderMan_dict,borderHunter_dict, hearthClass_dict, \
hearthMode_dict,simsVersion_dict, simsTraits_dict, spireChar_dict, spireBoss_dict, \
skyrimGuild_dict,skyrimCity_dict,pvzPlant_dict,plantZombie_dict,assassinChar_dict,\
assassinLocation_dict, haloVersions_dict, haloModes_dict, fireVersions_dict, fireWeapons_dict
import random
import nltk
from nltk import word_tokenize, PorterStemmer
import spacy
from spacy.symbols import nsubj, VERB, ADJ, NOUN

# Opening the json dictionary
# call it ontology2 so as not to confuse it with ontology from hw2
with open('ont_dict.json') as json_file:
    ontology2 = json.load(json_file)

####################################################################################################
# GLOBAL TABLES USED THROUGHOUT THE CODE
talked = []
not_talked = ontology2["ontology"]["specificGame"].copy()
mario_party = ["super mario party", "jackbox party pack 6", "mario party", "mario party 2", "mario party 3",
                           "mario party 4", "mario party 5", "mario party 6", "mario party 7", "mario party 8",
                           "mario party 9", "mario party 10"]
pokemon = ["pocket monsters", "pokemon"]
league_of_legends = ["league", "lol"]
super_smash_bros = ["super smash bros.", "super smash bros. melee", "super smash bros. wii",
                                "super smash bros. ultimate", "super smash bros. for nintendo 3ds and wii u", "smash",
                                "super smash brothers", "super smash bros"]
mario_kart = ["mario kart 64", "mario kart: super circuit", "mario kart: double dash", "mario kart ds",
                          "mario kart wii", "mario kart 7", "mario kart 8", "mario kart 8 deluxe", "mario kart",
                          "mario cart"]
overwatch = ['overwatch']
r6s = ["tom clancy's rainbow six siege", "rainbow six siege", "rainbow 6 siege", "r6s"]
dota = ["defense of the ancients", "dota2"]
animal_crossing = ["animal crossing", "animal crossing: wild world", "animal crossing: city folk",
                               "animal crossing: new leaf", "ac", "wild world", "acww", "city folk", "accf", "new leaf",
                               "acnl"]
undertale = ['undertale']
persona5 = ["persona 5", "persona five", "p5", "persona5"]
borderlands = [ "borderlands",  "borderlands 2", "borderlands 3","borderlands: the pre-sequel"]
hearthstone = ['hearthstone']
sims = ["sims", "sims one", "sims 1", "sims 2", "sims two", "sims 3", "sims three", "sims 4", "sims four",
                    "sims online", "sims stories", "sims carnival", "sims medieval", "sims social", "mysims",
                    "sims freeplay", "sims mobile"]
slay_the_spire = ["slay the spire", "sts"]
skyrim = ['skyrim']
plants_versus_zombies= ["plants versus zombies","plants vs. zombies 2","plants vs. zombies: garden warfare","plants vs. zombies. garden warfare 2","plants vs. zombies", "pvz:gw", "pvz:gw2", "pvz", "pvz2"]
fire_emblem =["fire emblem","awakening","binding blade", "fates birthright", "fates conquest",  "fates revelation","gaiden","genealogy of the holy war","mystery of the emblem", "path of radiance","radiant dawn","sacred stones", "shadow dragon","shadow dragon and the blade of light","shadows of valentia", "thracia", "thracia 776","thracia seven seven six", "three houses"]
halo= ["halo", "combat evolved","halo 2","halo two","halo 3", "helo three", "halo wars","halo 3: odst","halo: reach", "combat evolved anniversary","halo 4","halo four","spartan assault","the master chief collection","spartan strike","halo 5","halo five","halo wars 2", "fireteam raven"]
assassins_creed = ["assassin's creed", "assassins creed","assassins' creed"]

container_titles = {
    "mario party": mario_party, 
    "pokemon": pokemon, 
    "league of legends": league_of_legends,
    "super smash brothers": super_smash_bros,
    "mario kart": mario_kart,
    "overwatch": overwatch,
    "rainbow 6 siege": r6s,
    "dota": dota,
    "animal crossing": animal_crossing,
    "undertale": undertale,
    "persona 5": persona5,
    "borderlands": borderlands,
    "hearthstone": hearthstone,
    "sims": sims,
    "slay the spire": slay_the_spire,
    "skyrim": skyrim,
    "plants versus zombies": plants_versus_zombies,
    "fire emblem": fire_emblem,
    "halo":halo,
    "assassins creed": assassins_creed
}

# Video Game containers for all of the respective dictionaries for each respective game we cover
# different from above because these start with C for container
Cmario_party = ["mpMiniGames", "mpCharacter"]
Cpokemon = ["pokeChar", "poketype"]
Cleague_of_legends = ["leagueChamp", "leageMode"]
Csuper_smash_bros = ["smashfighter", "smashStage"]
Cmario_kart = ["mkartChar", "mkcartCourse"]
Coverwatch = ["overHeros", "overMode"]
Cr6s = ["r6sMode", "r6soperator"]
Cdota = ["dotaHeroes", "dota2Modes"]
Canimal_crossing  = ["acVillager", "acThings"]
Cundertale = ["underChar","underRoute"]
Cpersona5 = ["personaP", "personaBoss"]
Cborderlands = ["borderMan","borderVault"]
Chearthstone = ["hearthClass", "hearthMode"]
Csims = ["sims", "simsTraits"]
Cslay_the_spire = ["spireCharacter", "spireBoss"]
Cskyrim = ["skyrimGuild", "skyrimCity"] 
Cplantsvzombies = ["pvzPlant", "pvzZombie"]
Cfire_emblem = ["fireVersions", "fireWeapons"]
Chalo = ["haloVersion", "haloMode"]
Cassassins_creed = ["AssassinChar", "AssassinLocation"]
container_list = {"mario party": Cmario_party, 
                    "pokemon": Cpokemon, 
                    "league of legends": Cleague_of_legends,
                    "super smash brothers": Csuper_smash_bros,
                    "mario kart": Cmario_kart,
                    "overwatch": Coverwatch,
                    "rainbow 6 siege": Cr6s,
                    "dota": Cdota,
                    "animal crossing": Canimal_crossing,
                    "undertale": Cundertale,
                    "persona 5": Cpersona5,
                    "borderlands": Cborderlands,
                    "hearthstone": Chearthstone,
                    "sims": Csims,
                    "slay the spire": Cslay_the_spire,
                    "skyrim": Cskyrim,
                    "plants versus zombies": Cplantsvzombies,
                    "fire emblem":Cfire_emblem,
                    "halo":Chalo,
                    "assassins creed": Cassassins_creed
                }


containerItem_dict = {
    "mario party": ["in mario party the mini games allow you to compete against other players to earn coins and different bonuses.","mini games",
                   "in mario party you can play as many different characters, they are largely iconic faces from the mario franchise.", "characters"],
    "pokemon": ["in pokemon there are creatures that you train, each have different abilities and backstories.", "pokemon",
                "each pokemon has one or two types which determine their strengths and weaknesses", "types"],
    "league of legends": ["a league champion is the character you can choose to play, each with their own roles and abilities.", "champions",
                          "a  mode in league of legends allows for different objectives during your game play.", "modes"],
    "super smash brothers": ["fighters in super smash brothers are the characters you can embody to combat your opponents.","fighters",
                             "a stage in super smash brothers is the location used to battle your opponents, some have cool hazards to provide extra challange.", "stages"],
    "mario kart": ["in mario kart you can play as many different characters, also called racers, they are largely iconic faces from the mario franchise.", "racers",
                   "the races in mario kart take place on different courses, which allow for variation in hazards and aesthetics.", "courses"],
    "overwatch": ["an overwatch hero is the character you can choose to play, each with their own roles and abilities.", "hero",
                  "a  mode in overwatch allows for different objectives during your game play.", "modes"],
    "rainbow 6 siege": ["a  mode in rainbow 6 siege allows for different objectives during your game play.", "modes",
                        "an operator from rainbow six siege refers to their many playable characters.", "operators"],
    "dota": ["the heroes from dota refer to the different playable characters.", "heroes",
             "a  mode in dota allows for different objectives during your game play.", "modes"],
    "animal crossing": ["the villagers are the people and animals who can come live on your island as you expand.", "villagers",
                        "in animal crossing there are many things to do as you expand your island.", "things to do"],
    "undertale": ["the undertale characters are the different enemies you fight and befriend along the way.", "characters",
                  "the different routes of undertale are determined by how you interact with character, whether you befriend or kill them, and will impact the progression of the game.", "routes"],
    "persona 5": ["the personas in persona 5 are the creatures that you can collect and assimilate, helping you to battle bosses and clear through dungeons.", "personas",
                  "the bosses in persona 5 are the the true forms of the cognitive self of the villain that you are after, essentially the big bad at the end of the dungeon.", "bosses"],
    "borderlands": ["the manufacturers in borderlands are the producers of all of the offensive and defensive equipment, each with specific styles", "manufacturers",
                   "the vault hunters of borderlands are the different playable characters.", "hunters"],
    "hearthstone": ["in hearthstone the class is the primary determinant of a hero's powers and abilities, and the strongest factor in deck selection.", "classes",
                "in hearthstone the game mode determines the set of rules surrounding each battle.", "modes"],
    "sims": ["sims has been rereleased multiple times throughout the years, to allow developers to add new features.", "versions",
             "when creating a sim your are encourages to give them character traits, so that each one has a unique personality.", "traits"],
    "slay the spire": ["in slay the spire, each character has different card pool and starting item which define how the character can be played.","characters",
                       "in slay the spire the bosses are the most difficult enemies that you have to fight at the end of each floor.", "bosses"],
    "skyrim": ["the guilds in skyrim are factions you can join that help you clear through the game.", "guilds",
               "the cities in skyrim are locations you can visit along your journey", "cities"],
    "plants versus zombies": ["plants in plants versus zombies are the defense mechanism to counter zombie attacks.", "plants",
                              "zombies in plants versus zombies are the attackers coming to eat your brains.", "zombies"],
    "fire emblem": ["fire emblem has been rereleased multiple times throughout the years, to allow developers to add new storylines and characters.", "versions",
                    "in fire emblem the different weapons can be used to accomplish different goals during a battle.", "weapons"],
    "halo": ["sims has been rereleased multiple times throughout the years, to allow developers to add new features.", "versions",
             "a  mode in halo allows for different objectives during your game play.", "modes"],
    "assassins creed": ["the assassins in assassins creed are the different playable characters, eachwith a different story arch.", "assassins",
                     "assassins creed has taken place in many cool locations accross the globe, and during an array of time persons.", "possible future locations"]
}

container_dict = {
    "mario party": [mpMiniGames_dict, mpCharacter_dict],
    "pokemon": [pokeChar_dict, pokeType_dict],
    "league of legends": [leagueChamp_dict, leagueMode_dict],
    "super smash brothers": [smashfighter_dict, smashStage_dict],
    "mario kart": [mkartChar_dict, mkartCourse_dict],
    "overwatch": [overHero_dict, overMode_dict],
    "rainbow 6 siege": [r6sMode_dict, r6sOperator_dict],
    "dota": [dotaHeros_dict, dotaMode_dict],
    "animal crossing": [acVillager_dict, acThings_dict],
    "undertale": [underChar_dict, underRoute_dict],
    "persona 5": [personaP_dict, personaBoss_dict],
    "borderlands": [borderMan_dict, borderHunter_dict],
    "hearthstone": [hearthClass_dict, hearthMode_dict],
    "sims": [simsVersion_dict, simsTraits_dict],
    "slay the spire": [spireChar_dict, spireBoss_dict],
    "skyrim": [skyrimGuild_dict, skyrimCity_dict],
    "plants versus zombies": [pvzPlant_dict, plantZombie_dict],
    "fire emblem": [fireVersions_dict, fireWeapons_dict],
    "halo": [haloVersions_dict, haloModes_dict],
    "assassins creed": [assassinChar_dict, assassinLocation_dict]
}

###########################################################################

###########################################################################
# GLOBAL FUNCTIONS USED THROUGHOUT THE CODE
def title_finder(s):
    for key in container_titles.keys():
        if s in container_titles[key]:
            s = key
    return s
# num = parameter for macro number (0 or 1); 0 for specific2, 1 for specific3
# game = the game name
# ans = ans1 or ans2 (character or mode)
def response_finder (game, ans, num):
    # special condition for pokemon
    if game == 'pokemon' and num == 0:
        valueTemp = pokeChar_dict.get(ans)
        if (valueTemp[1] == ""):
            return (ans + ' is such a ' + random.choice(syn_dict["cool"])+" "+ str(valueTemp[0]) + ' pokemon! ' + str(valueTemp[2]))
        else:
            return (ans + ' is such a ' + random.choice(syn_dict["cool"]) + " " + str(valueTemp[0]) + " and "+ str(valueTemp[1]) + ' pokemon! '+ str(valueTemp[2]))
    # special condition for assassins creed
    if game == 'assassins creed' and num == 1:
        return str(ans) + "is an interesting idea, it would be fun to see the franchise in "+assassinLocation_dict.get(ans)+"."

    return container_dict[game][num].get(ans)

###########################################################################

class SPECIFIC1a(Macro):
    def run(self, ngrams, vars, args) -> str:
        try: 
            s = vars['specG']
            s = title_finder(s)
            # double checking just to make sure
            if s not in talked:
                talked.append(s)
            if s in not_talked:
                not_talked.remove(s)
            #return s
            opinion = spec_Dict.get(s)[0]
            question = spec_Dict.get(s)[1]

            return opinion + " "+question
        except:
            vars['specG'] = 'pokemon'
            return "i dont think we were talking about any game that i was interested in but one of my favorites is definitely " + vars['specG']


class SPECIFIC2a(Macro):
    def run(self, ngrams, vars, args) -> str:
         if len(vars['specG']) > 0:
            s = vars['specG']
            vars['switch'] = "false"
            try:
                ans1= vars['ans1']
            except:
                ans1 = vars['ans_not1']
            # find the dictionary that ans1(character) is in from ontology2
            # specAnswer1 is the dictionary entry containing all the other entries we need to iterate through
            container = []
            game_name = []
            specAnswerList = ["specAnswer1", "specAnswer2"]
            for sa in specAnswerList:
                for entry in ontology2["ontology"][sa]:
                    if ans1 in ontology2["ontology"][entry]:
                        container.append(entry)
            for item in container:
                for c in container_list.keys():
                    if item in container_list[c]:
                        game_name.append(c)
            
            char = ans1
            res = ""
            # Big dict energy 
            s = title_finder(s)
            if s in game_name:
                res = response_finder(s, ans1, 0)
                opinion = spec_Dict.get(s)[2]
                question = spec_Dict.get(s)[3]
                return res+" "+question
            if res == "" and len(game_name)>0:
                switch_game = random.choice(game_name)
                vars['switch_game'] = switch_game
                vars['switch'] = "true"
                res = "i think that is actually from " + str(switch_game) + ". would you like to talk about " + str(switch_game) + " instead?"
                return res
            else:
                question = spec_Dict.get(s)[3]
                return "sorry i got a little confused by your answer "+ ans1+ "! "+ question

class SPECIFIC2b(Macro):
    def run(self, ngrams, vars, args) -> str:

         if len(vars['specG']) > 0:
            s = vars['specG']
            vars['switch'] = "false"
            s = title_finder(s)

            #return s
            opinion = spec_Dict.get(s)[2]
            question = spec_Dict.get(s)[3]

            return opinion + " "+question


class SPECIFIC3a(Macro):
    def run(self, ngrams, vars, args) -> str:
         if len(vars['specG']) > 0:
            s = vars['specG']
            try:
                ans2= vars['ans2']
            except:
                ans2 = vars['ans_not2']
            vars['switch'] = "false"

            # find where ans2 came from
            container = []
            game_name = []
            specAnswerList = ["specAnswer1", "specAnswer2"]
            for sa in specAnswerList:
                for entry in ontology2["ontology"][sa]:
                    if ans2 in ontology2["ontology"][entry]:
                        container.append(entry)
            for item in container:
                for c in container_list.keys():
                    if item in container_list[c]:
                        game_name.append(c)

            s = title_finder(s)
            vars['genre'] = game_genre_finder(s)
            res = ""
            if s in game_name:
            #return s
                res = response_finder(s, ans2, 1)
                opinion = spec_Dict.get(s)[4]
                genre = spec_Dict.get(s)[5]
                return res + " what do you think about the "+ genre + " genre?"
            if res == "" and len(game_name)>0:
                switch_game = random.choice(game_name)
                vars['switch_game'] = switch_game
                vars['switch'] = "true"
                res = "i think that is actually from " + str(switch_game) + ". would you like to talk about " + str(switch_game) + " instead?"
                return res
            else:
                question = spec_Dict.get(s)[3]
                return "sorry i got a little confused by your answer \"" + ans2 + "\"! " + question
            #return s


class SPECIFIC3b(Macro):
    def run(self, ngrams, vars, args) -> str:

         if len(vars['specG']) > 0:
            s = vars['specG']
            vars['switch'] = "false"
            s = title_finder(s)
            vars['genre'] = game_genre_finder(s)
            #return s
            opinion = spec_Dict.get(s)[4]
            genre = spec_Dict.get(s)[5]

            return opinion + " what do you think about the "+ genre + " genre?"

class genre_pivot(Macro):
    def run (self, ngrams, vars, args):
        genre = vars['genre']
        game = None
        genre = genre_finder(genre)
        if genre in container_spec_genre:
            for i in container_spec_genre[genre]:
                if i in not_talked:
                    game = i
                    break
        return_val = dict_genre.get(genre)
        if game != None:
            talked.append(game)
            not_talked.remove(game)
            vars['specG'] = game
            return_val += str(game) + " is also a " + str(genre) + " game. would you like to talk about it?"
        # if no game was found
        else:
            # we still have games to talk about
            try:
                game = random.choice(not_talked)
                not_talked.remove(game)
                talked.append(game)
                vars['specG'] = game
                return_val += " unfortunately im not familiar with any other " + str(genre) + " games. but i know of other awesome games like " + str(game) + ". are you familiar?"
            except:
            # we're out of games to talk about
                return_val = "unfortunately we've discussed all the games i'm familiar with! goodbye"
        return return_val

class genre_pivot_learning(Macro):
    def run(self, ngrams, vars, args):
        genre = vars['genre']
        game = None
        if genre in container_spec_genre:
            for i in container_spec_genre[genre]:
                if i in not_talked:
                    game = i
                    break
        return_val = ""
        if game != None:
            talked.append(game)
            not_talked.remove(game)
            vars['specG'] = game
            return_val ="oh i didnt know you were interesting in "+ genre+" games! one of the "+genre+ " games i am most familiar with is "+ str(game) + ".  would you like to talk about it?"
        # if no game was found
        else:
            game = random.choice(not_talked)
            not_talked.remove(game)
            talked.append(game)
            vars['specG'] = game
            return_val = " hmmmmm... i am not sure about games in " + genre + " genre. but i know of other awesome games like " + game + ". are you familiar?"
        return return_val


class list_items_one(Macro):
    def run (self, ngrams, vars, args):
        if len(vars['specG']) > 0:
            s = vars['specG']
            s = title_finder(s)
            definition = containerItem_dict.get(s)[0]
            noun = containerItem_dict.get(s)[1]
            itemslist = random.sample(ontology2["ontology"][container_list[s][0]], 3)
        return definition+ ' some '+noun+ ' include ' + itemslist[0] + ', ' + itemslist[1] + ', and ' + itemslist[2]+ '.'
    
class list_items_two(Macro):
    def run (self, ngrams, vars, args):
        if len(vars['specG']) > 0:
            s = vars['specG']
            s = title_finder(s)
            definition = containerItem_dict.get(s)[2]
            noun = containerItem_dict.get(s)[3]
            itemslist = random.sample(ontology2["ontology"][container_list[s][1]], 3)
        return definition+ ' some '+noun+ ' include ' + itemslist[0] + ', ' + itemslist[1] + ', and ' + itemslist[2]+ '.'
# Synonym generator with NLTK tags
# synonym detection
class syn_det(Macro):
    def run(self, ngrams, vars, args):
        temp = vars['input']
        text = word_tokenize(temp)
        adj = [word for word, pos in nltk.pos_tag(text) if pos=='A' or pos=='JJ' or pos=='VBG']
        return_str = 'why do you think the game is '
        for i in range(len(adj)):
            if i == len(adj)-1 and len(adj) > 1:
                return_str = return_str + adj[i-1] + ' and ' + adj[i]
            else:
                return_str = return_str + adj[i] + ' '
        if len(adj) == 0: return_str = 'why do you feel this way'
        return return_str

class explain_response(Macro):
    def run(self, ngrams, vars, args):
        temp = vars['explain']
        ps = PorterStemmer() # stemming adjectives
        try:
            flag = 0 # LIKE IF 0
            obj = vars['like']
        except:
            flag = 1 # DISLIKE IF 1
            obj = vars['dislike']
        not_catch = find_not(temp)
        text = word_tokenize(temp)
        adj = []
        tag = []
        for word, pos in nltk.pos_tag(text): 
            if pos=='JJ' or pos=='VBG':
                adj.append(word)
                tag.append(pos)
        return_str = 'video games can create a multitude of interesting worlds.' # default

        for i in range(len(adj)):
            adjword = ps.stem(adj[i])
            if (tag[i] == 'VBG'):
                if (adjword[-1] == 'e'): 
                    adjword+='d'
                else: 
                    adjword+='ed'
            if flag == 0:
                return_str = 'it is interesting that ' + obj + ' make you feel ' + not_catch + adjword + '.'
            else:
                return_str = 'it is interesting that ' + obj + ' make you feel ' + not_catch + adjword + ' but '
        return return_str


######################################################################
# Genre Macros
# CONTAINER METHOD FOR GENRES
# platformer
# DICTIONARY of all the specific games we have matched with each specific genre
container_spec_genre = {
    "shooter":["overwatch", "rainbow 6 siege", "borderlands", "halo"],
    "action":["super smash brothers", "fire emblem", "assassins creed", "skyrim"],
    "fighting":["super smash brothers", "assassins creed", "borderlands"],
    "adventure":["assassins creed", "fire emblem", "skyrim", "pokemon"],
    "moba":["league of legends", "dota"],
    "party":["mario party", "mario kart"],
    "simulation":["animal crossing", "sims"],
    "strategy":["hearthstone", "fire emblem", "plants vs zombies", "slay the spire", "pokemon"],
    "racing":["mario kart"],
    "rpg":["undertale", "persona 5", "fire emblem", "skyrim"],
    "tbs":["pokemon", "fire emblem"]

}

def find_not(sentence):
    not_catch = ""
    if "not" in sentence.split():
        not_catch = "not "
    return not_catch

# this finds the genre of the game
def game_genre_finder (game):
    genre_val = []
    for key in container_spec_genre:
        if game in container_spec_genre[key]:
            genre_val.append(key)
    return random.choice(genre_val)

# this finds the genre in container_gen_syn
def genre_finder (temp_genre):
    for key in container_gen_syn.keys():
        if temp_genre in container_gen_syn[key]:
            temp_genre = key
    return temp_genre
#################################################################################

class GENRE_RECOMMENDER(Macro):
    def run(self, ngrams, vars, args):
        s = vars['genre']
        temp_genre = genre_finder(s)
        game = ''
        # IF THERE IS A SPECIFIC GAME OF THE GENRE IN QUESTION
        if temp_genre in container_spec_genre:
            game = random.choice(container_spec_genre[temp_genre])
            if len(game) > 0:
                vars['specG'] = game
                return "i know of some " + str(s) + " games! i think you might like " + str(game) +"."
        # IF THERE IS NOT SPECIFIC GAME OF THE GENRE IN QUESTION, TRY TO FIND A GENERAL GAME OF THE GENRE
        dialogue = ""
        if temp_genre in ontology2["ontology"]:
            select_from = ontology2["ontology"][temp_genre]
            game=random.choice(select_from)
            dialogue = "i definitely know of some " + s + " games. try " + game
        # IF THERE IS NO GAME WE KNOW OF THAT FITS THE GENRE
        else:
            dialogue = "sorry i dont know any games of that genre."
        return dialogue

class GENRE_OPINION(Macro):
    def run(self, ngrams, vars, args) -> str:
        s = vars['genre']
        temp_genre = genre_finder(s) # genre finder only works for the genres of specific games
        # FIND THE APPROPRIATE DIALOGUE FOR THE GENRE
        # 1) IMPORTANT NOTE: IN DIALOGUES.PY, DICT_GENRE, WE HAVE DIALOGUES FOR EACH GENRE.
        # 2) WE INCLUDED GENRES THAT ARE MARGINALLY RELATED TO THESE GENRES IN ontology["genre"] AND IN 
        # container_gen_syn
        # 3) IF WE ADD A NEW GENRE, WE ADD IT INTO BOTH OF THESE PLACES
        # 4) MOST IMPORTANTLY, WE ADD IT TO ONLY THE PLACES WHERE THE GENRE KEY IN DICT_GENRE EXISTS IN THE
        # GENRE VALUE: FOR EXAMPLE: ADDING "FANTASY" GENRE TO "ADVENTURE IS OK" BECAUSE IN DICT_GENRE
        # the word "adventure" is in the corresponding value "adventure games really let you experience what it's like to be a movie protagonist"
        # however we cannot add to "tbs" because the key "tbs" is not in the corresponding value ""turn based strategy games, along with turn-based tactic games, challenge me for the better.""
        if temp_genre != s:
            different = (dict_genre.get(temp_genre)).replace(temp_genre, s)
            return different + " would you like a " + s + " game?"
        elif temp_genre in dict_genre:
            return dict_genre.get(temp_genre) + " would you like a " + s + " game?"
        else:
            return 'interesting choice but im not familiar with that genre.'


class Genre_Opinion_simple:
    def run(self, ngrams, vars, args) -> str:
            adj1 =  random.choice(syn_dict["interesting"])
            adj2= adj1
            while (adj2 == adj1):
                adj2 = random.choice(syn_dict["interesting"])
            return  "the " +adj1+ " and "+ adj2+ " "+vars["genreTrait"]+ " are one of the best parts of the "+genre_finder (vars["genre"]) + " genre."


class like_macro(Macro):
    def run(self, ngrams, vars, args):
        temp = vars['like']
        if temp == "" or (temp.strip() in censor):
            temp = "video games"
        return temp

class dislike_macro(Macro):
    def run(self, ngrams, vars, args):
        temp = vars['dislike']
        if temp == "" or (temp.strip() in censor):
            temp = "video games"
        return temp

class game_desc(Macro):
    def run(self, ngrams, vars, args):
        explain = vars['specG']
        vars['switch3'] = "false" #to keep consistant with the favegames
        dialogue = descripSpec_Dict.get(explain)
        dialogue += " does that interest you?"
        return dialogue

class fave_games(Macro):
    def run(self, ngrams, vars, args):
        temp = not_talked
        game = random.choice(temp)
        # update list of discussed topics
        not_talked.remove(game)
        vars['switch3'] = "false"
        talked.append(game)
        vars['specG'] = game
        if len(not_talked ) <= 17:
            game = "maybe we should talk about something else...what is your favorite kind of story?"
            vars['switch3'] = "true"
        else:
            game = 'well one of my favorite games is ' + game + '. are you interested in that game?'
        return game
####################################################################################################
# This were put here because they arent changed that frequently and are long af
# This is a dictionary of all the genres in the ontology matched within each overarching genre
container_gen_syn = {
    "action": ["action"],
    "adventure": ["adventure", "fantasy"],
    "beat-em-up": ["beat-em-up", "beat em up","beat them up", "beet-em-up","beet em up"],
    "casual": ["casual"],
    "educational": ["educational"],
    "fighting": ["fighting"],
    "idle": ["idle"],
    "metroidvania": ["metroidvania"],
    "mmorpg": ["mmorpg"],
    "moba": ["moba"],
    "party": ["party"],
    "platformer": ["platformer"],
    "puzzle": ["puzzle"],
    "racing": ["racing"],
    "real-time strategy": ["real-time strategy", "real time strategy", "real-time-strategy"],
    "rhythm": ["rhythm"],
    "roguelike": ["roguelike"],
    "role-playing games": ["role-playing games", "role playing game", "rpg"],
    "sandbox rpg": ["sandbox rpg", "sandbox"],
    "shooter": ["shooter", "shooters", "shooting", "fps", "shoot"],
    "simulation": ["simulation", "sim"],
    "stealth": ["stealth"],
    "strategy": ["strategy"],
    "survival": ["survival"],
    "survival horror": ["survival horror"],
    "tactical rpg": ["tactical rpg", "tactical role playing game"],
    "tbs": ["tbs", "turn based strategy", "turn based", "turn"],
    "tbt": ["tbt", "turn based dungeon"],
    "tower defense": ["tower defense"],
    "visual novels": ["visual novels"]
}

# This will be moved one day someday 
syn_dict = {
    "cool":
        [
        "agreeable",
        "charming",
        "delightful",
        "enchanting",
        "enjoyable",
        "entertaining",
        "fun",
        "interesting",
        "pleasant",
        "pleasing"
        ],
    "interesting":
        [
            "complex",
            "intricate",
            "elaborate",
            "detailed",
            "complicated",
            "poignant",
            "pleasing",
            "magnetic",
            "engrossing",
            "clever",
            "captivating",
            "bewitching",
            "absorbing"

        ]
}


# if __name__ == "__main__":
#     # Testing
#     s = "pokemon"
#     ans1 = 'rainbow road'
#     container = []
#     game_name = []
#     specAnswerList = ["specAnswer1", "specAnswer2"]
#     for sa in specAnswerList:
#         for entry in ontology2["ontology"][sa]:
#             if ans1 in ontology2["ontology"][entry]:
#                 container.append(entry)
#     for item in container:
#         for c in container_list.keys():
#             if item in container_list[c]:
#                 game_name.append(c)
    
#     char = ans1
#     res = ""
#     # Big dict energy 
#     s = title_finder(s)
#     print(container)
#     print(game_name)
#     if s in game_name:
#         res = response_finder(s, ans1, 0)
#         opinion = spec_Dict.get(s)[2]
#         question = spec_Dict.get(s)[3]
#         print('hello')
#     if res == "" and len(game_name)>0:
#         switch_game = random.choice(game_name)
#         res = "i think that is actually from " + str(switch_game) + ". would you like to talk about " + str(switch_game) + " instead?"
#         print(res)
#     else:
#         question = spec_Dict.get(s)[3]
#         print( "sorry i got a little confused by your answer ")

