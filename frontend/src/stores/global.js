import { defineStore } from 'pinia'

export const useGlobalStore = defineStore('global', {
  state: () => ({
    user: {

    }
  }),
  actions: {
    increment() {
      this.count++
    }
  }
})
