export const analyzeObject = (object: any,messages:string[]) => {
    if (typeof object === "object" && object) {
        let fieldName = Object.keys(object)[0]
        if(fieldName){
            if (Object.prototype.hasOwnProperty.call(object, fieldName)) {
                const fieldErrors = (object as Record<string, any[]>)[fieldName]
                if (Array.isArray(fieldErrors)) {
                    fieldErrors.forEach(errorObject => {
                        if (errorObject && typeof errorObject === "object" && "message" in errorObject) {
                            const message = errorObject.message as string
                            if (message && message.length > 0) {
                                messages.push(message)
                            }
                        }
                    })
                }
            }
        }
    }
}