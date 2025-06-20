<script>
    let tools = [
        {
            englishName: "Prayer Times",
            url: "/tools/prayer-times"
        },
        {
            englishName: "Resources",
            url: "/tools/resources"
        }
    ]
</script>

<svelte:head>
    <title>Tools - Ahlulbayt.io</title> 
</svelte:head>

<h2 class="text-center">Tools</h2>
<div
    class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 md:flex-row items-center justify-center gap-2 w-full"
>
    {#each tools as tool}
        <a
            class="p-5 border rounded-md md:text-sm flex flex-col justify-between h-full gap-3 border-slate-300 bg-white hover:border-slate-700 group"
            href={`${tool.url}`}
        >
            <div
                class="w-full text-center text-base font-medium text-slate-800"
            >
                {tool.englishName}
            </div>
        </a>
    {/each}
</div>