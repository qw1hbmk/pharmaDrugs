with DrugActiveIngredients as (
  select
      BrandNameActiveIngredients.BrandName,
      BrandNameActiveIngredients.ActiveIngredientCode,
      DrugbankIngredientsCategories.CategoryID
    from BrandNameActiveIngredients, DrugbankIngredientsCategories
    where 
      ({brand_names_ored})
    and
      BrandNameActiveIngredients.ActiveIngredientCode = DrugbankIngredientsCategories.ActiveIngredientCode

),

DrugDuplicateIDs as (
  select
      ingredientA.BrandName,
      ingredientA.ActiveIngredientCode,
      ingredientA.CategoryID
    from DrugActiveIngredients ingredientA
      where ingredientA.CategoryID in (
        select otherDrugIngredients.CategoryID from DrugActiveIngredients otherDrugIngredients
          where otherDrugIngredients.BrandName != ingredientA.BrandName)
)

select
    DrugDuplicateIDs.BrandName as BrandName,
    DrugbankIngredients.IngredientName as IngredientName,
    DrugbankCategories.CategoryName as CategoryName
  from DrugDuplicateIDs, DrugbankIngredients, DrugbankCategories
  where
    DrugbankIngredients.ActiveIngredientCode = DrugDuplicateIDs.ActiveIngredientCode
  and
    DrugbankCategories.CategoryID = DrugDuplicateIDs.CategoryID
