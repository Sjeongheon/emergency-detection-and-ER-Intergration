from typing import Union
from fastapi import FastAPI, HTTPException, File, UploadFile
import os
import openai
import pandas as pd
import emergency as em
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = FastAPI(
    title = "Hospital recommendation API with available emergency room",
    description = "음성과 위치 정보를 기반으로 가용 응급실이 있는 병원을 추천해주는 API",
    version = "1.0.0"
    )


@app.get("/hospital_by_module")
async def get_hospital(request: str, latitude: float, longitude: float):
    path = ''

    # api key setting
    try:
        os.environ['OPENAI_API_KEY'] = openai.api_key
        c_id, c_key = os.environ['MAP_ID'], os.environ['MAP_KEY']
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    # text_summary
    try:
        hospitals = pd.read_csv(path + 'hospital_info.csv')
        # 모델, 토크나이저 로드
        save_directory = path + "fine_tuned_bert"   
        model = AutoModelForSequenceClassification.from_pretrained(save_directory)
        tokenizer = AutoTokenizer.from_pretrained(save_directory)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    # load hospital data
    try:
        summary = em.text_summary(request)
        predicted_class, _ = em.predict(summary, model, tokenizer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    # recommend hostpital
    if predicted_class < 3:
        recommended_hospital = em.recommend_hospital3(hospitals, latitude, longitude, c_id, c_key)
        result_json = recommended_hospital.apply(lambda row: {
            "hospitalName": row["병원이름"],
            "address": row["주소"],
            "emergencyMedicalInstitutionType": row["응급의료기관 종류"],
            "phoneNumber1": row["전화번호 1"],
            "phoneNumber3": row["전화번호 3"],
            "latitude": row["위도"],
            "longitude": row["경도"],
            "distance": row["거리"]
        }, axis=1).tolist()
    else:
        recommended_hospital = "주변에 가용 응급실이 있는 병원이 없습니다."
   
    return result_json

