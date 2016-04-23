select 
		BrandNameActiveIngredients.BrandName,
	from BrandNameActiveIngredients, DrugbankIngredients
	where 
		BrandNameActiveIngredients.ActiveIngredientCode = DrugbankIngredients.ActiveIngredientCode
	and 
		DrugbankIngredients.ActiveIngredientName = {active_ingredient}


