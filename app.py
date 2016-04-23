#!/usr/bin/env python3
import sqlite3
from flask import Flask, render_template, g, request
from pprint import pprint
from time import time
import fuzzyLev as fuzzy

with open('ingredients-conflicts.sql') as f:
	ingredient_conflicts = f.read()

with open('food-interactions.sql') as f:
	food_interactions = f.read()

with open('drug-categories.sql') as f:
	ingredient_categories = f.read()

with open('drug-category-duplicates.sql') as f:
	drug_category_duplicates = f.read()

with open('alt-recommendations.sql') as f:
	alt_recommendations = f.read()


def connect_db():
	#connects to the specific databse
	con = sqlite3.connect('pharmaDatabase.db')
	con.row_factory = sqlite3.Row
	with open('views.sql') as f:
		script = f.read()
	with con:
		con.executescript(script)

	return con

def get_db():
	if not hasattr(g, 'db'): 
		g.db = connect_db()
	return g.db


def load_brandnames():
	db = get_db()
	with get_db() as con:
		brandnames = con.execute('SELECT BrandName FROM DrugProduct;')
		brandnames_result = [b["BrandName"].lower() for b in brandnames]
	return brandnames_result


def get_brandnames():
	if not hasattr(g,'brandnames'):
		g.brandnames = load_brandnames()
	return g.brandnames


app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/fuzz')
def fuzz():
	brandnames = (get_brandnames())
	search_name1 = request.args["drug1"].lower()
	search_name2 = request.args["drug2"].lower()
	search_name3 = request.args["drug3"].lower()
	if search_name1 != "":
		top_by_levenshtein1 = map(lambda name: (fuzzy.levenshtein(search_name1, name[:len(search_name1)]), name), brandnames)
		top_by_fuzzy_levenshtein1 = map(lambda name: (fuzzy.fuzzyLevenshtein(search_name1, name[:len(search_name1)]), name), brandnames)
		#top_by_fuzzyVowels = map(lambda name: (fuzzy.fuzzyVowels(search_name, name[:len(search_name)]), name), brandnames)
		top_levenshtein1 = (sorted(list(top_by_levenshtein1))[:6])
		top_fuzzy_levenshtein1 = (sorted(list(top_by_fuzzy_levenshtein1))[:6])
		#print(list(reversed(sorted(top_by_fuzzyVowels)))[:10])
	else:
		top_levenshtein1 = []
		top_fuzzy_levenshtein1 = []

	if search_name2 != "":
		top_by_levenshtein2 = map(lambda name: (fuzzy.levenshtein(search_name2, name[:len(search_name2)]), name), brandnames)
		top_by_fuzzy_levenshtein2 = map(lambda name: (fuzzy.fuzzyLevenshtein(search_name2, name[:len(search_name2)]), name), brandnames)
		top_levenshtein2 = (sorted(list(top_by_levenshtein2))[:6])
		top_fuzzy_levenshtein2 = (sorted(list(top_by_fuzzy_levenshtein2))[:6])
	else:
		top_levenshtein2 = []
		top_fuzzy_levenshtein2 = []

	if search_name3 != "":
		top_by_levenshtein3 = map(lambda name: (fuzzy.levenshtein(search_name3, name[:len(search_name3)]), name), brandnames)
		top_by_fuzzy_levenshtein3 = map(lambda name: (fuzzy.fuzzyLevenshtein(search_name3, name[:len(search_name3)]), name), brandnames)
		top_levenshtein3 = (sorted(list(top_by_levenshtein3))[:6])
		top_fuzzy_levenshtein3 = (sorted(list(top_by_fuzzy_levenshtein3))[:6])
	else:
		top_levenshtein3 = []
		top_fuzzy_levenshtein3 = []
		
	return render_template('fuzz.html', top_levenshtein1=top_levenshtein1, top_fuzzy_levenshtein1=top_fuzzy_levenshtein1, top_levenshtein2=top_levenshtein2, top_fuzzy_levenshtein2=top_fuzzy_levenshtein2, top_levenshtein3=top_levenshtein3, top_fuzzy_levenshtein3=top_fuzzy_levenshtein3)


#view function
@app.route('/results')
def results():
	print("got here")
	brandNames = []
	if "drug1" in request.args:
		brandNames.append(request.args["drug1"])
	if "drug2" in request.args:
		brandNames.append(request.args["drug2"])
	if "drug3" in request.args:
		brandNames.append(request.args["drug3"])
	# if "drug4" in request.args:
	# 	brandNames.append(request.args["drug4"])
	# if "drug5" in request.args:
	# 	brandNames.append(request.args["drug5"])
	conflict_brands = " or ".join(map(lambda b: 'conflict.BrandName = "{b}"'.format(b=b), brandNames))
	ingredient_brands = " or ".join(map(lambda b: 'ingredient.BrandName = "{b}"'.format(b=b), brandNames))
	brands = " or ".join(map(lambda b: 'BrandName = "{b}"'.format(b=b), brandNames))
	# BrandName = "REGULAR STRENGTH TYLENOL COLD NIGHTTIME" or BrandName = "SATIVEX"
	ingredient_conflicts_query = ingredient_conflicts.format(
		brand_names_ored_conflict=conflict_brands, brand_names_ored_ingredient=ingredient_brands)

	food_interactions_query = food_interactions.format(brand_names_ored=brands)
	ingredient_categories_query = ingredient_categories.format(brand_names_ored=brands)
	drug_category_duplicates_query = drug_category_duplicates.format(brand_names_ored=brands)
	alt_recommendations_query = alt_recommendations.format(brand_names_ored=brands)

	with get_db() as con:
		t0 = time()
		ingredient_conflicts_cursor = con.execute(ingredient_conflicts_query)
		tf = time()
		print("ingred-conf: ", tf-t0)
		ingredient_conflicts_result = ingredient_conflicts_cursor.fetchall()

		t0 = time()
		food_interactions_cursor = con.execute(food_interactions_query)
		tf = time()
		print("food interactions: ", tf-t0)
		food_interactions_result = food_interactions_cursor.fetchall()
		
		t0 = time()
		ingredient_categories_cursor = con.execute(ingredient_categories_query)
		tf = time()
		print("ingredients categories: ", tf-t0)
		ingredient_categories_result = ingredient_categories_cursor.fetchall()

		t0 = time()
		drug_category_duplicates_cursor = con.execute(drug_category_duplicates_query)
		tf = time()
		print("category duplications: ", tf-t0)
		drug_category_duplicates_result = drug_category_duplicates_cursor.fetchall()

		# t0 = time()
		# alt_recommendations_cursor = con.execute(alt_recommendations_query)
		# tf = time()
		# print("ingred-conf: ", tf-t0)
		# alt_recommendations_result = alt_recommendations_cursor.fetchall()

	return render_template('results.html', 
				ingredient_conflicts=ingredient_conflicts_result, 
				food_interactions=food_interactions_result, 
				ingredient_categories=ingredient_categories_result,
				drug_category_duplicates=drug_category_duplicates_result
	)



if __name__ == '__main__':
	app.run(debug = True)



