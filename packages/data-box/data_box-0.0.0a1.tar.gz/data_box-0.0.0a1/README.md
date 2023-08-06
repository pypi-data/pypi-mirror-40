Data_Box
=======
This project is to clean factor data and to prepare for back test.

Dependencies
------------
- python 3.5
- pandas 0.22.0
- numpy 1.14.3
- pickle
- sklearn 0.19.1 (for pca only)

Example
-------

```bash
from data_box import data_box

db=data_box()\
    .set_lag(freq='d',day_lag=0)\
    .load_adjPrice(price)\ # 'price' is a pd.DataFrame with dates(20190101 int type) as its index and tickers as its column
    .load_indestry(ind)\
    .load_suspend(sus)\ 
    .load_indexWeight(index_weight)\
    .calc_indweight()\ # calculate industry weight based on index weight and stocks' industry in this index
    .load_cap(cap)\ 
    .add_factor('f1',factor1)\
    .add_factor('f2',factor2)\
    .add_factor('f3',factor3)\
    .align_data()\
    .factor_pca()\
    .factor_ind_neutral()\
    .factor_size_neutral()\
    .factor_zscore()

print(db.Factor)
print(db.Price)
print(db.Sus)
print(db.Cap)

# save and reload
db.save(path)
db2=databox().load(path)
```
