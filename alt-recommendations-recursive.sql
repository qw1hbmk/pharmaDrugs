with recursive

, GroupCategories as (
  select distinct
      DrugbankIngredientsCategories.CategoryID
    from BrandNameActiveIngredients
      inner join DrugbankIngredientsCategories
        on BrandNameActiveIngredients.ActiveIngredientCode = DrugbankIngredientsCategories.ActiveIngredientCode
    where
      {brand_names_ored}
)

, DrugsInCategories as (
  select distinct
      BrandName
    from GroupCategories
      inner join DrugbankIngredientsCategories
        on GroupCategories.CategoryID = DrugbankIngredientsCategories.CategoryID
      inner join BrandNameActiveIngredients
        on DrugbankIngredientsCategories.ActiveIngredientCode = BrandNameActiveIngredients.ActiveIngredientCode
)

BrandConflicts as (
  select distinct
      BrandNameConflicts.BrandName as BrandNameA,
      BrandNameActiveIngredients.BrandName as BrandNameB
    from BrandNameConflicts
    inner join BrandNameActiveIngredients
      on BrandNameConflicts.ConflictingIngredientCode = BrandNameActiveIngredients.ActiveIngredientCode
    where
        BrandNameA in DrugsInCategories
      and
        BrandNameB in DrugsInCategories
      and
        BrandNameA < BrandNameB
    order by random()
)

-- , MostCategoriesDrug as (
--   select
--       DrugsInCategories.BrandName,
--       count(distinct DrugbankIngredientsCategories.CategoryID) as num
--     from DrugsInCategories
--       inner join BrandNameActiveIngredients
--         on BrandNameActiveIngredients.BrandName = DrugsInCategories.BrandName
--       inner join DrugbankIngredientsCategories
--         on DrugbankIngredientsCategories.ActiveIngredientCode = BrandNameActiveIngredients.ActiveIngredientCode
--     group by
--       DrugsInCategories.BrandName
--     order by
--       num desc
--     limit 1
-- )

, wtf(BrandNameA, BrandNameB) as (
  select
      BrandNameConflicts.BrandNameA,
      BrandNameConflicts.BrandNameB
    from
      BrandNameConflicts
    limit 1
  union
    select
        BrandNameConflicts.BrandNameA,
        BrandNameConflicts.BrandNameB
      from DrugsInCategories
      where
          BrandName not in wtf
        and
          BrandName not in (
            select BrandNameB
              from BrandNameConflicts
              where
                BrandNameA in wtf
          )
      limit 15  -- for safety, so that we don't recurse forever
)

-- , DrugCodeCombos as (
--   select distinct
--       BrandNameActiveIngredients.DrugCode
--     from
-- )

select * from wtf
-- select count(*) from DrugsInCategories
