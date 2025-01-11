export const allTeams = Array.from({ length: 34 }, (_, i) => ({
  id: i + 1,
  name: `Team ${i + 1}`,
  rankingPoints: Math.floor(Math.random() * 100),
  coopertition: Math.random(),
})); 