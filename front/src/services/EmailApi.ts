import apiClient from "./ApiClient.ts";

export const generateEmailCode = async (email:string) => {
    try{
        const response = await apiClient.post("/api/code/generate",{
            email:email
        })

        return response.data;
    }catch(error){
        console.log(error)
    }
}

export const verifyCode = async (email:string,code:string) => {
    try{
        const response = await apiClient.post("/api/code/verify",{
            email:email,
            code:code
        })
        console.log(response.data)
        return response.data
    }catch(error){
        console.log(error)
    }
}