import apiClient from "./ApiClient.ts";

export const loginSteam = async () =>{
    window.location.href = `${import.meta.env.VITE_APP_BASE_URL}/api/steam/login`
}

export const logoutSteam = async () =>{
    const response = await apiClient.get("/api/steam/logout")
    return response.data
}

export const getGames = async (steam_id:string) => {
    const response = await apiClient.get(`/api/steam/games/${steam_id}`);
    return response.data
}