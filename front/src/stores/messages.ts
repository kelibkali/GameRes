import {defineStore} from 'pinia'
import {ref} from 'vue'

export interface MessageItem{
    id:number,
    text:string,
}

export const useMessagesStore = defineStore('messages',()=>{
    const messages = ref<MessageItem[]>([])

    let nextId = 0;

    const addMessage = (text:string):void => {
        const id = nextId++;
        const message :MessageItem = {id,text};
        messages.value.push(message)

        setTimeout(()=>{
            removeMessage(id)
        },3000)
    }

    const removeMessage = (id:number):void => {
        const index = messages.value.findIndex(msg=>msg.id === id);
        if (index !== -1) {
            messages.value.splice(index, 1);
        }
    }

    return{
        messages,
        addMessage,
        removeMessage,
    }
})