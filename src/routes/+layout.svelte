<script>
    import "../app.css";
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import { goto } from "$app/navigation";
    import { Keyboard, LogOut } from "@lucide/svelte";
    import HarfBoard from "$lib/HarfBoard.svelte";

    let { children } = $props();
    let harfBoardOpen = $state(false);

    function handleGlobalKey(event) {
        const target = event.target;
        const tag = target?.tagName;
        const isTyping = tag === 'INPUT' || tag === 'TEXTAREA' || target?.isContentEditable;

        if (!isTyping && event.key === 'a') {
            harfBoardOpen = true;
        }
    }

    onMount(() => {
        window.addEventListener("keydown", handleGlobalKey);
        return () => {
            window.removeEventListener("keydown", handleGlobalKey);
        };
    });
</script>

<button
    class="fixed top-5 left-5 z-50"
    onclick={() => harfBoardOpen = true}
    title="Harfboard"
>
    <Keyboard class="w-6 h-6 text-slate-300 hover:text-slate-500" />
</button>
<div
    id="container"
    class="lg:w-3/4 mx-auto mt-8 px-3 flex flex-col items-center gap-4"
>
    <a href="/">
        <img
            id="logo"
            src="/ahlulbayt.svg"
            alt="Logo"
            class="h-16 mb-4 shadow-lg rounded-md shadow-slate-300 hover:shadow-none hover:outline-[#F9DBBB] hover:outline"
        />
    </a>
    <div class="w-full gap-2 flex flex-col">
        <nav
            id="nav"
            class="w-full flex flex-row items-center justify-center gap-6"
        >
            <a
                href="/quran"
                class="hover:underline {$page.url.pathname.startsWith(`/quran`)
                    ? 'text-slate-900'
                    : 'text-slate-500'}">Qur'an</a
            >
            <a
                href="/hadith"
                class="hover:underline {$page.url.pathname.startsWith(`/hadith`)
                    ? 'text-slate-900'
                    : 'text-slate-500'}">Hadith</a
            >
            <a
                href="/fiqh"
                class="hover:underline {$page.url.pathname.startsWith(`/fiqh`)
                    ? 'text-slate-900'
                    : 'text-slate-500'}">Fiqh</a
            >
            <a
                href="/tools"
                class="hover:underline {$page.url.pathname.startsWith(`/tools`)
                    ? 'text-slate-900'
                    : 'text-slate-500'}">Tools</a
            >
        </nav>
        {@render children()}
    </div>
</div>
<button
    class="fixed top-5 right-5 z-50"
    onclick={() => console.log()}
    title="Logout"
>
    <LogOut class="w-6 h-6 text-slate-300 hover:text-slate-500" />
</button>

<HarfBoard bind:open={harfBoardOpen} on:close={() => (harfBoardOpen = false)} />