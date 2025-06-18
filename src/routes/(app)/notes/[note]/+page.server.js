import showdown from 'showdown';

export const load = async({params, parent}) => {
  let converter = new showdown.Converter({tables: true});
  const { notes } = await parent();
  return {
    note: converter.makeHtml(notes[params.note].content)
  }
}