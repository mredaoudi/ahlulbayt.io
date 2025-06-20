<script>
    const marjas = [
        {
            englishName: "Grand Ayatollah Sayyed Ali Hussaini Khamenei",
            url: "https://www.leader.ir/ar/book/48/2340/",
            arabicName: "المرجع الديني الأعلى آية الله العظمى السيد علي الحسيني الخامنئي"
        },
        {
            englishName: "Ayatollah Sayyed Ali Hussaini Sistani",
            url: "https://www.sistani.org/arabic/book/48/2340/",
            arabicName: "المرجع الديني آية الله العظمى السيد علي الحسيني السيستاني"
        }
    ];
</script>

<svelte:head>
    <title>Fiqh - Ahlulbayt.io</title> 
</svelte:head>

<h2 class="text-center">Fiqh</h2>
<div
    class="flex flex-col md:flex-row items-center justify-center gap-2 w-full"
>
    {#each marjas as marja}
        <a
            class="p-5 border rounded-md md:text-sm flex flex-col justify-between h-full w-full md:max-w-1/3 gap-3 border-slate-300 bg-white hover:border-slate-700 group"
            href={`${marja.url}`}
        >
            <div
                class="w-full text-center text-base font-medium text-slate-800"
            >
                {marja.englishName}
            </div>
            <div
                class="w-full text-center font-medium text-slate-600"
                style="font-family: 'Scheherazade New';"
            >
                {marja.arabicName}
            </div>
        </a>
    {/each}
</div>
