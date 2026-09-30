from fastapi import FastAPI
import service

from fastapi import Body
from fastapi import Request
from fastapi import Form
from fastapi.responses import RedirectResponse

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(
    swagger_ui_parameters={
        "operationsSorter": "alpha"
    }
)

templates = Jinja2Templates(
    directory="templates"
)


@app.get("/")
def home():
    return "MES Server 실행 성공"


@app.get("/api/line")
def get_line():
    return {
        "line_id": "LINE-01",
        "line_name": "조립라인 1",
        "status": "running"
    }

@app.get("/api/lines")
def get_lines(status: str | None = None):

    result = service.get_lines(status)

    return result


@app.get("/api/products", response_class=HTMLResponse)

def get_products(request: Request):

    result = service.get_products()

    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={
            "products": result
        }
    )

@app.get("/api/production")
def get_production():
    
    result = service.get_production_records()
    
    return result

@app.post("/api/production")
def create_production(data: dict = Body(...)):
    record_id = service.add_production(
        data["production_date"],
        data["line_id"],
        data["product_id"],
        data["target_qty"],
        data["produced_qty"],
        data.get("defect_qty", 0)
    )

    return {
        "success": True,
        "record_id": record_id
    }

@app.put("/api/production/{record_id}")
def update_production(
    record_id: int,
    data: dict = Body(...)
):
    affected = service.update_production(
        record_id,
        data["produced_qty"],
        data["defect_qty"]
    )

    if affected == 0:
        return {
            "success": False,
            "message": "해당 생산실적을 찾을 수 없습니다."
        }

    return {
        "success": True,
        "record_id": record_id
    }    

@app.delete("/api/production/{record_id}")
def delete_production(record_id: int):

    affected = service.delete_production(record_id)

    if affected == 0:
        return {
            "success": False,
            "message": "해당 생산실적을 찾을 수 없습니다."
        }

    return {
        "success": True,
        "record_id": record_id
    }

# ============================================================
# 생산라인 등록
# ============================================================

@app.post("/api/lines")
def create_line(data: dict = Body(...)):

    line_id = service.add_line(
        data["line_id"],
        data["line_name"],
        data.get("status", "stopped")
    )

    return {
        "success": True,
        "line_id": line_id
    }


# ============================================================
# 생산라인 수정
# ============================================================

@app.put("/api/lines/{line_id}")
def update_line(
    line_id: str,
    data: dict = Body(...)
):

    affected = service.update_line(
        line_id,
        data["line_name"],
        data["status"]
    )

    if affected == 0:
        return {
            "success": False,
            "message": "해당 생산라인을 찾을 수 없습니다."
        }

    return {
        "success": True,
        "line_id": line_id
    }

# ============================================================
# 제품 등록
# ============================================================

@app.post("/api/products")

def create_product(
    product_id: str = Form(...),
    product_name: str = Form(...)
):

    product_id = service.add_product(
        product_id,
        product_name
    )
		
    return RedirectResponse(
        url="/api/products",
        status_code=303
    )


# ============================================================
# 제품 수정
# ============================================================

@app.put("/api/products/{product_id}")
def update_product(
    product_id: str,
    data: dict = Body(...)
):

    affected = service.update_product(
        product_id,
        data["product_name"]
    )

    if affected == 0:
        return {
            "success": False,
            "message": "해당 제품을 찾을 수 없습니다."
        }

    return {
        "success": True,
        "product_id": product_id
    }

@app.post("/api/orders")
def create_order(data: dict = Body(...)):

    order_id = service.add_production_order(
        data["line_id"],
        data["product_id"],
        data["target_qty"],
        data["planned_start_at"],
        data["due_at"]
    )

    return {
        "success": True,
        "order_id": order_id,
        "status": "planned"
    }    

@app.get("/api/orders")
def get_orders():

    return service.get_production_orders()

@app.put("/api/orders/{order_id}/start")
def start_production(order_id: int):

    affected = service.start_production(order_id)

    if affected == 0:
        return {
            "success": False,
            "message": "작업지시를 찾을 수 없습니다."
        }

    return {
        "success": True,
        "order_id": order_id,
        "status": "running"
    }

@app.put("/api/orders/{order_id}/complete")
def complete_production(order_id: int):

    affected = service.complete_production(order_id)

    if affected == 0:
        return {
            "success": False,
            "message": "작업지시를 찾을 수 없습니다."
        }

    return {
        "success": True,
        "order_id": order_id,
        "status": "completed"
    }

@app.get("/test", response_class=HTMLResponse)
def test_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="test.html",
        context={
            "title": "MES",
            "message": "Web MES"
        }
    )