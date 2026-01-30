import axios from 'axios'

const apiClient = axios.create({
    baseURL: import.meta.env.VITE_APP_BASE_URL,
    withCredentials: true,
})

export default apiClient

export const fetchUser  = async () => {
    try{
        const response = await apiClient.get("/api/user")
        return response.data
    }catch (error) {
        console.log(error)
    }
}

export const logout = async () => {
    try {
        await apiClient.post("/logout")
        console.log("logged out")
        window.location.href = "/"
    }catch (error) {
        console.log(error)
    }
}

export const getCaptchaImage = async () => {
    try{
        //设置响应类型为二进制
        const response = await apiClient.get("/api/captcha/get",{
            responseType: "blob"
        })

        const blob = response.data
        const reader = new FileReader()
        return new Promise<string>((resolve, reject) => {
            reader.onloadend = () => {
                // reader.result 是 Data URL (data:image/png;base64,...)
                if (reader.result && typeof reader.result === 'string') {
                    resolve(reader.result);
                } else {
                    reject(new Error('Failed to convert image to data URL'));
                }
            };
            reader.onerror = () => {
                reject(new Error('Error reading image blob'));
            };
            reader.readAsDataURL(blob); // 开始读取 Blob 数据为 Data URL
        });
    }catch (error) {
        console.log(error)
    }
}