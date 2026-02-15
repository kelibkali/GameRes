import {defineStore} from 'pinia'
import type {UserModel} from "../types/User.ts";
import {computed, ref} from "vue";
import {checkLogin, register, userLogin, userLogout} from "../services/UserApi.ts";

export const useAuthStore = defineStore(
    'auth',
    ()=>{
        const user = ref<UserModel | null>(null);
        const loading = ref<boolean>(false);


        const isAuthenticated = computed(() => !!user.value);

        const registerUser = async (userData: UserModel) => {
            if(loading.value) return

            loading.value = true

            try{
                return await register(userData);
            }catch(error){
                return error;
            }finally {
                loading.value = false
            }
        }

        const loginUser = async (userData: Pick<UserModel, 'email'|'password'>) => {
            if(loading.value) return
            loading.value = true

            try{
                const result = await userLogin(userData);
                if(result.type === "success"){
                    await initAuthFromServer();
                }else{
                    console.log(result);
                }

                return result

            }catch(error){
                user.value = null;
            }finally {
                loading.value = false
            }
        }

        const logoutUser = async () => {
            if(loading.value) return
            loading.value = true
            try{
                const result = await userLogout();
                console.log(result);
                user.value = null;
            }catch(error){
                user.value = null;
            }finally {
                loading.value = false
            }
        }

        const initAuthFromServer = async () =>{
            try{
                const result = await checkLogin();

                if(result.type === "success"){
                    const userData = result.user_info;
                    user.value = {...userData};
                }else{
                    user.value = null
                }
            }catch(error){
                user.value = null;
            }
        }


        return {
            user,
            loading,
            isAuthenticated,

            registerUser,
            loginUser,
            logoutUser,
            initAuthFromServer,
        }
    }
)