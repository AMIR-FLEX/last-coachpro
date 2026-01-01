import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  User,
  UserCreate,
  UserLogin,
  TokenResponse,
  Athlete,
  AthleteCreate,
  AthleteUpdate,
  Food,
  FoodCategory,
  Exercise,
  MuscleGroup,
  TrainingPlan,
  DietPlan,
  BMRRequest,
  BMRResponse,
  TDEERequest,
  TDEEResponse,
  MacrosRequest,
  MacrosResponse,
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_BASE_URL}/api/v1`,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor - add token
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor - handle errors
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Token expired, try to refresh
          const refreshToken = this.getRefreshToken();
          if (refreshToken) {
            try {
              const response = await axios.post<TokenResponse>(
                `${API_BASE_URL}/api/v1/auth/refresh`,
                refreshToken,
                { headers: { 'Content-Type': 'application/json' } }
              );
              this.setTokens(response.data.access_token, response.data.refresh_token);
              // Retry original request
              if (error.config) {
                error.config.headers.Authorization = `Bearer ${response.data.access_token}`;
                return this.client.request(error.config);
              }
            } catch (refreshError) {
              this.clearTokens();
              if (typeof window !== 'undefined') {
                window.location.href = '/login';
              }
            }
          } else {
            this.clearTokens();
            if (typeof window !== 'undefined') {
              window.location.href = '/login';
            }
          }
        }
        return Promise.reject(error);
      }
    );
  }

  private getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('access_token');
  }

  private getRefreshToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('refresh_token');
  }

  setTokens(accessToken: string, refreshToken?: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', accessToken);
      if (refreshToken) {
        localStorage.setItem('refresh_token', refreshToken);
      }
    }
    this.token = accessToken;
  }

  clearTokens(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
    this.token = null;
  }

  // Auth API
  async register(data: UserCreate): Promise<User> {
    const response = await this.client.post<User>('/auth/register', data);
    return response.data;
  }

  async login(credentials: UserLogin): Promise<TokenResponse> {
    const response = await this.client.post<TokenResponse>('/auth/login', credentials);
    this.setTokens(response.data.access_token, response.data.refresh_token);
    return response.data;
  }

  async logout(): Promise<void> {
    this.clearTokens();
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.client.get<User>('/auth/me');
    return response.data;
  }

  // Athletes API
  async getAthletes(params?: { skip?: number; limit?: number; active_only?: boolean }): Promise<Athlete[]> {
    const response = await this.client.get<Athlete[]>('/athletes', { params });
    return response.data;
  }

  async getAthlete(id: number): Promise<Athlete> {
    const response = await this.client.get<Athlete>(`/athletes/${id}`);
    return response.data;
  }

  async createAthlete(data: AthleteCreate): Promise<Athlete> {
    const response = await this.client.post<Athlete>('/athletes', data);
    return response.data;
  }

  async updateAthlete(id: number, data: AthleteUpdate): Promise<Athlete> {
    const response = await this.client.put<Athlete>(`/athletes/${id}`, data);
    return response.data;
  }

  async deleteAthlete(id: number): Promise<void> {
    await this.client.delete(`/athletes/${id}`);
  }

  async searchAthletes(query: string, limit: number = 20): Promise<Athlete[]> {
    const response = await this.client.get<Athlete[]>('/athletes/search', {
      params: { q: query, limit },
    });
    return response.data;
  }

  // Injuries API
  async addAthleteInjury(athleteId: number, injuryData: any): Promise<any> {
    const response = await this.client.post(`/athletes/${athleteId}/injuries`, injuryData);
    return response.data;
  }

  async deleteAthleteInjury(injuryId: number): Promise<void> {
    await this.client.delete(`/athletes/injuries/${injuryId}`);
  }

  // Measurements API
  async addAthleteMeasurement(athleteId: number, measurementData: any): Promise<any> {
    const response = await this.client.post(`/athletes/${athleteId}/measurements`, measurementData);
    return response.data;
  }

  async getAthleteMeasurements(athleteId: number, limit: number = 10): Promise<any[]> {
    const response = await this.client.get(`/athletes/${athleteId}/measurements`, {
      params: { limit },
    });
    return response.data;
  }

  // Foods API
  async getFoodCategories(): Promise<FoodCategory[]> {
    const response = await this.client.get<FoodCategory[]>('/foods/categories');
    return response.data;
  }

  async searchFoods(query: string, categoryId?: number): Promise<Food[]> {
    const response = await this.client.get<Food[]>('/foods/search', {
      params: { q: query, category_id: categoryId },
    });
    return response.data;
  }

  async getFood(id: number): Promise<Food> {
    const response = await this.client.get<Food>(`/foods/${id}`);
    return response.data;
  }

  // Exercises API
  async getMuscleGroups(): Promise<MuscleGroup[]> {
    const response = await this.client.get<MuscleGroup[]>('/exercises/muscle-groups');
    return response.data;
  }

  async searchExercises(query: string, muscleGroupId?: number): Promise<Exercise[]> {
    const response = await this.client.get<Exercise[]>('/exercises/search', {
      params: { q: query, muscle_group_id: muscleGroupId },
    });
    return response.data;
  }

  async getExercise(id: number): Promise<Exercise> {
    const response = await this.client.get<Exercise>(`/exercises/${id}`);
    return response.data;
  }

  // Training Plans API
  async getAthleteTrainingPlans(athleteId: number, activeOnly: boolean = false): Promise<TrainingPlan[]> {
    const response = await this.client.get<TrainingPlan[]>(`/training/athlete/${athleteId}`, {
      params: { active_only: activeOnly },
    });
    return response.data;
  }

  async getActiveTrainingPlan(athleteId: number): Promise<TrainingPlan> {
    const response = await this.client.get<TrainingPlan>(`/training/athlete/${athleteId}/active`);
    return response.data;
  }

  async createTrainingPlan(data: any): Promise<TrainingPlan> {
    const response = await this.client.post<TrainingPlan>('/training/plans', data);
    return response.data;
  }

  async updateTrainingPlan(id: number, data: Partial<TrainingPlan>): Promise<TrainingPlan> {
    const response = await this.client.put<TrainingPlan>(`/training/plans/${id}`, data);
    return response.data;
  }

  async addTrainingDay(planId: number, dayData: any): Promise<any> {
    const response = await this.client.post(`/training/${planId}/days`, dayData);
    return response.data;
  }

  async addWorkoutItem(dayId: number, itemData: any): Promise<any> {
    const response = await this.client.post(`/training/days/${dayId}/items`, itemData);
    return response.data;
  }

  async deleteWorkoutItem(itemId: number): Promise<void> {
    await this.client.delete(`/training/items/${itemId}`);
  }

  async reorderWorkoutItems(dayId: number, itemIds: number[]): Promise<void> {
    await this.client.post(`/training/days/${dayId}/reorder`, itemIds);
  }

  // Diet Plans API
  async getAthleteDietPlans(athleteId: number, activeOnly: boolean = false): Promise<DietPlan[]> {
    const response = await this.client.get<DietPlan[]>(`/diet/athlete/${athleteId}`, {
      params: { active_only: activeOnly },
    });
    return response.data;
  }

  async getActiveDietPlan(athleteId: number): Promise<DietPlan> {
    const response = await this.client.get<DietPlan>(`/diet/athlete/${athleteId}/active`);
    return response.data;
  }

  async createDietPlan(data: any): Promise<DietPlan> {
    const response = await this.client.post<DietPlan>('/diet/plans', data);
    return response.data;
  }

  async updateDietPlan(id: number, data: Partial<DietPlan>): Promise<DietPlan> {
    const response = await this.client.put<DietPlan>(`/diet/plans/${id}`, data);
    return response.data;
  }

  // Calculator API
  async calculateBMR(data: BMRRequest): Promise<BMRResponse> {
    const response = await this.client.post<BMRResponse>('/calculator/bmr', data);
    return response.data;
  }

  async calculateTDEE(data: TDEERequest): Promise<TDEEResponse> {
    const response = await this.client.post<TDEEResponse>('/calculator/tdee', data);
    return response.data;
  }

  async calculateMacros(data: MacrosRequest): Promise<MacrosResponse> {
    const response = await this.client.post<MacrosResponse>('/calculator/macros', data);
    return response.data;
  }

  async calculate1RM(weight: number, reps: number): Promise<{ one_rm: number }> {
    const response = await this.client.post<{ one_rm: number }>('/calculator/1rm', {
      weight,
      reps,
    });
    return response.data;
  }

  async calculateAthleteNutrition(athleteId: number): Promise<MacrosResponse> {
    const response = await this.client.get<MacrosResponse>(`/athletes/${athleteId}/nutrition`);
    return response.data;
  }

  // Supplement Plans API
  async getAthleteSupplementPlans(athleteId: number, activeOnly: boolean = false): Promise<any[]> {
    const response = await this.client.get<any[]>(`/supplement-plans/athlete/${athleteId}`, {
      params: { active_only: activeOnly },
    });
    return response.data;
  }

  async getActiveSupplementPlan(athleteId: number): Promise<any> {
    const response = await this.client.get<any>(`/supplement-plans/athlete/${athleteId}/active`);
    return response.data;
  }

  async createSupplementPlan(data: any): Promise<any> {
    const response = await this.client.post<any>('/supplement-plans', data);
    return response.data;
  }

  async addSupplementItem(planId: number, itemData: any): Promise<any> {
    const response = await this.client.post(`/supplement-plans/${planId}/items`, itemData);
    return response.data;
  }

  async deleteSupplementItem(itemId: number): Promise<void> {
    await this.client.delete(`/supplement-plans/items/${itemId}`);
  }

  // Diet Items API
  async addDietItem(planId: number, itemData: any): Promise<any> {
    const response = await this.client.post(`/diet/${planId}/items`, itemData);
    return response.data;
  }

  async deleteDietItem(itemId: number): Promise<void> {
    await this.client.delete(`/diet/items/${itemId}`);
  }

  async reorderDietItems(planId: number, itemIds: number[]): Promise<void> {
    await this.client.post(`/diet/${planId}/reorder`, itemIds);
  }
}

export const apiClient = new ApiClient();

