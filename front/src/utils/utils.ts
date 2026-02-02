export const analyzeObject = (object: any): string => {
    if (typeof object === "object" && object) {
        let fieldName = Object.keys(object)[0]
        if (fieldName) {
            if (Object.prototype.hasOwnProperty.call(object, fieldName)) {
                const fieldErrors = (object as Record<string, any[]>)[fieldName]
                if (Array.isArray(fieldErrors)) {
                    for (const errorObject of fieldErrors) {
                        if (
                            errorObject &&
                            typeof errorObject === "object" &&
                            "message" in errorObject &&
                            typeof errorObject.message === "string" &&
                            errorObject.message.length > 0
                        ) {
                            return errorObject.message; // 找到第一个有效消息就立即返回
                        }
                    }
                }
            }
        }
    }
    return ""
}