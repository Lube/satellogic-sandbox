import Dashboard from "views/Dashboard/Dashboard";
import Tareas from "views/Tareas/TableList";
import Satelites from "views/Satelites/TableList";
import Asignaciones from "views/Asignaciones/TableList";
import Resultados from "views/Resultados/TableList";

const appRoutes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    icon: "pe-7s-graph",
    component: Dashboard
  },
  {
    path: "/tareas",
    name: "Tareas",
    icon: "pe-7s-note",
    component: Tareas
  },
  {
    path: "/satelites",
    name: "Satelites",
    icon: "pe-7s-rocket",
    component: Satelites
  },
  {
    path: "/asignaciones",
    name: "Asignaciones",
    icon: "pe-7s-notebook",
    component: Asignaciones
  },
  {
    path: "/resultados",
    name: "Resultados",
    icon: "pe-7s-note2",
    component: Resultados
  },
  { redirect: true, path: "/", to: "/dashboard", name: "dashboard" }
];

export default appRoutes;
