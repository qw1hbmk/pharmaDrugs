select
    DrugProduct.BrandName,
    DrugbankIngredients.IngredientName,
    ActiveIngredients.Strength,
    ActiveIngredients.StrengthUnit,
    group_concat(DrugbankCategories.CategoryName, '; ') as Categories
  from DrugbankCategories, DrugbankIngredientsCategories, DrugbankIngredients, ActiveIngredients, DrugProduct
  where
        DrugProduct.DrugCode = ActiveIngredients.DrugCode
      and
        ActiveIngredients.ActiveIngredientCode = DrugbankIngredients.ActiveIngredientCode
      and
        DrugbankIngredients.ActiveIngredientCode = DrugbankIngredientsCategories.ActiveIngredientCode
      and 
        DrugbankIngredientsCategories.CategoryID = DrugbankCategories.CategoryID
      and ({brand_names_ored})
  group by
    DrugbankIngredients.IngredientName, DrugProduct.BrandName

