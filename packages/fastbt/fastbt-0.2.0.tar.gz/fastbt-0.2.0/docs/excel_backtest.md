# Introduction

You can create your strategy in Excel and then use the `backtest_from_excel` function to get the results. The Excel file should be in the required format. Use the starter template **backtest_template.xls** in the examples directory.

## Concept

The function is just a wrapper to the `backtest` function. You specify the structure of your backtest in Excel and then supply a dataframe or a SQL connection to it.

```python
from fastbt.rapid import backtest_from_excel

backtest_from_excel('excel_template.xls', data=df)
```

The Excel file is split into parameters, columns and conditions (more details below).

-   **Parameters** are the parameters to the backtest function.
-   **Columns** are a list of columns with the necessary column types and arguments. These columns must be created before the backtest is run. Think them of something similar to named formulas in a Excel sheet.
-   **Conditions** are a list of conditions specified as a string. They must produce a Boolean value and are used to filter the results before running a backtest. Conditions must refer to already existing columns in the dataframe.

## Structure

The Excel template should have three sheets with the following names

-   parameters
-   columns
-   conditions

### Parameters

The parameters should have 2 columns with the first column being the parameter names and the second column the values. All these parameters directly correspond to the parameters in the `backtest` function. All the parameters are allowed except the following

-   columns
-   conditions
-   data
-   connection
-   tablename
-   where_clause

Since we are supplying a data source directly, we can disregard the parameters relating to data

### Columns

Columns are columns to be added to the existing dataframe. Think them as something similar to named formulas in Excel. They are mapped to the corresponding columns in datasource

The columns sheet has a header and must have the following mandatory columns

| header   | value                                                   |
| -------- | ------------------------------------------------------- |
| col_type | one of lag, percent_change, rolling, formula, indicator |
| col_name | an optional column name, mandatory for col_type formula |
| argument | the first argument to the col_type                      |
| on       | column on which the calculation is to be applied        |
| period   | the period in case of percent change, lag               |
| lag      | lag parameter for all column types except lag           |

### Conditions
