<script>
    let { data } = $props();
</script>

<svelte:head>
    <title>Notes - Ahlulbayt.io</title> 
</svelte:head>

<div class="mx-auto border border-slate-300 rounded-md px-16 py-4 bg-stone-50" style="font-family: 'Crimson Text';">
    {@html data.note}
</div>