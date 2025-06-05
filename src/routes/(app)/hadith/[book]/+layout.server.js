export const load = async ({params, fetch, parent}) => {
  const { books } = await parent();
  const book = books[params.book];
  const resp = await fetch(`/hadith/books/${book.bookId}.json`);
  return {
    book: book,
    categories: await resp.json()
  } 
}