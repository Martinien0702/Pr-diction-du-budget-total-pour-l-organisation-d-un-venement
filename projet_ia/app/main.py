# app/main.py
import time
import logging
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

from app.model_loader import load_model
from app.preprocessing import preprocess_input
from app.logger import log_success, log_error


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

model = load_model()



@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,

    Event_Type: str = Form(...),
    Venue_Capacity: float = Form(...),
    Marketing_Budget: float = Form(...),
    Pre_sale_Tickets: float = Form(...),
    Historical_Attendance_Similar_Events: float = Form(...),
    Venue_Rental_Cost: float = Form(...),
    Staff_Cost: float = Form(...),
    Stage_and_Equipment_Cost: float = Form(...),
    Permits_and_Licenses_Cost: float = Form(...)
):

    # Mesurer le temps
    start_time = time.time()

    # Construire DataFrame
    data = pd.DataFrame([{
        "Event_Type": Event_Type,
        "Venue_Capacity": Venue_Capacity,
        "Marketing_Budget": Marketing_Budget,
        "Pre_sale_Tickets": Pre_sale_Tickets,
        "Historical_Attendance_Similar_Events": Historical_Attendance_Similar_Events,
        "Venue_Rental_Cost": Venue_Rental_Cost,
        "Staff_Cost": Staff_Cost,
        "Stage_and_Equipment_Cost": Stage_and_Equipment_Cost,
        "Permits_and_Licenses_Cost": Permits_and_Licenses_Cost
    }])

    try:
        processed = preprocess_input(data)
        Expected_Attendance = 1000000
        prediction = model.predict(processed)[0]

        mae = Expected_Attendance - prediction
        elapsed = round(time.time() - start_time, 4)

        log_success(
            prediction=round(prediction, 2),
            mae=round(mae, 3),
            elapsed_time=elapsed,
            input_data=data.to_dict(orient="records")[0]
        )

    except Exception as e:
        log_error(str(e), data.to_dict(orient="records")[0])
        raise e


    except Exception as e:
        # ------ LOG D'ERREUR ------ #
        logging.error(
            f"ERROR: {str(e)} | Input={data.to_dict(orient='records')[0]}"
        )
        raise e

    return templates.TemplateResponse(
        "form.html",
        {"request": request, "prediction": round(prediction, 2)}
    )
