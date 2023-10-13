from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from re_edge_gpt import Chatbot, ConversationStyle
from pandas import DataFrame, read_excel
from tqdm import tqdm
""" from asyncio import get_event_loop """
from json import loads, dump, load
from re import sub
from time import time
from inspect import currentframe
from string import punctuation
from selenium.common.exceptions import NoSuchElementException

tillnow = 0
buildingname = ''
bot = False

# Load data from a JSON file


def load_data():
    try:
        with open('preferences.json', 'r') as file:
            data = load(file)
    except FileNotFoundError:
        data = {'tillnow': 0}
        save_data(data)
    return data

# Save data to the JSON file


def save_data(data):
    with open('preferences.json', 'w') as file:
        dump(data, file)

# Get a value from preferences


def get_preference(key, default=None):
    data = load_data()
    return data.get(key, default)

# Set a value in preferences


def set_preference(key, value):
    data = load_data()
    data[key] = value
    save_data(data)


def norm_text(inp: str):
    translator = str.maketrans('', '', punctuation)
    return ' '.join(inp.translate(translator).split())


def rm_wp_comma(string: str):
    return string.replace(" ", "").replace(",", "")


async def initgpt():
    command = f"""Please use the provided web links that I would share with you. I'm facing a tight
    deadline for tomorrow, so manually verifying all the links is impossible. These links are related to
    various portals or posts about a single building. Your response should consist of only the
    apartment or building name, strictly adhering to this format: "name:?" if it's available in
    at least one of the links. Please aim for the utmost accuracy and only provide me with the
    apartment name and use the specified response format throughout our conversation."""
    bot = await Chatbot.create(cookies=loads(open("cookie.json", encoding="utf-8").read()))
    await bot.ask(prompt=command, conversation_style=ConversationStyle.precise, simplify_response=True)
    return bot


async def get_buildingname(links: list):
    global buildingname
    global bot
    if not bot:
        bot = await initgpt()
    cmd = ''
    for link in links:
        cmd += f'"{link}", '
    answer = await bot.ask(prompt=cmd, conversation_style=ConversationStyle.balanced, simplify_response=True, locale='en-us')
    answer = answer['text']
    answer = answer[answer.find('is')+2:]
    buildingname = sub(r'[^a-zA-Z ]', '', answer[:answer.find('.')]).strip()


def Bot(data, driver, count=None, beg=None):
    global tillnow
    tillnow = get_preference('tillnow')
    print(f'till now {tillnow}')

    if not count:
        count = len(addresses)
    if not beg:
        beg = tillnow
        count += tillnow
    else:
        count += beg
    print(f'from {beg} to {count}')
    data= data[beg:count]
    addresses = data['COMPLEX_ADDRESS']
    validated_df = {'Comments': [], 'URL': [],
                    'Apartment_Availibility': [], 'Apartment_Alternate_Address': [], 'COMPLEX_NAME': []}
    ref_address = ''
    for address in tqdm(addresses):
        ref_address = address
        quadruplet = {'validators': [], 'addresses': [], 'links': [], }
        driver.get(f'https://www.google.com/search?q={address}')
        for i in range(2, 10):
            try:
                element = WebDriverWait(driver, 7).until(EC.presence_of_element_located(
                    (By.XPATH, f'//*[@id="rso"]/div[{i}]/div/div/div[1]/div/div/span/a')))
                href = element.get_attribute("href")
                val_address = element.find_element(By.XPATH, './h3').text
                metaname = href[12:href.find('.com')]

                if len(quadruplet['validators']) != 4 and metaname in ['zillow', 'trulia', 'apartments', 'redfin'] and metaname not in quadruplet['validators']:
                    quadruplet['validators'].append(metaname)

                    val_address = val_address[:val_address.find(
                        '- ')] if '- ' in val_address else val_address

                    quadruplet['addresses'].append(val_address)
                    quadruplet['links'].append(href)
            except Exception as e:
                """ print(e) """
                continue

        """# get building name using bingGPT
        loop = get_event_loop()
        loop.run_until_complete(get_buildingname(quadruplet['links']))
        validated_df['COMPLEX_NAME'].append(buildingname) """
        validated_df['COMPLEX_NAME'].append(buildingname)

        # get building type apatrment or not
        try:
            linkind = quadruplet['validators'].index('redfin')
            link = quadruplet['links'][linkind]
            """ print(link) """
            driver.get(link)
            proptype = driver.find_element(
                By.XPATH, '//*[@id="content"]/div[11]/div[2]/div[5]/div/div/div/div[2]/div/div[1]/div').text
        except (ValueError, NoSuchElementException):
            proptype = 'NA'
        except (IndexError, Exception):
            quadruplet['links'].append('NA')

        # Normalize the reference address
        normalized_reference = norm_text(ref_address)

        # Initialize variables to track the exact and best matching addresses
        exact_match_address = None
        best_match_address = None
        best_match_word_count = 0

        # Iterate through addresses to find the exact or best matching address
        for index, address in enumerate(quadruplet['addresses']):
            normalized_address = norm_text(address)
            if normalized_address == normalized_reference:
                exact_match_address = address
                exact_match_index = index
                break
            words_in_common = len(
                set(normalized_reference.split()) & set(normalized_address.split()))
            if words_in_common > best_match_word_count:
                best_match_word_count = words_in_common
                best_match_address = address
                best_match_index = index

        if exact_match_address:
            validated_df['Apartment_Alternate_Address'].append('')
            validated_df['URL'].append(quadruplet['links'][exact_match_index])

        else:
            if best_match_address:
                validated_df['URL'].append(
                    quadruplet['links'][best_match_index])
                if rm_wp_comma(best_match_address).lower() == rm_wp_comma(ref_address).lower():
                    validated_df['Apartment_Alternate_Address'].append('')
                else:
                    validated_df['Apartment_Alternate_Address'].append(
                        best_match_address)
            else:
                validated_df['Apartment_Alternate_Address'].append(
                    ref_address)
                validated_df['URL'].append(
                    'NA')

        if 'apartment' in proptype.lower() or 'multi' in proptype.lower():
            validated_df['Apartment_Availibility'].append('YES')
            validated_df['Comments'].append('')
        else:
            validated_df['Apartment_Availibility'].append('NO')
            validated_df['Comments'].append(proptype)
        tillnow += 1

    """bot.save_conversation('output\\convo.txt')
    bot.close()"""
    """    counts = {key: len(value) for key, value in validated_df.items()}
    for key, count in counts.items():
        print(f'The key "{key}" has {count} items.') """
    return dataPostprocess(DataFrame(validated_df), data)


def dataPostprocess(validated: DataFrame, raw: DataFrame):
    print('data post processing.......')
    """ print(validated.shape)
    print(raw.shape) """
    size = validated.shape[0]
    raw = raw.fillna('')
    final = {'-': list(raw['Unnamed: 1'][:size]),
             'COMPLEX_ADDRESS': list(raw['COMPLEX_ADDRESS'][:size]),
             'UNITS_COUNT': list(raw['UNITS_COUNT'][:size]),
             'BUILDINGS_COUNT': list(raw['BUILDINGS_COUNT'][:size]),
             'Apartment_Availibility': list(validated['Apartment_Availibility'][:size]),
             'COMPLEX_NAME': list(validated['COMPLEX_NAME'][:size]),
             'URL': list(validated['URL'][:size]),
             'Apartment_Alternate_Address': list(validated['Apartment_Alternate_Address'][:size]),
             'Comments': list(validated['Comments'][:size]),
             'Verified': list(raw['Verified'][:size]),
             'Analyzed Date': list(raw['Analyzed Date'][:size]),
             }
    return DataFrame(final)


data = read_excel('input\\data.xlsx')
options = Options()
options.page_load_strategy = 'eager'
options.add_argument('--headless')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_service = ChromeService(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=chrome_service, options=options)
driver.maximize_window()

df = {}
try:
    try:
        count = int(input("How much entries want to do?\n"))
    except:
        count = None
    df = Bot(data, driver, count)
    set_preference('tillnow', tillnow)
    print('Bot process completed.')
    print('Starting to write final output......')
    df.to_excel(f'output\\final_{int(time())}.xlsx',
                sheet_name='-', index=False)
    print('Successfully finished all task 😉👍🏻')
except Exception as e:
    error_message = f"An error occurred on line {currentframe().f_lineno}: {e}"
    original_traceback = e.__traceback__
    raise e.with_traceback(original_traceback) from None
