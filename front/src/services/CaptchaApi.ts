import apiClient from "./ApiClient.ts";

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

export const verifyCaptcha = async (code:string) => {
    try{
        const response = await apiClient.post("/api/captcha/verify",{
            captcha:code,
        });
        // console.log(response.data);
        return response.data;
    }catch (error) {
        console.log(error)
    }
}