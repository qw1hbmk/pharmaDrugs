
create temporary view BrandNameActiveIngredients as
  select distinct
    BrandName,
    ActiveIngredientCode
  from DrugProduct, ActiveIngredients
  where DrugProduct.DrugCode = ActiveIngredients.DrugCode
;



create temporary view BrandNameConflicts as
  select
      DrugProduct.BrandName as BrandName,
      ActiveIngredients.ActiveIngredientCode as ActiveIngredientCode,
      DrugbankIngredientsDrugInteractions.ActiveIngredientCodeConflicting as ConflictingIngredientCode

    from DrugProduct, ActiveIngredients, DrugbankIngredients, DrugbankIngredientsDrugInteractions

    where
        ActiveIngredients.DrugCode = DrugProduct.DrugCode
      and








      
        DrugbankIngredients.ActiveIngredientCode = ActiveIngredients.ActiveIngredientCode
      and 
        DrugbankIngredientsDrugInteractions.ActiveIngredientCode = DrugbankIngredients.ActiveIngredientCode
;





