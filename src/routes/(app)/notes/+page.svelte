<script>
    let { data } = $props();
</script>

<svelte:head>
    <title>Notes - Ahlulbayt.io</title>
</svelte:head>

<div class="mx-auto">
    <h2 class="text-center">Notes</h2>

    <div
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 md:flex-row items-center justify-center gap-2 w-full"
    >
        {#each Object.entries(data.notes) as [key, item]}
            <a
                class="p-5 border rounded-md md:text-sm flex flex-col justify-between h-full gap-3 border-slate-300 bg-white hover:border-slate-700 group"
                href={`/notes/${key}`}
            >
                <div
                    class="w-full text-center text-base font-medium text-slate-800"
                >
                    {item.title}
                </div>
            </a>
        {/each}
    </div>
</div>
