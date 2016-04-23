select
    BrandNameActiveIngredients.BrandName,
    DrugbankIngredients.IngredientName,
    group_concat(DrugbankFoodInteractions.FoodInteractionDescription, ' ') as FoodInteractionDescriptions
  from DrugbankFoodInteractions, DrugbankIngredientsFoodInteractions, DrugbankIngredients, BrandNameActiveIngredients
  where
      BrandNameActiveIngredients.ActiveIngredientCode = DrugbankIngredients.ActiveIngredientCode
    and
      DrugbankIngredients.ActiveIngredientCode = DrugbankIngredientsFoodInteractions.ActiveIngredientCode
    and 
      DrugbankIngredientsFoodInteractions.FoodInteractionID = DrugbankFoodInteractions.FoodInteractionID
    and ({brand_names_ored})
  group by
    DrugbankIngredients.IngredientName,
    BrandNameActiveIngredients.BrandName
