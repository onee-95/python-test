from datetime import date, timedelta
import requests
import time
from google.cloud import storage  # GCS 라이브러리 추가

# GCS에 파일 업로드 함수
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


_TOKEN = 'eyJhbGciOiJBMjU2S1ciLCJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwidHlwIjoiSldUIiwiemlwIjoiREVGIn0.W9M9YCCFm61qoTmwA0xkCN84a5FjVJHBsQepzbJ36GYQ4mgo7Q-e3Q.x2tBHAC-29s1zzxf.GCFfgeeNc1F8R711_xmIgPNsImiOOnfhu2cVyseTqsD4ZD8rxu1JUF1FrnHXa-fC7JCQo78LiGFkEKU2DpPYBieKdTDo7_Qa2ZB4Lnq1NJd1IvkCGbPiBeIgriZpg322TVOImFEyG4Sw5EXnAp7hgv2_RpRTuy26zgRSl-fXOU2pzK1HFFdQLXAjUyPqpxNz6uV6623kjNMeh7Df2Lx26yXGFO_QHqjosdDqpTLkC_yM3NRlIhl842yKLlf0tjhHXuacx8ZjsZ0XRprF_Bjtyd9q3tdh6OLe7a6vaVYA8VrfBUJMfQ3ANHNiCI3OHWJ6J-rbz8nOPBkqgjlrHNNECBxK8V8xtCcGt182H_ARJ-pBdmUw1nzq4XRxqsf7hmtN-Bufe1nv1tUNff-42i_lyGAbmUoe2pjH8CMYsAXomX7zobn-wNsDGjtTg04K5fQ7XbbJAoqyXAC9yHUEV1kOOewK7ZiZ34Ma_ST4vDzaUXid387cHLRqt0TwwUNNrS9bo14MUsyn4-q2pT9qxX_1S2I1WyCZ.0ajBNnz_RI-mjYgA-hDWeQ'
_APP_ID_AND = 'com.hidea.cat'


def geo_by_date_report(start_date, end_date, bucket_name):
    _REPORT_TYPE = 'geo_by_date_report'
    request_url = f'https://hq1.appsflyer.com/api/agg-data/export/app/{_APP_ID_AND}/{_REPORT_TYPE}/v5'

    headers = {
        "accept": "text/csv",
        "authorization": f"Bearer {_TOKEN}"
    }
    params_and = {
        'from': start_date,
        'to': end_date,
        'timezone': 'Asia/Seoul'
    }

    # 첫 번째 데이터 요청
    response = requests.get(request_url, params=params_and, headers=headers)
    output_file1 = '/tmp/aos_agg_9.csv'  # Cloud Run에서는 임시 디렉토리인 /tmp 사용
    with open(output_file1, 'w', newline='', encoding="utf-8-sig") as f:
        f.write(response.text)

    # GCS로 업로드
    upload_to_gcs(bucket_name, output_file1, 'aos_agg_9.csv')

def main():
    bucket_name = 'maximizer-test'  # GCS 버킷 이름
    start_date = '2024-09-01'
    end_date = str(date.today() - timedelta(days=1))

    # 데이터를 GCS에 저장
    geo_by_date_report(start_date, end_date, bucket_name)


if __name__ == '__main__':
    main()
