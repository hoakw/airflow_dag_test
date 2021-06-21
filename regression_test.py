import numpy as np
import pandas as pd
import pymysql

from sklearn import linear_model
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

args = {
        'owner' : 'airflow',
}

with DAG(
        dag_id='regression_test',
        default_args=args,
        schedule_interval=None,
        start_date=days_ago(2),
        tags=['modeling'],
) as dag:

    def get_result():
        alpha = 0.0
        beta = 0.0
        intercept = 0.0

        data_dict = {}

        conn = pymysql.connect(host='192.168.100.104',
                                user='june',
                                password='wns123',
                                db='ml_test',
                                charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor)
        sql = conn.cursor()

        sql_query = "select * from ml_test"

        sql.execute(sql_query)

        rows = sql.fetchall()
        df = pd.DataFrame(rows)

        print("#####[JUNE]#####")
        print("table = \n", df)

        X = df[['cpu', 'mem']]
        y = df['power']


        linear_regression = linear_model.LinearRegression(fit_intercept=True)
        linear_regression.fit(X=pd.DataFrame(X), y=y)

        print("#####[JUNE] a = ", linear_regression.coef_[0])
        print("#####[JUNE] b = ", linear_regression.coef_[1])
        print("#####[JUNE] intercept = ", linear_regression.intercept_)

        sql.close()

    run_this = PythonOperator(
            task_id = 'modeling',
            python_callable=get_result,
    )

    run_this
