export const load = async ({ params, fetch }) => {
    const res = await fetch(`/quran/surahs/${params.surah}.json`);
    const data = await res.json();
    return {
      surah: data,
    };
  }