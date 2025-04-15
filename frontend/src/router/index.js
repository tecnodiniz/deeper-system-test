import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/View/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/user/:id",
      name: "user",
      component: () => import("../View/UserView.vue"),
    },
  ],
});

export default router;
