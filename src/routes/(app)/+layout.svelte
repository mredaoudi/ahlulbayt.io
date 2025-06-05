<script>
    import { page } from "$app/stores";
    import { goto } from "$app/navigation";
    import { tick, onMount } from "svelte";
    import HarfBoard from "$lib/HarfBoard.svelte";
    import { Keyboard, LogOut, ArrowUpToLine } from "@lucide/svelte";

    let containerEl;
    let { children } = $props();
    let showButton = $state(false);
    let harfBoardOpen = $state(false);
    let buttonWrapperLeft = $state("0px");

    function updateButtonPosition() {
        if (containerEl) {
            const rect = containerEl.getBoundingClientRect();
            const buttonOffset = rect.left + rect.width;
            buttonWrapperLeft = `${buttonOffset + 16}px`;
        }
    }

    function handleScrollOrResize() {
        const scrollY = window.scrollY;
        const pageHeight = document.documentElement.scrollHeight;
        const screenHeight = window.innerHeight;

        const isPageTallEnough = pageHeight > screenHeight * 2;
        const hasScrolledDownEnough = scrollY > 400;

        showButton = isPageTallEnough && hasScrolledDownEnough;

        updateButtonPosition();
    }

    function closeHarfBoard() {
        const textbox = document.getElementById('hf-textbox');
        textbox.value = "";
        harfBoardOpen = false;
    }

    function scrollToTop() {
        window.scrollTo({ top: 0, behavior: "smooth" });
    }

    function unfocusAll() {
        if (document.activeElement instanceof HTMLElement) {
            document.activeElement.blur();
        }
        document.body.focus();
    }

    async function handleGlobalKey(event) {
        const target = event.target;
        const tag = target?.tagName;
        const isTyping = tag === 'INPUT' || tag === 'TEXTAREA' || target?.isContentEditable;

        if (!isTyping) {
            if (event.key === 'h') {
                harfBoardOpen = true;
                const textbox = document.getElementById('hf-textbox');
                await tick();
                event.preventDefault();
                textbox.focus();
            } else if (event.key === 'q') {
                goto('/quran');
            } else if (event.key === 'h') {
                goto('/hadith');
            } else if (event.key === 's') {
                const input = document.getElementById('search-input');
                if (input) {
                    event.preventDefault();
                    input.focus();
                }
            } 
        }
        if (event.key === 'Escape') {
            unfocusAll();
        }
    }

    onMount(() => {
        handleScrollOrResize();
        
        window.addEventListener("keydown", handleGlobalKey);
        window.addEventListener("scroll", handleScrollOrResize);
        window.addEventListener("resize", handleScrollOrResize);
        return () => {
            window.removeEventListener("keydown", handleGlobalKey);
            window.removeEventListener("scroll", handleScrollOrResize);
            window.removeEventListener("resize", handleScrollOrResize);
        };
    });
</script>

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
        <div
            bind:this={containerEl}
            class="mb-4 p-4 border rounded-lg shadow-lg border-slate-300 bg-gray-50 shadow-slate-200 text-slate-900"
        >
            {@render children()}
        </div>
        {#if showButton}
            <div class="fixed bottom-6 z-50" style="left: {buttonWrapperLeft};">
                <button
                    onclick={scrollToTop}
                    class=" px-2 py-2 rounded-md shadow-md transition-all duration-300 border bg-white border-slate-300"
                >
                    <ArrowUpToLine class="w-6 h-6 text-slate-500" />
                </button>
            </div>
        {/if}
    </div>
</div>

<HarfBoard bind:open={harfBoardOpen} on:close={() => closeHarfBoard()} />