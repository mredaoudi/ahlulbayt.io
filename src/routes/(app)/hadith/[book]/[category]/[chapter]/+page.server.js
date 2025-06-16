export const load = async ({params, parent}) => {
  const { category } = await parent();
  const chapter = category.chapters[params.chapter];
  return {
    chapter: chapter
  } 
}