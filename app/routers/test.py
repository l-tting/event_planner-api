from fastapi import APIRouter,status

router = APIRouter()

@router.post('/',status_code=status.HTTP_200_OK)
def test_route():
    return {"Message":"Test ok"}