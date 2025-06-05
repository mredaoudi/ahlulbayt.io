export const load = async (event) => {
  const res = await event.fetch('/hadith/books.json');
  const data = await res.json();
  return {
    books: data,
  };
}