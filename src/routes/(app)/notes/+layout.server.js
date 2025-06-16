export const load = async({fetch}) => {
  const notes = await fetch('/notes/notes.json');
  return {
    notes: await notes.json()
  }
}