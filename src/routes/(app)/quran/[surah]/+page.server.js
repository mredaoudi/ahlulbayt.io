export const load = async ({ params }) => {
    const res = await fetch(`http://localhost:8080/quran/${params.surah}`);
    const data = await res.json();
    return {
      surah: data,
    };
  }