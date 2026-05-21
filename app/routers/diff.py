from fastapi import APIRouter

from app.services.config_diff import generate_diff

router = APIRouter(prefix="/diff", tags=["Diff"])


@router.post("/")
def compare_configs(old_config: str, new_config: str):
    diff_result = generate_diff(old_config, new_config)

    return {
        "diff": diff_result
    }