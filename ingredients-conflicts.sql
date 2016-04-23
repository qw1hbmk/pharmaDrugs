with DrugNamesConflictIDs as (
  select
      ingredient.BrandName as BrandName,
      ingredient.ActiveIngredientCode as ActiveIngredientCode,
      conflict.BrandName as ConflictsWith,
      conflict.ActiveIngredientCode as ConflictingIngredientCode

    from BrandNameActiveIngredients ingredient
      inner join BrandNameConflicts conflict

      on ingredient.ActiveIngredientCode = conflict.ConflictingIngredientCode
    where
        ({brand_names_ored_ingredient})
      and
        ({brand_names_ored_conflict})
      and
        ingredient.BrandName != ConflictsWith
      and
        ingredient.ActiveIngredientCode < conflict.ActiveIngredientCode
      and 
        conflict.ActiveIngredientCode not in (
          select ActiveIngredientCode from BrandNameActiveIngredients 
            where BrandName = ingredient.BrandName)
)
select distinct
    DrugNamesConflictIDs.BrandName || 'x' || DrugNamesConflictIDs.ConflictsWith as GroupablePairName,
    DrugNamesConflictIDs.BrandName as BrandName,
    active.IngredientName as IngredientName,
    DrugNamesConflictIDs.ConflictsWith as ConflictsWith,
    conflict.IngredientName as ConflictingIngredient,
    DrugbankIngredientsDrugInteractions.Description as Description
  from DrugNamesConflictIDs
    inner join DrugbankIngredients active
    on active.ActiveIngredientCode = DrugNamesConflictIDs.ActiveIngredientCode
    inner join DrugbankIngredients conflict
    on conflict.ActiveIngredientCode = DrugNamesConflictIDs.ConflictingIngredientCode
    inner join DrugbankIngredientsDrugInteractions
    on 
        DrugbankIngredientsDrugInteractions.ActiveIngredientCode = DrugNamesConflictIDs.ActiveIngredientCode
      and
        DrugbankIngredientsDrugInteractions.ActiveIngredientCodeConflicting = DrugNamesConflictIDs.ConflictingIngredientCode






