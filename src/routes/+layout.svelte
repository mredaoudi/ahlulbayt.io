<script>
    import "../app.css";
    import { onMount } from 'svelte';
    import { page } from "$app/stores";
    import NavLink from "$lib/components/NavLink.svelte";
    import { goto } from "$app/navigation";
    import { ArrowUpToLine } from "@lucide/svelte";
    let { children } = $props();

    let showButton = $state(false);

    let containerEl;
    let buttonWrapperLeft = $state("0px");

    function updateButtonPosition() {
        if (containerEl) {
            const rect = containerEl.getBoundingClientRect();
            const buttonOffset = rect.left + rect.width; // right edge of container
            buttonWrapperLeft = `${buttonOffset + 16}px`; // 16px margin
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

    onMount(() => {
        updateButtonPosition();
        handleScrollOrResize();

        window.addEventListener("scroll", handleScrollOrResize);
        window.addEventListener("resize", handleScrollOrResize);

        return () => {
            window.removeEventListener("scroll", handleScrollOrResize);
            window.removeEventListener("resize", handleScrollOrResize);
        };
    });

    function scrollToTop() {
        window.scrollTo({ top: 0, behavior: "smooth" });
    }
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
            <NavLink url="quran" name="Qur'an" />
            <NavLink url="hadith" name="Hadith" />
            <NavLink url="fiqh" name="Fiqh" />
            <NavLink url="tools" name="Tools" />
        </nav>
        <div
            bind:this={containerEl}
            class="mb-4 p-4 border rounded-lg shadow-lg border-slate-300 bg-gray-50 shadow-slate-200 text-slate-900"
        >
            {@render children()}
        </div>
    </div>
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
