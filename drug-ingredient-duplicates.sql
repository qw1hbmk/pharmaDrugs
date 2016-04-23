with DrugActiveIngredients as (
  select
      BrandName,
      ActiveIngredientCode
    from BrandNameActiveIngredients
    where ({brand_names_ored})
),

DrugDuplicateIDs as (
  select
      ingredientA.BrandName,
      ingredientA.ActiveIngredientCode
    from DrugActiveIngredients ingredientA
      where ingredientA.ActiveIngredientCode in (
        select ActiveIngredientCode from DrugActiveIngredients otherDrugIngredients
          where otherDrugIngredients.BrandName != ingredientA.BrandName)
)

select
    DrugDuplicateIDs.BrandName as BrandName,
    DrugbankIngredients.IngredientName as IngredientName
  from DrugDuplicateIDs, DrugbankIngredients
  where
    DrugbankIngredients.ActiveIngredientCode = DrugDuplicateIDs.ActiveIngredientCode

