import apiClient from "./ApiClient.ts";
import type {UserModel} from "../types/User.ts";

export const register = async (user:UserModel) => {
    try{
        const response = await apiClient.post("/api/user/register",{
            username: user.username,
            password:user.password,
            email:user.email,
        })
        return response.data;
    }
    catch(error){
        console.log(error)
    }
}