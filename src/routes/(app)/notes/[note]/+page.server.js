import showdown from 'showdown';

export const load = async({params, fetch}) => {
  let converter = new showdown.Converter();
  const response = await fetch(`/static/notes/${params.note}.md`);
  return {
    note: converter.makeHtml(await response.text())
  }
}