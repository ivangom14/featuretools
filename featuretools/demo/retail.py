import pandas as pd

import featuretools as ft
import featuretools.variable_types as vtypes


def load_retail(id='demo_retail_data', nrows=None, return_single_table=False):
    '''
    Returns the retail entityset example which is a modified version of
    the data found `here <https://archive.ics.uci.edu/ml/datasets/online+retail>`_.

    Args:
        id (str):  Id to assign to EntitySet.
        nrows (int):  Number of rows to load of the underlying CSV.
            If None, load all.
        return_single_table (bool): If True, return a CSV rather than an EntitySet. Default is False.

    Examples:

        .. ipython::
            :verbatim:

            In [1]: import featuretools as ft

            In [2]: es = ft.demo.load_retail()

            In [3]: es
            Out[3]:
            Entityset: demo_retail_data
              Entities:
                orders (shape = [22190, 3])
                products (shape = [3684, 3])
                customers (shape = [4372, 2])
                order_products (shape = [401704, 7])

        Load in subset of data

        .. ipython::
            :verbatim:

            In [4]: es = ft.demo.load_retail(nrows=1000)

            In [5]: es
            Out[5]:
            Entityset: demo_retail_data
              Entities:
                orders (shape = [67, 5])
                products (shape = [606, 3])
                customers (shape = [50, 2])
                order_products (shape = [1000, 7])

    '''
    es = ft.EntitySet(id)
    csv_s3 = "https://s3.amazonaws.com/featuretools-static/" + RETAIL_CSV + ".csv"

    df = pd.read_csv(csv_s3,
                     nrows=nrows,
                     parse_dates=["order_date"])

    if return_single_table:
        return df

    es.entity_from_dataframe("order_products",
                             dataframe=df,
                             index="order_product_id",
                             time_index="order_date",
                             variable_types={'description': vtypes.Text})

    es.normalize_entity(new_entity_id="products",
                        base_entity_id="order_products",
                        index="product_id",
                        additional_variables=["description"])

    es.normalize_entity(new_entity_id="orders",
                        base_entity_id="order_products",
                        index="order_id",
                        additional_variables=["customer_name", "country", "cancelled"])

    es.normalize_entity(new_entity_id="customers",
                        base_entity_id="orders",
                        index="customer_name")
    es.add_last_time_indexes()

    return es


RETAIL_CSV = "online-retail-logs-2018-08-28"
