# Study
- [ ] [Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html)

# Install
- [x] [Local Install](https://airflow.apache.org/docs/apache-airflow/stable/start/local.html)

# Libraries
```shell
pip install apache-airflow
pip install apache-airflow-providers-amazon
```


# Questions
- start_date=days_ago(2) :2일전에 시작한다는건 무슨 얘기?
- interval 규칙
- airflow backfill
    - To backfill access Airflow docker container and run (Usage Manual에 있음)
- docker로 돌릴 때 및 local로 돌릴 때, custom python library 어떻게 연동하지?
    - `from settings.utils import (add_scala_steps, slack_failed_notification)`

# Reference
- [boto3 : AWS SDK for Python](https://github.com/boto/boto3)