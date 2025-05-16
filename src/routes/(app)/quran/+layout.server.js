export const load = async (event) => {
  const res = await event.fetch('/quran/surahs.json');
  const data = await res.json();
  return {
    surahs: data,
  };
}