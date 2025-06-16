<script>
    import { goto } from "$app/navigation";
    import { Search, Shuffle } from "@lucide/svelte";
    import { includesCaseInsensitive, isArabic } from "$lib/utils.js";

    let { data } = $props();
    let searchTextState = $state({value: ""});
    let filteredBooks = $derived.by(() =>{
        let filteredResults = data.books;
        if(searchTextState.value !== ""){
            filteredResults = filteredResults.filter((book) =>
                includesCaseInsensitive(book.BookName, searchTextState.value) ||
                includesCaseInsensitive(book.author, searchTextState.value) ||
                includesCaseInsensitive(book.englishName, searchTextState.value)
            );
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
                placeholder="Search book"
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
                    Found {filteredBooks.length} books
                </span>
            {/if}
        </div>
        <button
            onclick={() => gotoRandomVerse()}
            class="flex gap-2 p-2 border rounded-md bg-white border-slate-300 text-slate-500 hover:border-slate-700 hover:text-slate-700"
        >
            <Shuffle class="w-5" />
            <span class="hidden sm:inline">Go to random hadith</span>
        </button>
    </div>
    <div class="nav-grid grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 items-center justify-center gap-2 w-full">
        {#each filteredBooks as ch, index}
            <a
                class="nav-cell p-5 border rounded-md md:text-sm flex flex-col justify-center h-full gap-3 border-slate-300 bg-white hover:border-slate-700 group"
                href={`/hadith/${index+1}`}
            >
                <img src="{ch.bookCover}" alt="{ch.bookId}" class="w-24 rounded mx-auto shadow-md shadow-slate-300 group-hover:shadow-lg"/>
                <div
                    class="w-full text-center text-base font-medium text-slate-800"
                >
                    {ch.BookName}
                </div>
                <div class="flex w-full justify-center text-center">
                    <span>{ch.author}</span>
                </div>
                <div class="flex w-full justify-between text-slate-500 text-xs opacity-70 group-hover:opacity-100">
                    <span>{ch.englishName}</span>
                    <span>{ch.idRangeMax} hadiths</span>
                </div>
            </a>
        {/each}
    </div>
</div>