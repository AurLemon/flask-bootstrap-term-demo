import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
    state: () => ({
        username: "未登录"
    }),
    actions: {
        setUsername(username) {
            this.username = username;
        }
    }
})
