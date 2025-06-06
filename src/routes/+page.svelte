<script>
    import "../app.css";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";

    let clicks = $state(0);

    function handleImageClick() {
        clicks++;
        if (clicks === 5) {
            goto("/quran");
        }
    }

    function handleGlobalKey() {
        if (event.key === 'e') {
            goto('/quran');
        }
    }

    onMount(() => {
        window.addEventListener("keydown", handleGlobalKey);
        return () => {
            window.removeEventListener("keydown", handleGlobalKey);
        };
    });
</script>

<svelte:head>
    <title>Ahlulbayt.io</title>
</svelte:head>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
<img
    onclick={handleImageClick}
    src="/kisa.webp"
    class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 max-w-full h-80 rounded-full shadow-xl shadow-slate-400 outline-[#F9DBBB] outline opacity-80"
    alt="Logo"
/>
