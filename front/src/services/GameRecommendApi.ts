import apiClient from "./ApiClient.ts";

export const getRecommendGames = async () => {
    try{
        const response = await apiClient.get(`/api/recommendation/get_recommend_games`);
        console.log(response.data);
        return response.data;
    }catch(error){
        console.error(error);
    }
}