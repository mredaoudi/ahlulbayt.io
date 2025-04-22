<script>
    import { Shuffle } from "@lucide/svelte";
    import { Search } from "@lucide/svelte";
    import { includesCaseInsensitive, isArabic } from "$lib/utils.js";
    import { goto } from "$app/navigation";

    let { data } = $props();
    let searchTextState = $state({value: ""});
    let filteredSurahs = $derived.by(() =>{
        let filteredResults = data.surahs;
        if(searchTextState.value !== ""){
            filteredResults = filteredResults.filter((surah) =>
                includesCaseInsensitive(surah.ar, searchTextState.value) ||
                includesCaseInsensitive(surah.en, searchTextState.value) ||
                includesCaseInsensitive(surah._a, searchTextState.value) ||
                includesCaseInsensitive(surah._l, searchTextState.value)
            );
        }
        return filteredResults;
    });

    function gotoRandomVerse() {
        const randomSurahIndex = Math.floor(Math.random() * data.surahs.length);
        const totalVerses = data.surahs[randomSurahIndex]._c;
        const randomVerse = Math.floor(Math.random() * totalVerses) + 1;
        goto(`/quran/${randomSurahIndex + 1}#v${randomVerse}`);
    }
</script>

<div class="flex flex-col items-center gap-6">
    <div class="w-full flex flex-row justify-between items-center">
        <div class="relative flex items-end">
            <input
                type="text"
                placeholder="Search surah"
                dir={isArabic(searchTextState.value) ? 'rtl' : 'ltr'}
                style:font-family={isArabic(searchTextState.value) ? "'Scheherazade New'" : 'inherit'}
                style:text-align={isArabic(searchTextState.value) ? 'right' : 'left'}
                class="py-2 pl-10 rounded-md border focus:outline-none focus:ring-1 border-slate-300 focus:ring-slate-500 focus:border-transparent"
                bind:value={searchTextState.value}
            />
            <Search
                class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400"
            ></Search>
            {#if searchTextState.value !== ""}
                <span class="pl-2 pb-1 text-slate-500 text-sm">
                    Found {filteredSurahs.length} surahs
                </span>
            {/if}
        </div>
        <button
            onclick={() => gotoRandomVerse()}
            class="flex gap-2 p-2 border rounded-md bg-white border-slate-300 text-slate-500 hover:border-slate-700 hover:text-slate-700"
        >
            <Shuffle class="w-5" />
            Go to random verse
        </button>
        
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 items-center justify-center gap-2 w-full">
        {#each filteredSurahs as ch}
            <a
                class="p-5 border rounded-md md:text-sm flex flex-col justify-between h-full gap-3 border-slate-300 bg-white hover:border-slate-700 group"
                href={`/quran/${ch._n}`}
            >
                <div
                    class="w-full text-center text-xs font-medium text-slate-500"
                >
                    {ch._n}
                </div>
                <div
                    class="w-full text-center text-base font-medium text-slate-800"
                >
                    {ch.en} -
                    <span style="font-family: 'Scheherazade New';"
                        >{ch.ar}</span
                    >
                </div>
                <div class="flex w-full justify-center">
                    <span>{ch._a}</span>
                </div>
                <div class="flex  w-full justify-between text-slate-500 opacity-70 group-hover:opacity-100">
                    <span>{ch._c} <span class="text-xs">verses</span></span>
                    <span class="{ch._l === 'Meccan' ? 'group-hover:text-amber-700' : 'group-hover:text-emerald-700'}">{ch._l}</span>
                </div>
            </a>
        {/each}
    </div>
</div>
