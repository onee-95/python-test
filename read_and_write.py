import pandas as pd
from google.cloud import storage
import io

def read_from_gcs(bucket_name, source_blob_name):
    """GCS에서 파일 읽기"""
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    # GCS에서 CSV 파일을 읽어 DataFrame으로 변환
    data = blob.download_as_text()
    df = pd.read_csv(io.StringIO(data))
    return df


def process_data(df):
    """데이터 가공 함수"""
    df = df[df["Country"]=="US"]

    # 예시: 특정 조건에 따라 데이터 필터링
    # df = df[df['Date'] != '2024-10-11']  # 2024-10-11 데이터를 제외
    # 필요에 따라 가공 작업 추가
    return df


def save_to_gcs(bucket_name, destination_blob_name, df):
    """DataFrame을 GCS에 저장"""
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # DataFrame을 CSV 형식으로 변환 후 GCS에 업로드
    blob.upload_from_string(df.to_csv(index=False), content_type='text/csv')


def main():
    bucket_name = 'maximizer-test'  # 버킷 이름
    source_blob_name = 'catnsoup/source/aos_agg_9.csv'  # 읽을 파일 경로
    destination_blob_name = 'catnsoup/source/aos_agg_9_fix.csv'  # 저장할 파일 경로

    # 1. GCS에서 파일 읽기
    df = read_from_gcs(bucket_name, source_blob_name)

    # 2. 데이터 가공
    processed_df = process_data(df)

    # 3. GCS에 결과 저장
    save_to_gcs(bucket_name, destination_blob_name, processed_df)


if __name__ == "__main__":
    main()
