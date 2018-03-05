const asignaciones = [
  [
    {
      nombre: "lube",
      status: "FREE",
      success_rate: 0.5,
      results: null,
      plan: [
        {
          recursos: [1, 6],
          payoff: 4,
          hora: 1,
          nombre: "C"
        }
      ]
    },
    {
      nombre: "viccita",
      status: "FREE",
      success_rate: 0.95,
      results: null,
      plan: [
        {
          recursos: [1, 2],
          payoff: 10,
          hora: 1,
          nombre: "A"
        },
        {
          recursos: [5, 6],
          payoff: 4,
          hora: 1,
          nombre: "D"
        }
      ]
    }
  ]
];

const resultados = [
  [
    {
      nombre: "lube",
      status: "BUSY",
      success_rate: 0.5,
      results: [
        {
          nombre: "C",
          resultado: 4
        }
      ],
      plan: [
        {
          recursos: [1, 6],
          payoff: 4,
          hora: 1,
          nombre: "C"
        }
      ]
    },
    {
      nombre: "viccita",
      status: "BUSY",
      success_rate: 0.95,
      results: [
        {
          nombre: "A",
          resultado: 10
        },
        {
          nombre: "D",
          resultado: 0
        }
      ],
      plan: [
        {
          recursos: [1, 2],
          payoff: 10,
          hora: 1,
          nombre: "A"
        },
        {
          recursos: [5, 6],
          payoff: 4,
          hora: 1,
          nombre: "D"
        }
      ]
    }
  ]
];

const satelites = [
  {
    nombre: "lube",
    success_rate: 0.5,
    status: "FREE"
  },
  {
    nombre: "viccita",
    success_rate: 0.9,
    status: "BUSY"
  }
];

const tareas = [
  { recursos: [1, 2], payoff: 10, hora: 1, nombre: "A" },
  { recursos: [1, 5], payoff: 1, hora: 1, nombre: "B" },
  { recursos: [1, 6], payoff: 1, hora: 1, nombre: "C" },
  { recursos: [5, 6], payoff: 0.1, hora: 1, nombre: "D" }
];
