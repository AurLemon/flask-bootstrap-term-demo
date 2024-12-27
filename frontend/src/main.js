import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import './assets/styles/main.scss'
import './assets/styles/base.scss'

import './libraries/bootstrap/js/jquery.js'
import './libraries/bootstrap/css/bootstrap.min.css'
import './libraries/bootstrap/js/bootstrap.min.js'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
