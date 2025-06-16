<script>
    let { data } = $props();
</script>

<svelte:head>
    <title>Notes - Ahlulbayt.io</title> 
</svelte:head>

<div class="w-1/2 mx-auto">
    <h2 class="text-center">Notes</h2>
    <ul>
    {#each data.notes as item}
        <li><a class="text-slate-600 hover:underline hover:text-sky-500" href="/notes/{item.id}">{item.name}</a></li>
    {/each}
    </ul>
</div>