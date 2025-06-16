<script>
    import { onMount } from "svelte";
    import { Search, ChevronLeft, ChevronRight, Copy, Link } from "@lucide/svelte";
    import { toArabicNumber, isArabic, includesCaseInsensitive, boldMatchedWord } from "$lib/utils";
    const { data } = $props();

    let searchTextState = $state({ value: "" });
    let filteredHadiths = $derived.by(() => {
        let filteredResults = data.chapter.hadiths;
        if (searchTextState.value !== "") {
            filteredResults = filteredResults.filter(
                (hadith) =>
                    includesCaseInsensitive(hadith.arabicText, searchTextState.value) ||
                    includesCaseInsensitive(hadith.englishText, searchTextState.value),
            );
            filteredResults = filteredResults.map((hadith) => {
                return {
                    ...hadith,
                    arabicText: boldMatchedWord(hadith.arabicText, searchTextState.value),
                    englishText: boldMatchedWord(hadith.englishText, searchTextState.value),
                };
            });
        }
        return filteredResults;
    });
    
</script>

<div class="relative mb-6 md:mb-0">
    <input
        id="search-input"
        type="text"
        placeholder="Search hadith"
        dir={isArabic(searchTextState.value) ? "rtl" : "ltr"}
        style:font-family={isArabic(searchTextState.value)
            ? "'Scheherazade New'"
            : "inherit"}
        style:text-align={isArabic(searchTextState.value) ? "right" : "left"}
        class="py-2 pl-10 rounded-md border focus:outline-none focus:ring-1 border-slate-300 focus:ring-slate-500 focus:border-transparent"
        bind:value={searchTextState.value}
    />
    <Search
        class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400"
    ></Search>
</div>
<div class="flex flex-col items-center justify-center text-slate-700 mb-8 mt-8">
    <div class="font-bold">{data.chapter.chapter}</div>
</div>
<!-- <div class="mt-4 flex flex-row justify-between text-sm text-slate-500">
    {#if previousSurah}
    <div class="flex items-center hover:underline">
        <ChevronLeft class="w-4" />
        <a href={`/quran/${previousSurah._n}`}><span style="font-family: 'Amiri'">{previousSurah.arabicText}</span> - {previousSurah._a}</a>
    </div>
    {:else}
        <span></span>
    {/if}
    {#if nextSurah}
        <div class="flex items-center hover:underline">
            <a href={`/quran/${nextSurah._n}`}><span style="font-family: 'Amiri'">{nextSurah.arabicText}</span> - {nextSurah._a}</a>
            <ChevronRight class="w-4"/>
        </div>
    {:else}
        <span></span>
    {/if}
</div> -->
<div
    class="mx-auto flex flex-col mb-8 bg-zinc-50 border rounded-md shadow-slate-200 border-slate-300 relative"
>
    <div
        class="hidden sm:block absolute -top-6 z-50 left-1/2 transform -translate-x-1/2 border px-10 py-2 rounded text-lg bg-zinc-50 text-slate-700"
        style={searchTextState.value === "" ? "font-family: 'Amiri'" : ""}
    >
        {searchTextState.value === ""
            ? `${filteredHadiths.length} hadiths`
            : `${filteredHadiths.length} results found for "${searchTextState.value}"`}
    </div>
    {#each filteredHadiths as hadith, i}
    <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
    <div
        tabindex="0"
        class="flex flex-col py-6 px-8 {i === 0 ? 'pt-8' : ''} gap-6 {i === filteredHadiths.length - 1 ? '' : 'border-b'} border-slate-200 relative focus:outline-none focus:ring-1 focus:ring-slate-500 focus:bg-slate-100 focus:rounded-sm"
    >
        <div
            class="absolute flex flex-col gap-1 top-1 left-1 px-2 py-2 rounded text-lg text-slate-300"
            style="font-family: 'Amiri'"
        >
            <Copy class="w-4 hover:text-slate-500 cursor-pointer"/>
            <Link class="w-4 hover:text-slate-500 cursor-pointer"/>
        </div>
        <div class="text-center text-slate-400">{i+1}</div>
        <div
            class="text-right text-xl leading-10"
            style="font-family: 'Scheherazade New';"
        >
            {@html hadith.arabicText}
        </div>
        <div class="font-light text-slate-600">{@html hadith.englishText}</div>
    </div>
    {/each}
</div>