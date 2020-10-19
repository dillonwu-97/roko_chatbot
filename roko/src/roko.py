from emora_stdm import DialogueFlow, KnowledgeBase, Macro
from enum import Enum, auto
import json
from dialogues import spec_Dict, dict_genre, mpMiniGames_dict, mpCharacter_dict, underChar_dict,\
acVillager_dict, pokeType_dict, smashStage_dict, smashfighter_dict, mkartChar_dict,\
leagueChamp_dict, dotaHeros_dict, r6sOperator_dict, overHero_dict, descripSpec_Dict, descriptionFull_dict,\
comp_Dict
from classes import SPECIFIC1a, SPECIFIC2a, SPECIFIC2b, SPECIFIC3a, SPECIFIC3b, GENRE_OPINION,\
syn_det, like_macro, dislike_macro, game_desc, ontology2, list_items_one, list_items_two,\
GENRE_RECOMMENDER, explain_response, fave_games, genre_pivot, genre_pivot_learning
import random
import nltk
from nltk import word_tokenize
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 

# Opening the json dictionary
with open('ont_dict.json') as json_file:
    ontology = json.load(json_file)
######################################################################################################

class State(Enum):
    # # Initialize
    
    # Social Gaming
    sS1a= auto()
    sS2a= auto()
    sS2b= auto()
    sS2c= auto()
    sS3a= auto()
    sS3b= auto()
    sS3c= auto()
    sU1a= auto()
    sU2a= auto()
    sU2b= auto()
    sS1aA= auto()

    # Learning module
    LS1a= auto()
    LS2a= auto()
    LS2aa= auto()
    LS3a = auto()
    LS3aa = auto()
    LU1a= auto()
    LU2a= auto()
    LU3a= auto()
    LS1b = auto()

    # Start state
    S0= auto()

    # Favorite gaming
    fS1a= auto()
    fS1aa= auto()
    fS1b= auto()
    fS1ba= auto()
    fS1bb= auto()
    fS1c= auto()
    fS1d= auto()
    fS2ab= auto()
    fS2ac= auto()
    fS2ba= auto()
    fS2bb= auto()
    fS2da= auto()
    fS2db= auto()
    fS2dc= auto()
    fS3ba= auto()
    fS3bb= auto()
    fS3bd = auto()
    fS4a= auto()
    fS4b= auto()
    fU0= auto()
    fU1d= auto()
    fU2a= auto()
    fU2aa= auto()
    fU2ac= auto()
    fU2b= auto()
    fU2da= auto()
    fU2db= auto()
    fU3b= auto()
    fU4a= auto()
    fU4b= auto()
    fS2bc = auto()
    fS3bc = auto()
    fS4bc = auto()
    fU5a= auto()

    # General Gaming
    gS1a= auto()
    gS1b= auto()
    gS1c= auto()
    gS1d= auto()
    gS1f= auto()
    gS2a= auto()
    gS2b= auto()
    gS2c= auto()
    gS2d = auto()
    gS3aa= auto()
    gS3ab= auto()
    gS3b= auto()
    gS3c= auto()
    gS4a= auto()
    gS4b = auto()
    gS5a= auto()
    gU0= auto()
    gU1aa= auto()
    gU1ac= auto()
    gU1ad= auto()
    gU2a= auto()
    gU2b= auto()
    gU2c= auto()
    gU2d= auto()
    gU3a= auto()
    gU3b= auto()
    gU4a= auto()

    g5a= auto()
    g5b= auto()
    g5c= auto()

    # Health Module
    hS0 = auto()
    hU0 = auto()

    hS1a = auto()
    hS1b = auto()
    hS1c = auto()
    hS1d = auto()

    hU1a = auto()
    hU1b = auto()
    hU1c = auto()
    hU1d = auto()

    hS2END = auto()

    # Meta
    mS0 = auto()
    mU0 = auto()
    mS1a = auto()
    mS1b= auto()
    mS1c = auto()
    mS1d = auto()

    mU1a= auto()
    mU1b = auto()
    mU1c = auto()
    mU1d = auto()

    mS1aa= auto()
    mS1ab = auto()
    mS1ac = auto()

    mS1ba = auto()
    mS1bb = auto()
    mS1bc = auto()

    mS1ca = auto()
    mS1cb = auto()
    mS1cc = auto()


    mS2da = auto()
    mS2db = auto()
    mS2dc = auto()



    mU2a = auto()
    mU2b = auto()
    mU2d = auto()

    mS1db = auto()
    mS1da = auto()

    # Ending
    OOO = auto() #future health module
    END= auto()
    ERR = auto()
    endChallenge= auto()
    endGen= auto()
    endGenre= auto()
    endMario= auto()
    endMeta= auto()
    endOtherGames= auto()
    endPuzzle= auto()
    endRec= auto()
    endSocial= auto()
    endSpecGame= auto()
###########################################################################
## NaTex - Affirmation / Denial / Question
affirm = r"[{#ONT(positive), #ONT(agree), #ONT(like), #ONT(interested)}]"
deny = r"[{#ONT(negative), #ONT(disagree), #ONT(dislike)}]"
general = r"[$generalG={#ONT(largeGameList)} -#ONT(specificGame)]"
dontknow =  '<{' \
            'dont know,do not know,unsure,[not,{sure,certain}],hard to say,no idea,uncertain,[!no {opinion,opinions,idea,ideas,thought,thoughts,knowledge}],' \
            '[{dont,do not}, have, {opinion,opinions,idea,ideas,thought,thoughts,knowledge}],' \
            '[!{cant,cannot,dont} {think,remember,recall}]' \
            '}>'
#### Module - General Gaming / Experience Gaming
# Regularly used natex inputs
# Anything: '/.*/'
# Affirm: '<[#ONT(positive)]>'
# Deny: '<[#ONT(negative)]>'
#######################################################################################
# CLASSES

class game_catcher(Macro):
    def run(self, ngrams, vars, args):
        global catch_flag
        return_dialogue = ""
        temp = vars['inquiry']
        high_r = -1
        for j in genG:
            for i in ontology["ontology"][j]:
                if 100 > fuzz.ratio(i, temp) > 50:
                    if fuzz.ratio(i, temp) > high_r:
                        high_r = fuzz.ratio(i, temp)
                        return_dialogue += "i didnt quite catch that! did you mean " + i + "?"
                        if j == "specificGame":
                            vars['specG'] = i
                            catch_flag = 1
                        else:
                            vars['generalG'] = i
                            catch_flag = 0
                        return return_dialogue
        return "i have not heard of that game before. what genre is it?"
class game_catcher_parttwo(Macro):
    def run(self, ngrams, vars, args):
        if catch_flag == 1:
            talked.append(vars['specG'])
            return "would you like to talk about " + vars['specG'] + "? i know a lot about the game!"
        else:
            return "oh! ive heard of " + vars['generalG'] + ". what are your thoughts on it?"
class metaComp(Macro):
    def run(self, ngrams, vars, args) -> str:

         if len(vars['company']) > 0:
            c = vars['company']

            #make sure name is uniform
            playstation = ["ps", "sony"]
            fromsoftware = ["fromsoft","from software","from soft","dark souls"]
            riotgames = ["riot games","riot"],
            blizzard = ["blizard", "activision"]
            rockstar_games = ["rockstar", "rock star"]

            if c in playstation:
                c = 'playstation'
            elif c in fromsoftware:
                c = 'fromsoftware'
            elif c in riotgames:
                c = 'riotgames'
            elif c in blizzard:
                c = 'blizzard'
            elif c in rockstar_games:
                c = 'rockstar games'


            #return s
            opinion = comp_Dict.get(c)

            return opinion + " as the industry grows as a whole, i know there is much debate over whether video games should be viewed as art, or merely entertainement. what do you think about video games as an art form?"
############################################################
#############################################################
#global list so that there is no repeat in conversation topic
genG = ["specificGame", "generalGame", "horror_games", "shooters_games","adventure_games", "racing_games", "rpg_games", "real-time strategy_games","party_games","roguelike_games", "survival_games","tbt_games", "tbs_games", "platformer_games", "beat-em-up_games","stealth_games", "rhythm_games", "metroidvania_games", "visual novels_games", "role-playing games_games", "tactical rpg_games", "sandbox rpg_game", "tower defense_games", "puzzle_games", "idle_games",  "casual_games", "educational_games"]
talked = []
not_talked = ontology["ontology"]["specificGame"].copy()
# if catch_flag is 0 -> genGame, if catch_flag is 1 -> specific Game
catch_flag = -1 # default flag is 0 because default flag of -1 crashes program
############################################################


knowledge = KnowledgeBase()
knowledge.load_json(ontology)
df = DialogueFlow(State.S0, initial_speaker=DialogueFlow.Speaker.SYSTEM, kb=knowledge,
                  macros={"syn_det":syn_det(), "fave_games":fave_games(), "SPECIFIC1a": SPECIFIC1a(),
                          "SPECIFIC2a": SPECIFIC2a(), "SPECIFIC2b": SPECIFIC2b(),"SPECIFIC3a":SPECIFIC3a(),
                          "SPECIFIC3b": SPECIFIC3b(), "GENRE_OPINION": GENRE_OPINION(), "GENRE_RECOMMENDER": GENRE_RECOMMENDER(),
                          "like_macro": like_macro(), "dislike_macro":dislike_macro(), "game_desc":game_desc(),
                         "game_catcher":game_catcher(), "game_catcher_parttwo":game_catcher_parttwo(), "list_items_one":list_items_one(),
                         "list_items_two":list_items_two(), "explain_response":explain_response(), "genre_pivot":genre_pivot(),
                          "genre_pivot_learning": genre_pivot_learning(),"list_items_two":list_items_two(), "explain_response":explain_response(), "genre_pivot":genre_pivot(),
                         "metaComp":metaComp()})

### Main Prompt - Do you play video games?
df.add_system_transition(State.S0, State.gU0, '"Do you play video games?" $empty=""')
df.add_user_transition(State.gU0, State.gS1d, '[$word=#ONT(dislike), $dislike=/.*/]')
df.add_user_transition(State.gU0, State.gS1a, '[#ONT(positive)]', score = 2.0) 
df.add_user_transition(State.gU0, State.gS1b, '{[#ONT(negative), -#ONT(positive)], dontknow}', score=3.0)
df.add_user_transition(State.gU0, State.gS1c, '[[$word=#ONT(like), $like=/.*/], -#ONT(positive)]')
df.add_user_transition(State.gU0, State.fS1b, general, score = 3.0)
df.add_user_transition(State.gU0, State.fS1d, '[{$specG=#ONT(specificGame)}]', score=3.0)
df.set_error_successor(State.gU0, State.mS0)


### Negative Response
df.add_system_transition(State.gS1b, State.gU1aa, '"video games are great, and there are games for everyone. in general would you prefer a game you can play by yourself, or with others?"')
df.add_system_transition(State.gS1c, State.gU1ac, '"why do you" $word #like_macro')
df.add_system_transition(State.gS1d, State.gU1ad, '"why do you" $word #dislike_macro')
df.add_user_transition(State.gU1ac, State.fS1d, '[{$specG=#ONT(specificGame)}]')
df.add_user_transition(State.gU1ac, State.gS2d, '[-{$specG=#ONT(specificGame)} $explain=/.*/]') # continues from why do you like

df.add_user_transition(State.gU1ad, State.gS2d, '$explain=/.*/') # continues from why do you dislike
df.add_user_transition(State.gU2d, State.gS1b, '/.*/') 

#TODO: expand accepted phrases
df.add_user_transition(State.gU1aa, State.gS2a,"[{$response=#ONT(alone)}]") # alone
df.add_user_transition(State.gU1aa, State.gS2b, "[{$response=#ONT(team)}]") # with others
df.set_error_successor(State.gU1aa, State.gS2c)

df.add_system_transition(State.gS2a, State.gU2a, '"there are a lot of fun games for people that are more introverted. i highly recommend the" $specG=pokemon "franchise! would you be interested in them?"')
df.add_system_transition(State.gS2b, State.gU2b, '"thats awesome! being with people is great and games are a great way to be more sociable. i highly recommend the" $specG=mario kart "games! would you be interested in them?"')

df.add_user_transition(State.gU2a, State.g5a, '[{#ONT(positive)}]')
df.add_user_transition(State.gU2b, State.g5a, '[{#ONT(positive)}]')
df.add_user_transition(State.gU2a, State.fS1aa, '<{what}>')
df.add_user_transition(State.gU2b, State.fS1aa, '<{what}>')
df.set_error_successor(State.gU2b, State.g5b)
df.set_error_successor(State.gU2a, State.g5b)
df.add_user_transition(State.gU2a, State.g5b, '[{#ONT(negative)}]')
df.add_user_transition(State.gU2b, State.g5b, '[{#ONT(negative)}]')


#reccomended negative -> meta
df.add_system_transition(State.g5b, State.mU0, '"i will brainstorm more games for you! in the mean time, what do you see for the future of gaming?"')


#reccomended positive -> meta
df.add_system_transition(State.g5a, State.mU0, '"i look forward to talking to you about the " $specG " franchise in the future! in the mean time, what do you see for the future of gaming?"')


#reccomended postive, how about you -> fave games
df.add_system_transition(State.g5c, State.fU0, '"i look forward to talking to you about the " $specG " franchise in the future! now tell me about about some of the games you like!"')




# conversation about how great games are for social growth
# SOCIAL MODULE
df.add_system_transition(State.sS1a, State.sU1a, '$genre "games are pretty great for building social skills and cognitive development, and kids should play more" $genre "games. do you think kids should play more games?"')
df.add_system_transition(State.sS1aA, State.sU1a, '"games can discuss a wide range of stories, and allow their users to build social skills. do you think kids should play more games?"')
df.add_user_transition(State.sU1a, State.sS2a, '[{#ONT(agree), #ONT(positive), #ONT(like)}]') # contains the words agree, social?
df.add_user_transition(State.sU1a, State.sS2b, '[{#ONT(disagree), #ONT(negative), #ONT(dislike)}]') # contains negative words, disagree, antisocial
df.add_user_transition(State.sU1a, State.hS0, '[{#ONT(metaHealth), #ONT(healthExercise), #ONT(healthBreaks)}]', score = 2.0)
df.set_error_successor(State.sU1a, State.hS0)

df.add_system_transition(State.sS2a, State.sU2a, '"can you expand on your perspective?"')
df.add_system_transition(State.sS2b, State.sU2b, '"can you elaborate on what you mean by that?"')
df.add_user_transition(State.sU2a, State.sS3a, '[{$pos_word=#ONT(positive_con)}]', score = 3.0)
df.add_user_transition(State.sU2b, State.sS3b, '[{$neg_word=#ONT(negative_con)}]', score = 3.0)
df.set_error_successor(State.sU2b, State.hS0)

df.add_system_transition(State.sS3a, State.hU0, '"im glad you think games help people be "$pos_word "! but its also important to stay healthy while gaming. how should people practice healthy gaming?"')
df.add_system_transition(State.sS3b, State.hU0, '"i agree that sometimes games can make people " $neg_word ". health is another issue. how do you think people can practice healthy gaming? "')

df.add_system_transition(State.hS0, State.hU0, '"thats an interesting opinion! i like to stay healthy as i game. what are ways you think people can practice healthy gaming?"') #Could open the conversation for the user to either continue this conversation on healthy gaming or go to another conversation. Doesn't come off as preachy, just as a personal preference. The user could ask the bot to elaborate.

df.add_user_transition(State.hU0, State.hS1a, '"[{how, you, your}, -#ONT("healthExcersise")]"') #If the user asks for the elaborate on how the bot likes to stay healthy as it games -- how
df.add_user_transition(State.hU0, State.hS1b, '"[{what, why, who}, -#ONT("healthExcersise")]"') #If the user asks for the elaborate on how the bot likes to stay healthy as it games -- why
df.add_user_transition(State.hU0, State.hS1c, '"[#ONT("healthExcersise"]"') #excersise
df.add_user_transition(State.hU0, State.hS1d, '"[#ONT("healthBreaks"]"') #breaks
df.set_error_successor(State.hU0, State.hS1a)


df.add_system_transition(State.hS1a, State.hU1a, '"i practice healthy gaming by taking breaks and going on walks! do you have any other ideas about what i can do?"') #Could open the conversation for the user to either continue this conversation on healthy gaming or go to another conversation. Doesn't come off as preachy, just as a personal preference. The user could ask the bot to elaborate.
df.add_user_transition(State.hU1a, State.hS1c, '"[#ONT("healthExcersise"]"') #excersise
df.add_user_transition(State.hU1a, State.hS1d, '"[#ONT("healthBreaks"]"') #breaks
df.set_error_successor(State.hU1a, State.hS1c)


df.add_system_transition(State.hS1b, State.hU1b, '"i think healthy gaming is important because before, i noticed i took less care of myself while playing another game. what do you think i can do?"') #Could open the conversation for the user to either continue this conversation on healthy gaming or go to another conversation. Doesn't come off as preachy, just as a personal preference. The user could ask the bot to elaborate.
df.add_user_transition(State.hU1b, State.hS1c, '"[#ONT("healthExcersise"]"') #excersise
df.add_user_transition(State.hU1b, State.hS1d, '"[#ONT("healthBreaks"]"') #breaks
df.set_error_successor(State.hU1b, State.hS1c)


df.add_system_transition(State.hS1c, State.hU1c, '"exercise can be a great way to stay healthy! thank you helping me brainstorm!"')
df.set_error_successor(State.hU1c, State.hS2END) #transition to end


df.add_system_transition(State.hS1d, State.hU1d, '"taking breaks can be a great way to stay healthy! thank you helping me brainstorm!"')
df.set_error_successor(State.hU1d, State.hS2END) #transition to end

df.add_system_transition(State.hS2END, State.hS2END, '"thank you for talking to me about video games! hope to talk to you again soon!"')

#end social
df.add_system_transition(State.gS2c, State.gU2c, '"there are many great stories in games! are there maybe particular types of stories you enjoy like horror or adventure stories?"' )
df.add_system_transition(State.gS2d, State.gU2c, '[!#explain_response "are there maybe particular types of stories you enjoy like horror or adventure stories?"]')
df.add_user_transition(State.gU2c, State.gS3aa, "[{$genre=#ONT(genre)}]", score = 2.0)
df.add_user_transition(State.gU2c, State.gS3ab, dontknow)
df.add_system_transition(State.gS3ab, State.gU3b, '"it doesnt seem like you know much. tell me what you know about video games"')
df.add_user_transition(State.gU3b, State.gS3b, '/.*/')
df.add_system_transition(State.gS3b, State.endGen, '"i have nothing to say to you. goodbye"')
df.set_error_successor(State.gU2c, State.sS1aA)

df.add_system_transition(State.gS3aa, State.gU3a, '[!#GENRE_OPINION]')
df.add_user_transition(State.gU3a, State.gS4b, affirm)
df.add_system_transition(State.gS4b, State.gU4a, '[!#GENRE_RECOMMENDER]')
df.add_user_transition(State.gU4a, State.fS1d, affirm)
df.add_user_transition(State.gU3a, State.gS4a, '[{#ONT(question)}]')
df.set_error_successor(State.gU4a, State.gS3c)
df.set_error_successor(State.gU3a, State.gS3c)
df.add_system_transition(State.gS3c, State.endGen, '"thanks for the conversation! goodbye."')


### Positive Response
df.add_system_transition(State.gS1a, State.fU0, '"I like to game in my free time, too. What\'s your favorite game?"') #at this point, go for genre, game name detection, or i dont have one

#Catching unknown games or typos
df.add_system_transition(State.fS1a, State.fU1d, '[!#game_catcher]')
df.add_user_transition(State.fU1d, State.fS2da, '[{#ONT(agree)}]', score = 3.0) # caught the yes
df.add_user_transition(State.fU1d, State.fS1b, general, score = 3.0) # caught a game that is general
df.add_user_transition(State.fU1d, State.fS1d, '[$specG=#ONT(specificGame)]', score=3.0) # caught a game that is specific
df.add_user_transition(State.fU1d, State.fS2db, '[#ONT(negative)]', score=3.0) # go to game learning module
df.add_user_transition(State.fU1d, State.LS1a, '[<$learned_genre=#ONT(genre), -#ONT(genreSpec)>]')
df.add_user_transition(State.fU1d, State.LS1b, '[$genre=#ONT(genreSpec)]', score = 2.0)
df.set_error_successor(State.fU1d, State.fS2dc)
df.add_system_transition(State.fS2da, State.fU2da, '[!#game_catcher_parttwo]')
df.add_user_transition(State.fU2da, State.fS1ba, '$input=/.*/')
df.add_user_transition(State.fU2da, State.fS1d, affirm, score = 2.0)
df.add_user_transition(State.fU2da, State.fS2dc, deny, score = 2.0)
df.add_system_transition(State.fS2dc, State.fU2a, '[!#fave_games]')

# df.add_system_transition(State.fS2da, State.fU2db, )
# df.add_user_transition()


#### Favorite Gaming Conversation
df.add_user_transition(State.fU0, State.fS1a, '[!-{#ONT(specificGame), #ONT(largeGameList)} $inquiry=/.*/]')
df.add_user_transition(State.fU0, State.fS1d, '[{$specG=#ONT(specificGame)}]', score=3.0) # If the user talks about a game we know about
df.add_user_transition(State.fU0, State.fS1b,  general, score=2.0) # If the user has a specific game they like but it's not something we know a lot about
df.add_user_transition(State.fU0, State.fS1c, dontknow, score = 1.5)
df.set_error_successor(State.fU0, State.fS1c) # If user answers anything not in general game or specific game list

# sub dialogue
df.add_system_transition(State.fS1b, State.fU2aa, '"oh! ive heard of "$generalG", but i have never played it. how would you describe the game?"')

### new stuff for flow diagram maybe
df.add_user_transition(State.fU2aa, State.fS1ba, '$input=/.*/')
df.add_system_transition(State.fS1ba, State.fU2ac, '[!#syn_det()]')
df.add_user_transition(State.fU2ac, State.fS1bb, '/.*/')
###

# Learning module
df.add_system_transition(State.fS2db, State.LU1a, '"ive never heard of that game before. what is the genre?"')

df.add_user_transition(State.LU1a, State.LS1a, '[<$learned_genre=#ONT(genre), -#ONT(genreSpec)>]')

df.add_user_transition(State.LU1a, State.LS1b, '[$genre=#ONT(genreSpec)]')
df.set_error_successor(State.LU1a, State.LS2aa)

df.add_system_transition(State.LS2aa, State.LU2a, '"i never knew that was a genre. is that game single-player or multiplayer?"')
df.add_system_transition(State.LS1a, State.LU2a, '$learned_genre eh "? is it single-player or multiplayer?"')
df.add_user_transition(State.LU2a, State.LS2a, r"$learned_type=[{#ONT(alone), #ONT(team)}]")
df.set_error_successor(State.LU2a, State.LS3aa)
df.add_system_transition(State.LS2a, State.mU0, '"thank you for telling me about this game! in general, what do you see for the future of gaming?"')
df.add_system_transition(State.LS3aa, State.mU0, '"thank you for telling me about this game! what do you see for the future of gaming?"')



df.add_system_transition(State.LS1b, State.fU5a, '[!#genre_pivot_learning]')
# Continuation'[! $familiar " huh?" #char_macro($familiar)]'
df.add_system_transition(State.fS1bb, State.fU2a, '[!"thats really interesting."#fave_games]')
df.add_system_transition (State.fS1c, State.fU2a, '[!#fave_games]')
df.add_system_transition(State.fS1d, State.fU2b, '[!#SPECIFIC1a]') #initializing ans1 for later use

# Specific
df.add_user_transition(State.fU2b, State.fS2ba, '[{$ans1=#ONT(specAnswer1), $ans_not1=#ONT(specAnswer2)}]') #Specific # answer not = for all coverage of misidentifying a game
df.add_user_transition(State.fU2b, State.fS2bc, '[{what, show, who, example, examples}, -#ONT(specAnswer1)]')
df.set_error_successor(State.fU2b, State.fS2bb)
df.add_system_transition(State.fS2bc, State.fU2b, '[!#list_items_one]')

# General
affirm = r"[{#ONT(positive), #ONT(agree), #ONT(like), #ONT(interested)}]"
df.add_system_transition(State.fS2ab, State.fU2a, '[!#fave_games]') # this loops from negative
df.add_system_transition(State.fS1aa, State.fU2a, '[!#game_desc]') #TODO: link this back somewhere else this shoulw be  going somewhere else?

df.add_user_transition(State.fU2a, State.fS2ab, '[<{#ONT(negative)},#EQ($switch3,false)>]', score =1.5) #negative
df.add_user_transition(State.fU2a, State.fS1d, '[<{#ONT(positive), #ONT(agree), #ONT(like), #ONT(interested)}, #EQ($switch3,false)>]') #affirmative; this starts the conversation about specific games
df.add_user_transition(State.fU2a, State.fS1aa, '<{what is}, #EQ($switch3,false)>')


df.add_user_transition(State.fU2a, State.sS1a, '<[$genre=#ONT(genre)], #EQ($switch3,true)>', score=2.0)
df.set_error_successor(State.fU2a, State.sS1aA) #TODO: change this later
#df.set_error_successor(State.fU2a, State.fS2bb)


# specific game conversation
df.add_system_transition(State.fS2bb, State.fU3b, '[!#SPECIFIC2b]')
df.add_system_transition(State.fS2ba, State.fU3b, '[!#SPECIFIC2a]') #type / champion or something #initializing ans2 for later use

df.add_user_transition(State.fU3b, State.fS3bd, '[{$ans2=#ONT(specAnswer2), $ans_not2=#ONT(specAnswer1)}]')
df.add_user_transition(State.fU3b, State.fS3bc, '[<$temp=#ONT(positive), #EQ($switch,true)>]') #ooo
df.add_user_transition(State.fU3b, State.fS3ba, '[{what, show, who, example, examples}, -#ONT(specAnswer2)]') # asking for a list of the item we asked about
df.set_error_successor(State.fU3b, State.fS3bb)

df.add_system_transition(State.fS3ba, State.fU3b, '[!#list_items_two]')
df.add_system_transition(State.fS3bc, State.fU2b, '$specG=$switch_game $ans1=$empty $ans2=$empty "is fun too." [!#SPECIFIC1a]') # if the user decides to switch game topics

df.add_system_transition(State.fS3bb, State.fU4a, r'[!#SPECIFIC3b]')
df.add_system_transition(State.fS3bd, State.fU4b, r'[!#SPECIFIC3a]')

df.add_user_transition(State.fU4b, State.fS4bc, '[<$temp=#ONT(positive), #EQ($switch,true)>]') #ooo
df.add_system_transition(State.fS4bc, State.fU2b, '$specG=$switch_game $ans1=$empty $ans2=$empty "is also cool." [!#SPECIFIC1a]')

df.add_user_transition(State.fU4a, State.mS0, '[{#ONT(genreOpinions)}]')
df.add_user_transition(State.fU4b, State.mS0, '[{#ONT(genreOpinions)}]')
df.set_error_successor(State.fU4a, State.fS4a)
df.set_error_successor(State.fU4b, State.fS4a)

df.add_system_transition(State.fS4a, State.fU5a, '[!#genre_pivot]')
df.add_user_transition(State.fU5a, State.fS1d, affirm)
df.add_user_transition(State.fU5a, State.fS2ab, deny)
df.set_error_successor(State.fU5a, State.fS2ab)


##### meta module insertion
df.add_system_transition(State.mS0, State.mU0, '"video games have so much to offer from visual storylines to character arcs and from challenges to mediums of social interaction. what do you see for the future of gaming?"')
df.add_user_transition(State.mU0, State.mS1a, '[#ONT(metaArt)]')
df.add_user_transition(State.mU0, State.mS1b, '[#ONT(metaVR)]')
df.add_user_transition(State.mU0, State.mS1c, '[#ONT(metaBus)]')
df.set_error_successor(State.mU0, State.mS1d)
#BOOKMARK

###ART CONVERSATION ##########
df.add_system_transition(State.mS1a, State.mU1a, '"video game graphics are getting more advanced, as designers render more and more creative images. what do you think about video games as an art form?"')
df.add_user_transition(State.mU1a, State.mS1aa, '[#ONT(positive)]')#yes/like
df.add_user_transition(State.mU1a, State.mS1ab, '[#ONT(negative)]')#no/dislike
df.set_error_successor(State.mU1a, State.mS1ac) #error



##Yes
# if the user has not done speific game module
#df.add_system_transition( State.mS1aa, State.fS1a, '"I think so too! what are some of your favorite story driven video games?"')
#else
df.add_system_transition( State.mS1aa, State.mU1d, '"I think so too! unfortunately, although more than a billion people play video games worldwide, many people view video games as a negative pastime. why do you think people feel this way?"')



## no
# if the user has not done speific game module
#df.add_system_transition( State.mS1ab, State.fS1a, '"I entirely disagree! what are some of your favorite story driven video games?"')
#else
df.add_system_transition( State.mS1ab, State.mU1d, '"I entirely disagree! unfortunately, although more than a billion people playing video games world wide, many people view video games as a negative pastime. why do you  think people feel this way?"')

## error
# if the user has not done speific game module
#df.add_system_transition( State.mS1ac, State.fS1a, '"the artistic merit of video games is often questioned. what are some of your favorite story driven video games?"')
#else
df.add_system_transition( State.mS1ac, State.mU1d, '"the artistic merit of video games is often questioned. why do you think people view video games as a negative pastime?"')



###VR Conversation ####
df.add_system_transition(State.mS1b, State.mU1b, '"virtual reality is gaining traction right now! what do you think about virtual reality?"')
df.add_user_transition(State.mU1b, State.mS1ba, '[#ONT(positive)]')#yes/like
df.add_user_transition(State.mU1b, State.mS1bb, '[#ONT(negative)]')#no/dislike
df.set_error_successor(State.mU1b, State.mS1bb)



#to do: oooo
##Yes
# if the user has not done speific game module
#df.add_system_transition( State.mS1ba, State.fS1a, '"I think so too! what are some of your favorite story driven video games?"')
#else
df.add_system_transition( State.mS1ba, State.mU1c, '"virtual reality offers a beautiful addition to the video gaming world.  unfortunately there is a large stigma around video games. why do you think people feel this way?"')


## no
# if the user has not done speific game module
#df.add_system_transition( State.mS1bb, State.fS1a, '"I entirely disagree! what are some of your favorite story driven video games?"')
#else
df.add_system_transition( State.mS1bb, State.mU1d, '"virtual reality is a growing presence in gaming for sure. unfortunately there is a large stigma around video games. why do you think people feel this way?"')




###INDUSTRY CONVERSATION ####
df.add_system_transition(State.mS1c, State.mU1c, '"the video game industry has grown tremendously in the past decade, however some people speculate that the success of these companies will not last. what video game companies do you think will endure?"')
df.add_user_transition(State.mU1c, State.mS1ca, '[$company=#ONT(metaComp)]')#catch from ontology
df.set_error_successor(State.mU1c, State.mS1cc)


##Yes
# if the user has not done speific game module
# df.add_system_transition( State.mS1ca, State.fS1a, '"#Metacomp what are some of your favorite games from $company?"')
#else
df.add_system_transition( State.mS1ca, State.mU1a, '[!#metaComp]')


## error
# if the user has not done speific game module
# df.add_system_transition( State.mS1cc, State.fS1a, 'it is hard to say what the industry will look like in the near future considering how much it has grown in the past fifteen years. what games would you say helped fuel that growth?"')
#else
df.add_system_transition( State.mS1cc, State.mS1a, '"it is hard to say what the industry will look like in the near future considering it grew a lot. what do you think about video games as an art form?"')


###### stigma #######


df.add_system_transition(State.mS1d, State.mU1d, '"there seems to be a lot of stigma surrounding video games. what do you think are the reasons people look down on playing video games?"')
df.add_user_transition(State.mU1d, State.mS1da, '[#ONT(metaEntertainment)]')# entertainmentMeta
df.add_user_transition(State.mU1d, State.mS1db, '[#ONT(metaHealth)]') #healthMeta
df.set_error_successor(State.mU1d, State.mS1db) #error




##entertainment
df.add_system_transition( State.mS1da, State.mU2d, '"thats true theyre a source of entertainment, but there are a lot of parallels that video games and sports share. do you think its unfair for the two to be seen as equals?"')
df.add_user_transition(State.mU2d, State.mS2da, '[#ONT(positive)]')#yes
df.add_user_transition(State.mU2d, State.mS2db, '[#ONT(negative)]')#no
df.set_error_successor(State.mU2d, State.mS2dc)

#no
df.add_system_transition( State.mS2da, State.hU0, '"i agree! however it is important to practice healthy gaming! what are ways do you think people can practice healthy gaming?"')



#yes
df.add_system_transition( State.mS2db, State.hU0, '"i disagree. video games can foster a lot of great skills similar to sports. in both sports and video games however, it is important to stay healthy. what are ways you can practice healthy gaming?"')

#error
df.add_system_transition( State.mS2dc, State.hU0, '"regardless of whether you play sports or video games, youve got to take care of yourself. what are ways do you think people can practice healthy gaming?"')


## healthy gaming
# transition into healthy gaming module
df.add_system_transition( State.mS1db, State.hU0, '"video games are often seen as unhealthy-it can lead to a lot of bad habits that all culminate to not taking care of yourself. what are ways do you think people can practice healthy gaming?"')




df.add_system_transition(State.ERR, State.ERR, '"ERROR"')

## end meta insertion

#Future Module Ends
df.add_system_transition(State.endSpecGame, State.END, "Future Spec Games Module") #this exists
df.add_system_transition(State.endGen, State.END, "Future General Module") #this exists

if __name__ == '__main__':
    df.run(debugging=False)
