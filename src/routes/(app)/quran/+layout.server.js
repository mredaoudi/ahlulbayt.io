export const load = async () => {
  const res = await fetch(`http://localhost:8080/quran`);
  return await res.json();
}