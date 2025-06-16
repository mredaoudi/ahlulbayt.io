export const load = async ({params, fetch, parent}) => {
  const { categories } = await parent();
  const category = categories[params.category];
  return {
    category: category
  } 
}