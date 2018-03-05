import httpClient from "./httpClient";

export async function getTareas() {
  const { data } = await httpClient.get("/api/tareas");
  console.log(data);
  return data;
}

export async function getSatelites() {
  const { data } = await httpClient.get("/api/satelites");

  return data;
}

export async function getAsignaciones() {
  const { data } = await httpClient.get("/api/asignaciones");

  return data;
}

export async function getResultados() {
  const { data } = await httpClient.get("/api/resultados");

  return data;
}

export async function addTarea(tarea) {
  const { data } = await httpClient.post("/api/tarea", tarea);

  return data;
}

export async function ejecutarCampaña() {
  const { data } = await httpClient.post("/api/ejecutar_campaña");

  return data;
}
