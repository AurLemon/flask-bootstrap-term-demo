import { createRouter, createWebHistory } from "vue-router";
import BlogView from "../views/BlogView.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "blog",
            component: BlogView,
        },
        {
            path: "/postview",
            name: "postView",
            component: () => import("../views/PostView.vue")
        },
        {
            path: "/admin",
            name: "admin",
            component: () => import("../views/AdminView.vue"),
        },
        {
            path: "/login",
            name: "login",
            component: () => import("../views/LoginView.vue"),
        },
        {
            path: "/register",
            name: "register",
            component: () => import("../views/RegisterView.vue"),
        },
        {
            path: "/upload",
            name: "upload",
            component: () => import("../views/UploadView.vue"),
        },
        {
            path: "/thanks",
            name: "thanks",
            component: () => import("../views/ThanksView.vue"),
        },
        {
            path: "/news/:id",
            name: "newsDetails",
            component: () => import("../views/NewsDetails.vue"),
            props: true,
        },
        {
            path: "/news/add",
            name: "newsAdd",
            component: () => import("../views/AddNews.vue")
        },
        {
            path: "/user",
            name: "user",
            component: () => import("../views/UserInfo.vue"),
        }
    ],
});

export default router;
