from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
default_args = {
    "start_date": datetime(2023, 1, 1),
    # "retries": 2,
}

def generate_conf(**kwargs):
    conf = "oid_section=OIDs\n[OIDs]\ncertificateTemplateName=1.3.6.1.4.1.311.20.2\n\n[req]\ndefault_bits=2048\nemailAddress={email}\nreq_extensions=v3_req\nx509_extensions=v3_ca\nprompt=no\ndefault_md=sha256\nreq_extensions=req_ext\ndistinguished_name=dn\n\n[dn]\nC={country}\nOU={organisational_unit}\nO={organisation}\nCN={common_name}\n\n[v3_req]\nbasicConstraints=CA:FALSE\nkeyUsage=digitalSignature, nonRepudiation, keyEncipherment\n\n[req_ext]\ncertificateTemplateName=ASN1:PRINTABLESTRING:PREZATCA-Code-Signing\nsubjectAltName=dirName:alt_names\n\n[alt_names]\nSN=1-{egs_unit}|2-{egs_version}|3-{egs_serial_no}\nUID={vat_no}\ntitle={title}\nregisteredAddress={reg_address}\nbusinessCategory={business_category}\n".format(
        email="support+fatoora@marmin.ai",
        country="SA",
        organisational_unit="Riyad Branch",
        organisation="311076986100003",
        common_name="EA123456789",
        egs_unit="TST",
        egs_version="TST",
        egs_serial_no="ed22f1d8e6a211189b58d9a8f11e445f",
        vat_no="311076986100003",
        title=1000,
        reg_address= "RRRD2929",
        business_category= "Real estate activities"
    )
    with open('csr_{}.cnf'.format(311076986100003), 'w') as fs:
        fs.write(conf)

    ti = kwargs['ti']
    ti.xcom_push(key='csr_file_name', value=311076986100003)

def clean_dag(session=None, **kwargs):
    from airflow.models import XCom
    print(kwargs['ti'])
    try:
        dag_run_id = kwargs['run_id']
        session.query(XCom).filter(XCom.run_id == dag_run_id).delete
        print(dag_run_id, XCom.run_id)
    except Exception as e:
        print(e)

with DAG("CSR-generation-workflow", default_args=default_args) as dag:

    create_cnf = PythonOperator(task_id="create-cfg", python_callable=generate_conf)

    read_cnf = BashOperator(task_id="read-cfg", do_xcom_push=True ,bash_command="bash -c '/opt/airflow/read.sh /opt/airflow/csr_311076986100003.cnf'")

    create_priavteKey = BashOperator(task_id="gen-private_key", do_xcom_push=True, bash_command="bash -c '/opt/airflow/genPk.sh /opt/airflow/private_311076986100003.pem'")

    create_csr = BashOperator(task_id="gen-csr", do_xcom_push=True, bash_command="bash -c '/opt/airflow/gencsr.sh /opt/airflow/private_311076986100003.pem /opt/airflow/csr_311076986100003.cnf /opt/airflow/csr'")
    
    dag_clean = PythonOperator(task_id="dag-clean", python_callable=clean_dag)

    create_cnf >> read_cnf >> create_priavteKey >> create_csr >> dag_clean