"""
Pydantic Schemas
================
اسکیماهای اعتبارسنجی داده‌ها
"""

from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserLogin, Token, TokenPayload
)
from app.schemas.athlete import (
    AthleteCreate, AthleteUpdate, AthleteResponse, AthleteListResponse,
    InjuryCreate, InjuryResponse, MeasurementCreate, MeasurementResponse
)
from app.schemas.food import (
    FoodCategoryCreate, FoodCategoryResponse, FoodCreate, FoodResponse, FoodSearch
)
from app.schemas.exercise import (
    MuscleGroupCreate, MuscleGroupResponse, ExerciseCreate, ExerciseResponse, ExerciseSearch
)
from app.schemas.supplement import (
    SupplementCategoryCreate, SupplementCategoryResponse,
    SupplementCreate, SupplementResponse
)
from app.schemas.training import (
    TrainingPlanCreate, TrainingPlanUpdate, TrainingPlanResponse,
    TrainingDayCreate, TrainingDayResponse,
    WorkoutItemCreate, WorkoutItemResponse
)
from app.schemas.diet import (
    DietPlanCreate, DietPlanUpdate, DietPlanResponse,
    DietItemCreate, DietItemResponse, MacroSummary
)
from app.schemas.supplement_plan import (
    SupplementPlanCreate, SupplementPlanUpdate, SupplementPlanResponse,
    SupplementPlanItemCreate, SupplementPlanItemResponse
)
from app.schemas.progress import ProgressRecordCreate, ProgressRecordResponse
from app.schemas.common import MessageResponse, PaginatedResponse

__all__ = [
    # User & Auth
    "UserCreate", "UserUpdate", "UserResponse", "UserLogin", "Token", "TokenPayload",
    
    # Athlete
    "AthleteCreate", "AthleteUpdate", "AthleteResponse", "AthleteListResponse",
    "InjuryCreate", "InjuryResponse", "MeasurementCreate", "MeasurementResponse",
    
    # Data Banks
    "FoodCategoryCreate", "FoodCategoryResponse", "FoodCreate", "FoodResponse", "FoodSearch",
    "MuscleGroupCreate", "MuscleGroupResponse", "ExerciseCreate", "ExerciseResponse", "ExerciseSearch",
    "SupplementCategoryCreate", "SupplementCategoryResponse", "SupplementCreate", "SupplementResponse",
    
    # Plans
    "TrainingPlanCreate", "TrainingPlanUpdate", "TrainingPlanResponse",
    "TrainingDayCreate", "TrainingDayResponse", "WorkoutItemCreate", "WorkoutItemResponse",
    "DietPlanCreate", "DietPlanUpdate", "DietPlanResponse",
    "DietItemCreate", "DietItemResponse", "MacroSummary",
    "SupplementPlanCreate", "SupplementPlanUpdate", "SupplementPlanResponse",
    "SupplementPlanItemCreate", "SupplementPlanItemResponse",
    
    # Progress
    "ProgressRecordCreate", "ProgressRecordResponse",
    
    # Common
    "MessageResponse", "PaginatedResponse",
]
