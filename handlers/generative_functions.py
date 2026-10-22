import random
from messages import msgs

# Word lists live in bot_msgs_local.py (fun commands are local-only)

def generate_woman_and_date_result():
    woman = random.choice(msgs.WOMEN_TYPES)
    result = int(random.randint(1, 4))
    man = random.choice(msgs.MAN_TYPES)
    return {
        "woman_type": woman,
        "result": result,
        "man_type": man
    }

def generate_penis_characteristics():
    length = int(random.randint(4, 25))
    left_testicle_diameter = int(random.randint(1, 10))
    right_testicle_diameter = int(random.randint(1, 10))
    hair_state = random.choice(msgs.PENIS_HAIR_TYPES)
    foreskin_condition = random.choice(msgs.FORESKIN_TYPES)
    obhvat_cm = int(random.randint(4, 25))
    return {
        "length": length,
        "left_diameter": left_testicle_diameter,
        "right_diameter": right_testicle_diameter,
        "hair": hair_state,
        "foreskin": foreskin_condition,
        "obhvat": obhvat_cm,
    }

def generate_pussy_characteristics():
    depth = int(random.randint(5, 20))
    type = random.choice(msgs.PUSSY_TYPES)
    hair_state = random.choice(msgs.PUSSY_HAIR_TYPES)
    return {
        "pussy_depth": depth,
        "pussy_type": type,
        "pussy_hair": hair_state
    }

def generate_drug_effect():
    drug = random.choice(msgs.DRUGS)
    effect = random.choice(msgs.DRUG_EFFECTS)
    return {
        "drug_type": drug,
        "drug_effect": effect,
    }

def generate_percent() -> int:
    return random.randint(1, 100)
