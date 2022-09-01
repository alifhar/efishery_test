
from datetime import datetime

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator

def ft_dim_customer():
	query = """select * from customers;"""
	df_ = pd.read_sql_query(query, engine)
	df_.to_sql(f'dim_customer', engine, if_exists='replace', index=False)

def ft_fact_order_accumulating()
	query = """ 
		select
			f1.id order_date_id,
			f2.id invoice_date_id,
			f3.id payment_date_id,
			a.id customer_id,
			b.order_number,
			c.invoice_number,
			d.payment_number,
			e.total_order_quantity,
			e.total_order_usd_amount,
			DATEDIFF(DAY, b.date, c.date) order_to_invoice_lag_days,
			DATEDIFF(DAY, c.date, d.date) invoice_to_payment_lag_days
		from customers a
			left join orders b on a.id = b.customer_id
			left join invoices c on b.order_number = c.order_number
			left join payments d on c.invoice_number = d.invoice_number
			left join 
				(select order_number, sum(quantity) total_order_quantity, sum(usd_amount) total_order_usd_amount from order_lines group by order_number) e
				on b.order_number = e.order_number
			left join dim_date f1 on b.date = f1.date
			left join dim_date f2 on c.date = f2.date
			left join dim_date f3 on d.date = f3.date;
	"""
					
	df_ = pd.read_sql_query(query, engine)
	df_.to_sql(f'fact_order_accumulating', engine, if_exists='replace', index=False)


with DAG(
    'efishery',
    schedule_interval = '0 7 * * *',
    start_date=datetime(2022, 1, 1),
    catchup=False
) as dag:

	dim_customer = PythonOperator(
        task_id='dim_customer',
		python_callable = ft_dim_customer
    )

    fact_order_accumulating = PythonOperator(
        task_id='fact_order_accumulating',
        python_callable = ft_fact_order_accumulating
    )

	dim_customer >> fact_order_accumulating
