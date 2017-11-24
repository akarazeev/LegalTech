from flask import Flask, request
import pandas as pd
import requests
import difflib
import logging
import typing
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

app = Flask(__name__)

tgmenu = pd.read_csv('tgmenu_full.csv', sep=';')


def get_final_json(cuisine: str) -> str:
    """
    :param cuisine: e.g. "shrimps+satay"
    :return: json.dumps(dict) or returns empty json
    """

    def get_spoonacular_recipe_json(cuisine: str) -> dict:
        """
        :param cuisine: e.g. "shrimps+satay"
        """
        url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?cuisine={}".format(cuisine)
        req = requests.get(url, headers={"X-Mashape-Key": "Tim7vix60umshqwqOTZaggzpDixUp1iZUY7jsn7b2wLGarxcra",
                                         "Accept": "application/json"})
        rjson = req.json()

        logger.info('Recipe: {}'.format(rjson))

        return rjson

    def get_spoonacular_info_json(recipe_id: int) -> dict:
        url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{}/information?includeNutrition=true".format(
            recipe_id)
        req = requests.get(url, headers={"X-Mashape-Key": "Tim7vix60umshqwqOTZaggzpDixUp1iZUY7jsn7b2wLGarxcra",
                                         "Accept": "application/json"})
        rjson = req.json()
        logger.info('Nutrition info: {}'.format(rjson))

        return rjson

    def select_titles(nutrients, titles):
        """
        :param nutrients: list of dicts
        :param titles: list of strings
        """
        return list(filter(lambda x: x['title'] in titles, nutrients))

    recipe_json = get_spoonacular_recipe_json(cuisine)

    if 'results' not in recipe_json:
        return "{}"
    elif len(recipe_json['results']) == 0:
        return "{}"
    else:
        recipe = recipe_json['results'][0]
        recipe_id = recipe['id']
        recipe_title = recipe['title']

        nutrients = get_spoonacular_info_json(recipe_id)['nutrition']['nutrients']
        good_titles = ['Calories', 'Protein']
        selected = select_titles(nutrients, good_titles)

        for i in range(len(selected)):
            _ = selected[i].pop('percentOfDailyNeeds', None)
            _ = selected[i].pop('unit', None)

        final_dict = dict()
        final_dict['nutrients'] = selected
        final_dict['title'] = recipe_title
        final_dict['id'] = recipe_id

        return json.dumps(final_dict)


@app.route('/cuisine/<cuisine>', methods=['get'])
def search_recipes(cuisine):
    logger.info('Cuisine: {}'.format(cuisine))

    final_json = get_final_json(cuisine)

    return final_json


def check_ru(phrase):
    return phrase.lower() in tgmenu['name_ru_low'].values


def get_closest_rus(ru_phrase):
    closest_list = difflib.get_close_matches(ru_phrase, tgmenu['name_ru'])
    if len(closest_list) >= 1:
        return closest_list[0]
    else:
        return None


def pd_translate(ru_phrase):
    return tgmenu[tgmenu['name_ru_low'] == ru_phrase.lower()]['name_en'].values[0]


def pd_get_category(en_phrase):
    print(en_phrase)
    print(tgmenu[tgmenu['name_en_low'] == en_phrase.lower()]['category_en'].values)
    return tgmenu[tgmenu['name_en_low'] == en_phrase.lower()]['category_en'].values[0]


@app.route('/translate/<phrase>', methods=['get'])
def translate_phrase(phrase):
    logger.info('Phrase: {}'.format(phrase))
    phrase = phrase.replace('+', ' ')

    translation = None

    closest_phrase = get_closest_rus(phrase)

    if check_ru(closest_phrase):
        translation = pd_translate(closest_phrase)

    category = None

    if translation is not None:
        category = pd_get_category(translation)

    final_dict = {
        'origin': phrase,
        'translation': translation,
        'category': category
    }

    final_json = json.dumps(final_dict)

    return final_json


if __name__ == '__main__':
    # print(tgmenu.columns)
    # print(tgmenu['name_ru'])

    app.run(host='0.0.0.0', port=5001, debug=True)
