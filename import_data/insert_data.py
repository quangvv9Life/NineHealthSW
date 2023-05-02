import os
import psycopg2
from config import DatabaseConnection
import datetime


def add_new_line(filename):
    # Define the directory to search for text files
    # directory = r"C:\\Users\\Dell\\Downloads\\mfp"

    # Define the words to insert newlines before and after
    words = [
        "Nutrition Facts",
        "Edit <https://www.myfitnesspal.com/en/food/edit/53882013928493>",
        "Learn more<https://support.myfitnesspal.com/hc/en-us/articles/360032273292-What-does-the-check-mark-mean->",
        "Servings:",
        "Calories",
        "Total Fat",
        "Saturated",
        "Polyunsaturated",
        "Monounsaturated",
        "Trans",
        "Cholesterol",
        "Vitamin A",
        "Vitamin C",
        "Sodium",
        "Potassium",
        "Total Carbs",
        "Dietary Fiber",
        "Sugars",
        "Protein",
        "Calcium",
        "Iron",
        "*Percent Daily Values are based on a 2000 calorie diet."
    ]

    filenames = []
    filenames.append(filename)
    # for filename in os.listdir(dir_path):
    for filename in filenames:
        # Loop through all the text files in the directory
        # for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            # Read the contents of the file
            with open(os.path.join(filename), "r", encoding='utf-8') as f:
                contents = f.read()

            # Insert newlines before and after each word
            for word in words:
                contents = contents.replace(word, "\n" + word + "\n")

            # Write the modified contents back to the file
            with open(os.path.join(filename), "w", encoding='utf-8') as f:
                f.write(contents)
    return "add new file successfully"


def remove_new_line(filename):
    # directory containing text files
    # dir_path = r'c:\\Users\\Dell\\Downloads\\mfp'

    # loop through each file in dir
    filenames = []
    filenames.append(filename)
    # for filename in os.listdir(dir_path):
    for filename in filenames:
        if filename.endswith(".txt"):
            file_path = os.path.join(filename)

            # read in file
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            # remove new line
            text = text.replace('\n', '')

            # write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
    return "remove new line successfully"


def insert_to_db(filename, database):
    filename.replace('\u200b1', '')
    file_names = []
    file_names.append(filename)
    # for filename in os.listdir(dir_path):
    for file_name in file_names:
        # for file_name in os.listdir(downloads_path):
        if file_name.endswith(".txt"):
            save_path = os.path.join(file_name)

            # step 4 - find anchor row and parse information
            anchor_text = "https://support.myfitnesspal.com/hc/en-us/articles/360032273292-What-does-the-check-mark-mean-"
            parsed_info = {}

            with open(save_path, "r", encoding='utf-8') as f:
                content = f.read().replace('\u200b', '')
                lines = content.splitlines()
                # lines = f.readlines()
                for i, line in enumerate(lines):
                    if anchor_text in line:
                        parsed_info['food_id'] = 1000000
                        parsed_info['food_name'] = str(
                            lines[i - 1].strip()).lower()
                        parsed_info['food_name_search'] = None
                        parsed_info['ingredient_name'] = parsed_info['food_name']
                        parsed_info['ingredient_name_en'] = parsed_info['food_name']
                        parsed_info['ingredient_name_search'] = None
                        parsed_info['ingredient_unit_vn'] = ''.join(
                            [c for c in lines[i + 3].strip() if not c.isdigit()]).replace('gram(s)', 'g').replace('tbsp(s)', 'tbsp').replace('ml(s)', 'ml').replace('gram', 'g').replace('gr', 'g').replace('mL', 'ml')
                        parsed_info['ingredient_unit_en'] = parsed_info['ingredient_unit_vn']
                        parsed_info['serving'] = 1
                        parsed_info['quantity'] = float(
                            lines[i + 3].strip().split()[0])
                        parsed_info['calories'] = float(
                            lines[i + 5].strip().split()[0])
                        parsed_info['sodium'] = float(
                            lines[i + 23].strip().split()[0])
                        parsed_info['potassium'] = float(
                            lines[i + 25].strip().split()[0])
                        parsed_info['saturated_fat'] = float(
                            lines[i + 9].strip().split()[0])
                        parsed_info['carbohydrates'] = float(
                            lines[i + 27].strip().split()[0])
                        parsed_info['polyunsaturated_fat'] = float(
                            lines[i + 11].strip().split()[0])
                        parsed_info['fiber'] = float(
                            lines[i + 29].strip().split()[0])
                        parsed_info['fat'] = float(
                            lines[i + 7].strip().split()[0])
                        parsed_info['monounsaturated_fat'] = float(
                            lines[i + 13].strip().split()[0])
                        parsed_info['sugar'] = float(
                            lines[i + 31].strip().split()[0])
                        parsed_info['trans_fat'] = float(
                            lines[i + 15].strip().split()[0])
                        parsed_info['protein'] = float(
                            lines[i + 33].strip().split()[0])
                        parsed_info['cholesterol'] = float(
                            lines[i + 17].strip().split()[0])
                        parsed_info['vitamin_a'] = float(
                            lines[i + 19].strip().split()[0])
                        parsed_info['calcium'] = float(
                            lines[i + 35].strip().split()[0])
                        parsed_info['vitamin_c'] = float(
                            lines[i + 21].strip().split()[0])
                        parsed_info['iron'] = float(
                            lines[i + 37].strip().split()[0])
                        parsed_info['smart_points'] = round(
                            0.035 * parsed_info['calories'] + 0.275 * parsed_info['saturated_fat'] + 0.12 * parsed_info['sugar'] - 0.098 * parsed_info['protein'], 4)
                        parsed_info['food_category_id'] = None
                        parsed_info['from_source'] = 'man_py'

            # step 5 - insert into database
            db = DatabaseConnection(database)
            conn = db.connection
            cur = conn.cursor()

            # Format as string
            now = datetime.datetime.now()
            cr_date = now.strftime('%Y-%m-%d %H:%M:%S')
            query = "INSERT INTO public.fin_man_py( food_id, food_name, food_name_search, ingredient_name, ingredient_name_en, ingredient_name_search ,ingredient_unit_vn, ingredient_unit_en, serving, quantity, calories, sodium, potassium, saturated_fat, carbohydrates, polyunsaturated_fat, fiber, fat, monounsaturated_fat, sugar, trans_fat, protein, cholesterol, vitamin_a, calcium, vitamin_c, iron, smart_points, food_category_id, from_source, cr_date) VALUES ({})".format(
                ','.join([
                    str(parsed_info['food_id']),
                    "'" + parsed_info['food_name'] + "'",
                    'NULL' if parsed_info['food_name_search'] is None else parsed_info['food_name_search'],
                    "'" + parsed_info['ingredient_name'] + "'",
                    "'" +
                    parsed_info['ingredient_name_en'] + "'",
                    'NULL' if parsed_info['ingredient_name_search'] is None else parsed_info['ingredient_name_search'],
                    "'" +
                    parsed_info['ingredient_unit_vn'].replace(' ', '') + "'",
                    "'" +
                    parsed_info['ingredient_unit_en'].replace(' ', '') + "'",
                    str(parsed_info['serving']),
                    str(parsed_info['quantity']),
                    str(parsed_info['calories']),
                    str(parsed_info['sodium']),
                    str(parsed_info['potassium']),
                    str(parsed_info['saturated_fat']),
                    str(parsed_info['carbohydrates']),
                    str(parsed_info['polyunsaturated_fat']),
                    str(parsed_info['fiber']),
                    str(parsed_info['fat']),
                    str(parsed_info['monounsaturated_fat']),
                    str(parsed_info['sugar']),
                    str(parsed_info['trans_fat']),
                    str(parsed_info['protein']),
                    str(parsed_info['cholesterol']),
                    str(parsed_info['vitamin_a']),
                    str(parsed_info['calcium']),
                    str(parsed_info['vitamin_c']),
                    str(parsed_info['iron']),
                    str(parsed_info['smart_points']),
                    'NULL' if parsed_info['food_category_id'] is None else parsed_info['food_category_id'],
                    "'" + parsed_info['from_source'] + "'",
                    "'" + cr_date + "'"
                ])
            )

            # print(query)
            cur.execute(query)
            conn.commit()
            cur.close()
            conn.close()
    return "done"
