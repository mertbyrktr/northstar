const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_URL = isLocal ? 'http://127.0.0.1:8000/api/v1' : '/api/v1';

class API {
    static getToken() {
        return localStorage.getItem('northstar_token');
    }

    static async request(endpoint, method = 'GET', body = null) {
        const headers = { 'Content-Type': 'application/json' };
        const token = this.getToken();
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const isForm = body instanceof URLSearchParams;
        if (isForm) delete headers['Content-Type'];

        const config = { method, headers };
        if (body) config.body = isForm ? body : JSON.stringify(body);

        try {
            const response = await fetch(`${API_URL}${endpoint}`, config);
            if (!response.ok) {
                const err = await response.json().catch(() => ({}));
                throw new Error(err.detail && typeof err.detail === 'string' ? err.detail : 'Request failed');
            }
            if (response.status === 204 || response.status === 200 && endpoint.includes('delete')) {
                return await response.json().catch(() => null);
            }
            return await response.json();
        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            throw error;
        }
    }

    // AUTH
    static async login(email, password) {
        const formData = new URLSearchParams();
        formData.append('username', email); // OAuth2 spec
        formData.append('password', password);
        const data = await this.request('/auth/login', 'POST', formData);
        if (data.access_token) localStorage.setItem('northstar_token', data.access_token);
        return data;
    }
    static async register(name, email, password) {
        return await this.request('/auth/register', 'POST', { name, email, password });
    }
    static logout() {
        localStorage.removeItem('northstar_token');
    }

    // WORKOUTS
    static async getWorkouts() { return await this.request('/workouts'); }
    static async deleteWorkout(id) { return await this.request(`/workouts/${id}`, 'DELETE'); }
    static async addExercise(workout_id, name, sets, reps, weight) {
        const payload = { workout_id, name, sets: parseInt(sets), reps: parseInt(reps), weight: parseFloat(weight) };
        return await this.request('/workouts/exercises', 'POST', payload);
    }
    static async deleteExercise(id) { return await this.request(`/exercises/${id}`, 'DELETE'); }
    
    // GOALS
    static async getGoals() { return await this.request('/goals').catch(() => []); }
    static async addGoal(title) { return await this.request('/goals', 'POST', { title }); }
    static async deleteGoal(id) { return await this.request(`/goals/${id}`, 'DELETE'); }
    static async toggleGoal(id) { return await this.request(`/goals/${id}/toggle`, 'PUT'); }
    
    // PROFILE & AI
    static async getProfile() { 
        return await this.request('/users/profile').catch(() => null); 
    }
    static async updateProfile(weight, height, age) { 
        return await this.request('/users/profile', 'PUT', { weight: parseFloat(weight), height: parseFloat(height), age: parseInt(age) }); 
    }
    static async getWeightMetrics() {
        return await this.request('/metrics/weight').catch(() => []);
    }
    static async logWeight(weight) {
        return await this.request('/metrics/weight', 'POST', { weight: parseFloat(weight) });
    }
    static async getAIRecommendation() { 
        // Deprecated
        return null;
    }
}
