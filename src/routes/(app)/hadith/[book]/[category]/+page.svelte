<script>
    import { page } from "$app/state";
    import { goto } from "$app/navigation";
    import { Search, Shuffle } from "@lucide/svelte";
    import { includesCaseInsensitive, isArabic } from "$lib/utils.js";

    const { data } = $props();
    let searchTextState = $state({value: ""});
    let filteredChapters = $derived.by(() => {
        let filteredResults = Object.values(data.category.chapters).map(chap => {
            return {
                chapter: chap.chapter,
                hadithCount: chap.hadiths.length
            }
        });
        if(searchTextState.value !== ""){
            filteredResults = filteredResults.filter((cat) =>
                includesCaseInsensitive(cat.category, searchTextState.value)
            )
        }
        return filteredResults;
    });
</script>

<svelte:head>
    <title>Hadith - Ahlulbayt.io</title> 
</svelte:head>

<div class="flex flex-col items-center gap-6">
    <div class="w-full flex justify-between items-center gap-1">
        <div class="relative flex items-end">
            <input
                id="search-input"
                type="text"
                placeholder="Search category"
                dir={isArabic(searchTextState.value) ? 'rtl' : 'ltr'}
                style:font-family={isArabic(searchTextState.value) ? "'Scheherazade New'" : 'inherit'}
                style:text-align={isArabic(searchTextState.value) ? 'right' : 'left'}
                class="py-2 pl-10 rounded-md border w-full focus:outline-none focus:ring-1 border-slate-300 focus:ring-slate-500 focus:border-transparent"
                bind:value={searchTextState.value}
            />
            <Search
                class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400"
            ></Search>
            {#if searchTextState.value !== ""}
                <span class="pl-2 pb-1 text-slate-500 text-sm">
                    Found {filteredChapters.length} books
                </span>
            {/if}
        </div>
        <div class="text-slate-700">
            {data.book.BookName} 
        </div>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4  items-center justify-center gap-2 w-full">
        {#each filteredChapters as ch, index}
            <a
                class="p-5 border rounded-md md:text-sm flex flex-col justify-center h-36 gap-3 border-slate-300 bg-white hover:border-slate-700 group"
                href={`/hadith/${page.params.book}/${page.params.category}/${index+1}`}
            >
                <div
                    class="w-full text-center text-base font-medium text-slate-800 overflow-y-scroll"
                >
                    {ch.chapter}
                </div>
                <div class="flex w-full justify-center text-slate-500 text-xs opacity-70 group-hover:opacity-100">
                    <span>{ch.hadithCount} hadiths</span>
                </div>
            </a>
        {/each}
    </div>
</div>