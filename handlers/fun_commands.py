from aiogram import Router, types
import handlers.generative_functions as gf
from aiogram.filters import Command
from messages import msgs

router = Router()

######################################################
################### FUNNY COMMANDS ###################
######## (included only when BOT_MODE=local) #########
######################################################

@router.message(Command("gay"))
async def gay_check(message: types.Message):
    percent = gf.generate_percent()
    for max_val, rank in msgs.GAY_RANKS:
        if percent <= max_val:
            await message.reply(msgs.GAY_RESPONSE.format(percent=percent, rank=rank), parse_mode='HTML')
            return


@router.message(Command("dating"))
async def dating_lottery(message: types.Message):
    data = gf.generate_woman_and_date_result()
    response = msgs.DATING_RESPONSES[data["result"]].format(woman=data["woman_type"], man=data["man_type"])
    await message.reply(response, parse_mode='HTML')

@router.message(Command("cock"))
async def cock_check(message: types.Message):
    data = gf.generate_penis_characteristics()
    left = data["left_diameter"]
    right = data["right_diameter"]
    template = msgs.COCK_RESPONSE_DIFFERENT if left != right else msgs.COCK_RESPONSE_SAME
    await message.reply(template.format(length=data["length"], hair=data["hair"], foreskin=data["foreskin"],
                                        obhvat=data["obhvat"], left=left, right=right), parse_mode='HTML')

@router.message(Command("pussy"))
async def pussy_check(message: types.Message):
    data = gf.generate_pussy_characteristics()
    depth = data["pussy_depth"]
    result = msgs.PUSSY_RESPONSE.format(type=data["pussy_type"], hair=data["pussy_hair"], depth=depth)
    if depth >= msgs.PUSSY_DEEP_THRESHOLD:
        result += msgs.PUSSY_DEEP_SUFFIX
    await message.reply(result)

@router.message(Command("drug"))
async def drug_lottery(message: types.Message):
    data = gf.generate_drug_effect()
    response = msgs.DRUG_RESPONSE.format(drug=data["drug_type"], effect=data["drug_effect"])
    await message.reply(response, parse_mode='HTML')
