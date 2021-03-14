from airflow.sensors.filesystem import FileSensor


file_task = FileSensor(task_id='check_file', filepath='/tmp/order_data.csv')

