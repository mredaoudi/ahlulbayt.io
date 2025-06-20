<script>
    import { goto } from "$app/navigation";
    import { Search, Shuffle } from "@lucide/svelte";
    import { includesCaseInsensitive, isArabic, getRandomNumberInRange } from "$lib/utils.js";

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

    async function gotoRandomVerse() {
        const randomSurahIndex = await getRandomNumberInRange(1, 114);
        const totalVerses = data.surahs[randomSurahIndex - 1]._c;
        const randomVerse = await getRandomNumberInRange(1, totalVerses);
        goto(`/quran/${randomSurahIndex}#e${randomVerse}`);
    }
</script>

<svelte:head>
    <title>Qur'an - Ahlulbayt.io</title> 
</svelte:head>

<div class="flex flex-col items-center gap-6">
    <div class="w-full flex justify-between items-center gap-1">
        <div class="relative flex items-end">
            <input
                id="search-input"
                type="text"
                placeholder="Search surah"
                dir={isArabic(searchTextState.value) ? 'rtl' : 'ltr'}
                style:font-family={isArabic(searchTextState.value) ? "'Scheherazade New'" : 'inherit'}
                style:text-align={isArabic(searchTextState.value) ? 'right' : 'left'}
                class="py-2 pl-10 rounded-md border w-full focus:outline-none  focus:ring-1 border-slate-300 focus:ring-slate-500 focus:border-transparent"
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
            onclick={async () => await gotoRandomVerse()}
            class="flex gap-2 p-2 border rounded-md bg-white border-slate-300 text-slate-500 hover:border-slate-700 hover:text-slate-700"
        >
            <Shuffle class="w-5" />
            <span class="hidden sm:inline">Go to random verse</span>
        </button>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 items-center justify-center gap-2 w-full">
        {#each filteredSurahs as ch}
            <a
                id="e{ch._n}"
                class="p-5 border rounded-md md:text-sm flex flex-col justify-between h-full gap-3 border-slate-300 bg-white hover:border-slate-700 group"
                href={`/quran/${ch._n}`}
            >
                <div
                    class="w-full text-center text-xs font-medium text-slate-500"
                >
                    {ch._n}
                </div>
                <div class="w-full text-center text-base font-medium text-slate-800">{ch.en}</div>
                <div class="w-full text-center font-medium text-slate-800" style="font-family: 'Scheherazade New';">{ch.ar}</div>
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
