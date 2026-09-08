from fastapi import APIRouter

router = APIRouter()

system_state = {
    "camera": "online",
    "database": "online",
    "ai_engine": "online"
}

@router.get("/")
def get_system_status():
    return system_state

@router.post("/simulate")
def simulate_failure(component: str, status: str):
    if component in system_state:
        system_state[component] = status
        return {"message": f"{component} status set to {status}"}
    return {"error": "Component not found"}
