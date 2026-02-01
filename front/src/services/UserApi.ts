import apiClient from "./ApiClient.ts";
import type {UserModel} from "../types/User.ts";

export const register = async (user:UserModel) => {
    try{
        const response = await apiClient.post("/api/user/register",{
            username: user.username,
            password:user.password,
            email:user.email,
        },{
            headers: {
                "Content-Type": "application/json",
            }
        })
        return response.data;
    }
    catch(error){
        console.log(error)
    }
}

export const checkLogin = async () => {
    try{
        const response = await apiClient.get("/api/user/check_login",{
            headers: {
                "Content-Type": "application/json"
            },
            withCredentials: true,
        })
        return response.data;
    }catch(error){
        console.log(error)
    }
}

export const userLogin = async (user:UserModel) => {
    try{
        const response = await apiClient.post("/api/user/login",{
            email:user.email,
            password:user.password.trim(),
        },{
            headers: {
                "Content-Type": "application/json"
            }
        })
        return response.data;
    }catch(error){
        console.log(error)
    }
}

export const userLogout = async () => {
    try{
        await apiClient.get("/api/user/logout",{
            headers: {
                "Content-Type": "application/json"
            },
            withCredentials: true,
        })
    }catch(error){
        console.log(error)
    }

}