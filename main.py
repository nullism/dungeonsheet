#!/usr/bin/env python

import flask as f
import json
import time
import MySQLdb
from pymongo import MongoClient
import logging

app = f.Flask(__name__)
client = MongoClient()
db = client.dnd

def get_character(char_key):
    row = db.characters.find_one({'character_key':char_key})
    if not row:
        return None
    return row

def save_character(char_key, stats):
    db.characters.update({"character_key":char_key}, 
        {"stats":stats, "updated":time.time(), "character_key":char_key}, 
        upsert=True)


@app.route('/')
def index():
    char_key = f.session.get('character_key','')
    char_row = get_character(char_key)
    if char_row:
        f.flash("Welcome back %s"%(char_row['stats']['character_name']))
    elif len(char_key) > 3:
        f.flash("New character created for key %s!"%(char_key))
        save_character(char_key, get_defaults())

    return f.render_template('index-3.5.html', 
        character_key=char_key)

@app.route('/character', methods=['POST'])
def character_screen():

    char_key = f.request.form.get('character_key','')
    if len(char_key) < 4:
        return f.render_template('index-3.5.html')
    f.session['character_key'] = char_key
    return f.redirect(f.url_for('index'))


@app.route('/stats.json')
def stats():

    char_key = f.session.get('character_key', '')
    defaults = get_defaults()

    if len(char_key) > 3:
        row = get_character(f.session['character_key'])
        if not row:
            return json.dumps(defaults)
        if f.request.args.get('resetSkills'):
            row['stats']['skills'] = defaults['skills']
        return json.dumps(row['stats'])
    return json.dumps(defaults)
    
@app.route('/stats.json/save', methods=['POST'])
def stats_save():

    stats_json = f.request.json
    
    if not stats_json:
        f.flash('Could not get stats!')
        return json.dumps({"error":True }), 400

    char_key = f.session.get('character_key','')
    if len(char_key) < 4:
        f.flash('Invalid character key!')
        return json.dumps({"error":True}), 400

    if not stats_json.get('stats'):
        f.flash('Could not find stats JSON object')
        return json.dumps({"error":True}), 400
    save_character(char_key, json.loads(stats_json['stats']))
    return json.dumps({"error":False})

def get_defaults():

    defaults = { 
        "character_name":"Your name",
        "age":25,
        "level":1,
        "speed":6,
        "exp":0,
        "base_attack_bonus":0,
        "size":"Medium",
        "gender":"Male",
        "eyes":"",
        "hair":"",
        "skin":"",
        "money":{
            "gold":0,
            "silver":0,
            "copper":0,
        },

        "hp": 15,
        "initiative_mod": 0,
        "size_ac_mod": 0,
        "natural_armor": 0,
        "armor_bonus": 0,
        "shield_bonus": 0,
        "deflection_mod": 0,
        "misc_ac_mod": 0,      
        "nonlethal_damage": 0,
        "damage_reduction": 0, 

        # Grapple
        "grapple": { 
            "size_mod":0,
            "misc_mod":0,
        },

        # Saving throws
        "base_fort_save": 0,
        "magic_fort_mod": 0,
        "misc_fort_mod": 0,
 
        "base_ref_save": 0,
        "magic_ref_mod": 0,
        "misc_ref_mod": 0,

        "base_will_save": 0,
        "magic_will_mod": 0,
        "misc_will_mod": 0,

        "arcane_spell_failure": 0,
        "spell_save": 0,
        "conditional_modifiers": "",
        
        "abilities": [
            { "name":"STR", "value":10 }, #0
            { "name":"DEX", "value":10 }, #1
            { "name":"CON", "value":10 }, #2
            { "name":"INT", "value":10 }, #3
            { "name":"WIS", "value":10 }, #4
            { "name":"CHA", "value":10 }, #5
        ],

        "attacks": [
            { "name":"Unarmed Strike", "bonus":0, "damage":"1d3", "critical":"x2", "range":0, "type":"bludgeoning", "notes":"", "ammo":"NA"},
        ],

        "skills": [
            { "name":"Appraise", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Autohypnosis", "trained":False, "ability_index":4, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Balance", "trained":False, "ability_index":1, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":True, "notes":"" },
            { "name":"Bluff", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Climb", "trained":False, "ability_index":0, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":True, "notes":"" },
            { "name":"Concentration", "trained":False, "ability_index":2, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Craft (Misc 1)", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Craft (Misc 2)", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Craft (Misc 3)", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Decipher Script", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Diplomacy", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"Half elves get +2" },
            { "name":"Disable Device", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Disguise", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Escape Artist", "trained":False, "ability_index":1, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":True, "notes":"" },
            { "name":"Forgery", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Gather Info", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Handle Animal", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Heal", "trained":False, "ability_index":4, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Hide", "trained":False, "ability_index":1, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":True, "notes":"" },
            { "name":"Intimidate", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"I'm comin fo dat ass" },
            { "name":"Jump", "trained":False, "ability_index":0, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":True, "notes":"" },
            { "name":"Knowledge (Arcana)", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Knowledge (Arch/Eng)", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Knowledge (Dungeoneering)", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Knowledge (Geography)", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Knowledge (History)", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Knowledge (Local)", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Knowledge (Nature)", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Knowledge (Nobility)", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Knowledge (The Planes)", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Knowledge (Psionics)", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Knowledge (Religion)", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Knowledge (Misc 1)", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Knowledge (Misc 2)", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Listen", "trained":False, "ability_index":4, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Move Silently", "trained":False, "ability_index":1, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":True, "notes":"" },
            { "name":"Open Lock", "trained":False, "ability_index":1, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Perform (Act)", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Perform (Comedy)", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Perform (Dance)", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Perform (Keyboard)", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Perform (Oratory)", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"Heh Heh" },
            { "name":"Perform (String Instrument)", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Perform (Wind Instrument)", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Perform (Sing)", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Perform (Misc 1)", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Perform (Misc 2)", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Profession (Misc 1)", "trained":False, "ability_index":4, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Profession (Misc 2)", "trained":False, "ability_index":4, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Psicraft", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Ride", "trained":False, "ability_index":1, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Search", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Sense Motive", "trained":False, "ability_index":4, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Sleight of Hand", "trained":False, "ability_index":1, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":True, "notes":"" },
            { "name":"Spellcraft", "trained":False, "ability_index":3, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Spot", "trained":False, "ability_index":4, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Survival", "trained":False, "ability_index":4, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            { "name":"Swim", "trained":False, "ability_index":0, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":True, "notes":"" },
            { "name":"Tumble", "trained":False, "ability_index":1, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":True, "notes":"" },
            { "name":"Use Magic Device", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Use Psionic Device", "trained":False, "ability_index":5, "ranks":0, "misc_mod":0, "use_untrained":False, "penalty":False, "notes":"" },
            { "name":"Use Rope", "trained":False, "ability_index":1, "ranks":0, "misc_mod":0, "use_untrained":True, "penalty":False, "notes":"" },
            
        ],

        "items": [
            { "name":"", "is_worn":False, "weight":0, "ac_bonus":0, "special_properties":"", "quantity":1 },
        ],

        "feats": [
            { "name":"" },
        ],

        "languages": [
            { "name":"Common" },
        ],

        "special_abilities": [
            { "name":"" },
        ],

        "spells": [
            { "name":"", "notes":"", "level":0 },
        ],

        "spell_levels": [
            {"level":"0", "number_known":0, "save_dc":0, "per_day":0, "bonus":0},
            {"level":"1st", "number_known":0, "save_dc":0, "per_day":0, "bonus":0},
            {"level":"2nd", "number_known":0, "save_dc":0, "per_day":0, "bonus":0},
            {"level":"3rd", "number_known":0, "save_dc":0, "per_day":0, "bonus":0},
            {"level":"4th", "number_known":0, "save_dc":0, "per_day":0, "bonus":0},
            {"level":"5th", "number_known":0, "save_dc":0, "per_day":0, "bonus":0},
            {"level":"6th", "number_known":0, "save_dc":0, "per_day":0, "bonus":0},
            {"level":"7th", "number_known":0, "save_dc":0, "per_day":0, "bonus":0},
            {"level":"8th", "number_known":0, "save_dc":0, "per_day":0, "bonus":0},
            {"level":"9th", "number_known":0, "save_dc":0, "per_day":0, "bonus":0},
        ],

    }
    return defaults
