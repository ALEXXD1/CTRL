import json
import requests
from urllib.request import urlopen
from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, MessageHandler, BaseFilter, run_async

from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler
from requests import get

def covindia(bot: Bot, update: Update):
    message = update.effective_message
    state = ''
    confirmed = 0
    deceased = 0
    recovered = 0
    state_input = ''.join([message.text.split(' ')[i] + ' ' for i in range(1, len(message.text.split(' ')))]).strip()
    if state_input:
        url_india = 'https://api.covid19india.org/data.json'
        json_url = urlopen(url_india)
        state_dict = json.loads(json_url.read())
        for sdict in state_dict['statewise']:
            if sdict['state'].lower() == state_input.lower():
                confirmed = sdict['confirmed']
                deceased = sdict['deaths']
                recovered = sdict['recovered']
                state = sdict['state']
                break
    
    if state:
        bot.send_message(
            message.chat.id,
            '`COVID-19 Tracker`\n*Number of confirmed cases in %s:* %s\n*Deceased:* %s\n*Recovered:* %s\n\n_Source:_ covid19india.org' % (state, confirmed, deceased, recovered),
            parse_mode = ParseMode.MARKDOWN,
            disable_web_page_preview = True
        )
    else:
        bot.send_message(
            message.chat.id,
            'You need to specify a valid Indian state!',
            parse_mode = ParseMode.MARKDOWN,
            disable_web_page_preview = True
        )
@run_async
def covid(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/corona '):]
    fetch = get(f'https://coronavirus-tracker-api.herokuapp.com/all')

    if fetch.status_code == 200:
        usr = fetch.json()
        data = fetch.text
        parsed = json.loads(data)
        total_confirmed_global = parsed["latest"]["confirmed"]
        total_deaths_global = parsed["latest"]["deaths"]
        total_recovered_global = parsed["latest"]["recovered"]
        active_cases_covid19 = total_confirmed_global - total_deaths_global - total_recovered_global
        reply_text = ("*COVID-19 Stats🦠:*\n"
        "Total Confirmed: `" + str(total_confirmed_global) + "`\n"
        "Total Deaths: `" + str(total_deaths_global) + "`\n"
        "Total Recovered: `" + str(total_recovered_global) +"`\n"
        "Active Cases: `"+ str(active_cases_covid19) + "`")
        message.reply_text("API is currently down")

        return

    elif fetch.status_code == 404:
        message.reply_text("API is currently down!")

__help__ = """
 - /covid: get worldwide corona status
 - /covindia <state>: Get real time COVID-19 stats for the input Indian state
"""

__mod_name__ = 'COVID-19'

COV_INDIA_HANDLER = DisableAbleCommandHandler('covindia', covindia)
COVID_HANDLER = DisableAbleCommandHandler("covid", covid)
dispatcher.add_handler(COVID_HANDLER)
dispatcher.add_handler(COV_INDIA_HANDLER)
