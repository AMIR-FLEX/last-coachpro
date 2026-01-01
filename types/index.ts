// API Types based on Backend Schemas

export type Gender = 'male' | 'female';
export type Goal = 'bulk' | 'cut' | 'maintain' | 'recomp' | 'strength' | 'endurance';
export type ActivityLevel = 'sedentary' | 'light' | 'moderate' | 'active' | 'very_active';
export type ExperienceLevel = 'beginner' | 'intermediate' | 'advanced' | 'elite';

// Helper functions to convert activity factor to ActivityLevel
export function activityFactorToLevel(factor: string | number): ActivityLevel {
  const num = typeof factor === 'string' ? parseFloat(factor) : factor;
  if (num <= 1.2) return 'sedentary';
  if (num <= 1.375) return 'light';
  if (num <= 1.55) return 'moderate';
  if (num <= 1.725) return 'active';
  return 'very_active';
}

export function levelToActivityFactor(level: ActivityLevel): string {
  const map: Record<ActivityLevel, string> = {
    sedentary: '1.2',
    light: '1.375',
    moderate: '1.55',
    active: '1.725',
    very_active: '1.9',
  };
  return map[level];
}

// User Types
export interface User {
  id: number;
  email: string;
  full_name: string;
  phone?: string;
  bio?: string;
  avatar_url?: string;
  is_active: boolean;
  is_superuser: boolean;
  theme: string;
  language: string;
  created_at: string;
  updated_at?: string;
}

export interface UserCreate {
  email: string;
  password: string;
  full_name: string;
  phone?: string;
  bio?: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token?: string;
  token_type: string;
}

// Athlete Types
export interface Athlete {
  id: number;
  coach_id: number;
  name: string;
  age?: number;
  gender?: Gender;
  height?: number;
  weight?: number;
  phone?: string;
  email?: string;
  goal?: Goal;
  activity_level?: ActivityLevel;
  experience_level?: ExperienceLevel;
  job?: string;
  sleep_quality?: string;
  allergies?: string;
  medical_conditions?: string;
  notes?: string;
  is_active: boolean;
  avatar_url?: string;
  subscription_start?: string;
  subscription_months?: number;
  subscription_amount?: number;
  injuries: Injury[];
  created_at: string;
  updated_at?: string;
}

export interface AthleteCreate {
  name: string;
  age?: number;
  gender?: Gender;
  height?: number;
  weight?: number;
  phone?: string;
  email?: string;
  goal?: Goal;
  activity_level?: ActivityLevel;
  experience_level?: ExperienceLevel;
  job?: string;
  sleep_quality?: string;
  allergies?: string;
  medical_conditions?: string;
  notes?: string;
  subscription_start?: string;
  subscription_months?: number;
  subscription_amount?: number;
  injuries?: InjuryCreate[];
}

export interface AthleteUpdate {
  name?: string;
  age?: number;
  gender?: Gender;
  height?: number;
  weight?: number;
  phone?: string;
  email?: string;
  goal?: Goal;
  activity_level?: ActivityLevel;
  experience_level?: ExperienceLevel;
  job?: string;
  sleep_quality?: string;
  allergies?: string;
  medical_conditions?: string;
  notes?: string;
  is_active?: boolean;
  subscription_start?: string;
  subscription_months?: number;
  subscription_amount?: number;
}

// Injury Types
export interface Injury {
  id: number;
  athlete_id: number;
  body_part: string;
  description?: string;
  severity?: 'mild' | 'moderate' | 'severe';
  is_healed: boolean;
  injury_date?: string;
  created_at: string;
}

export interface InjuryCreate {
  body_part: string;
  description?: string;
  severity?: 'mild' | 'moderate' | 'severe';
  is_healed?: boolean;
  injury_date?: string;
}

// Measurement Types
export interface Measurement {
  id: number;
  athlete_id: number;
  recorded_at: string;
  weight?: number;
  body_fat?: number;
  neck?: number;
  chest?: number;
  shoulders?: number;
  waist?: number;
  hip?: number;
  thigh_right?: number;
  thigh_left?: number;
  arm_right?: number;
  arm_left?: number;
  forearm_right?: number;
  forearm_left?: number;
  calf_right?: number;
  calf_left?: number;
  wrist?: number;
  notes?: string;
}

export interface MeasurementCreate {
  recorded_at?: string;
  weight?: number;
  body_fat?: number;
  neck?: number;
  chest?: number;
  shoulders?: number;
  waist?: number;
  hip?: number;
  thigh_right?: number;
  thigh_left?: number;
  arm_right?: number;
  arm_left?: number;
  forearm_right?: number;
  forearm_left?: number;
  calf_right?: number;
  calf_left?: number;
  wrist?: number;
  notes?: string;
}

// Food Types
export interface Food {
  id: number;
  name: string;
  name_en?: string;
  category_id: number;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  fiber?: number;
  base_amount: number;
  unit: string;
}

export interface FoodCategory {
  id: number;
  name: string;
  name_en: string;
  icon?: string;
  sort_order: number;
}

// Exercise Types
export interface Exercise {
  id: number;
  name: string;
  name_en?: string;
  muscle_group_id: number;
  equipment?: string;
  type?: string;
  instructions?: string;
}

export interface MuscleGroup {
  id: number;
  name: string;
  name_en: string;
  sort_order: number;
}

// Training Plan Types
export interface TrainingPlan {
  id: number;
  athlete_id: number;
  name: string;
  description?: string;
  duration_weeks?: number;
  split_type?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
  days?: TrainingDay[];
}

export interface TrainingDay {
  id: number;
  training_plan_id: number; // Matches backend schema exactly
  day_number: number;
  name?: string;
  notes?: string;
  is_rest_day?: boolean;
  workout_items?: WorkoutItem[];
  created_at?: string;
}

export interface WorkoutItem {
  id: number;
  training_day_id: number; // Matches backend schema exactly (was: day_id)
  exercise_id?: number;
  exercise?: Exercise;
  custom_name?: string;
  secondary_exercise_name?: string;
  tertiary_exercise_name?: string;
  set_type?: string;
  sets?: number;
  reps?: string;
  weight?: number;
  duration_minutes?: number;
  rest_seconds?: number;
  tempo?: string; // Matches backend
  intensity?: string;
  notes?: string;
  order: number;
  created_at?: string;
}

export interface TrainingSession {
  id: number;
  plan_id: number;
  day_number: number;
  exercises: ExerciseInSession[];
}

export interface ExerciseInSession {
  id: number;
  session_id: number;
  exercise_id: number;
  exercise_name: string;
  sets: number;
  reps?: number;
  weight?: number;
  duration?: number;
  rest_seconds?: number;
  notes?: string;
  order: number;
}

// Diet Plan Types
export interface DietPlan {
  id: number;
  athlete_id: number;
  name: string;
  description?: string;
  target_calories?: number;
  target_protein?: number;
  target_carbs?: number;
  target_fat?: number;
  general_notes?: string; // Matches backend schema (was missing)
  is_active: boolean;
  created_at: string;
  updated_at?: string;
  items?: DietItem[];
}

export interface DietItem {
  id: number;
  diet_plan_id: number; // Matches backend schema exactly (was: plan_id)
  food_id?: number;
  food?: Food;
  custom_name?: string;
  meal: string; // MealType enum value from backend
  amount: number;
  unit?: string; // Optional in backend
  custom_calories?: number;
  custom_protein?: number;
  custom_carbs?: number;
  custom_fat?: number;
  calculated_calories?: number;
  calculated_protein?: number;
  calculated_carbs?: number;
  calculated_fat?: number;
  notes?: string; // Matches backend
  order: number;
  created_at?: string;
}

export interface Meal {
  id: number;
  plan_id: number;
  meal_type: string;
  meal_order: number;
  foods: MealFood[];
}

export interface MealFood {
  id: number;
  meal_id: number;
  food_id: number;
  food_name: string;
  amount: number;
  unit: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
}

// Supplement Plan Types
export interface SupplementPlan {
  id: number;
  athlete_id: number;
  name: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
  items?: SupplementPlanItem[];
}

export interface SupplementPlanItem {
  id: number;
  supplement_plan_id: number; // Matches backend schema exactly (was: plan_id)
  supplement_id?: number;
  supplement?: Supplement;
  custom_name?: string;
  dose?: string;
  timing?: string;
  notes?: string;
  instructions?: string;
  order: number;
  created_at?: string;
}

export interface Supplement {
  id: number;
  name: string;
  name_en?: string;
  category?: string;
  description?: string;
}

// Calculator Types
export interface BMRRequest {
  weight: number;
  height: number;
  age: number;
  gender: Gender;
  body_fat?: number;
}

export interface BMRResponse {
  bmr: number;
  bmr_method: string;
}

export interface TDEERequest extends BMRRequest {
  activity_level: ActivityLevel;
}

export interface TDEEResponse {
  bmr: number;
  tdee: number;
  activity_multiplier: number;
}

export interface MacrosRequest extends TDEERequest {
  goal: Goal;
}

export interface MacrosResponse {
  bmr: number;
  tdee: number;
  goal: Goal;
  macros: {
    calories: number;
    protein: number;
    carbs: number;
    fat: number;
  };
  macro_ratios: {
    protein_percentage: number;
    carbs_percentage: number;
    fat_percentage: number;
  };
}

// UI State Types
export type TabType = 'users' | 'training' | 'nutrition' | 'supplements' | 'progress';

export interface AppState {
  theme: 'dark' | 'light';
  currentTab: TabType;
  activeAthleteId: number | null;
}

