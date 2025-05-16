<script>
    import { onMount } from 'svelte';
    import { ArrowUpToLine } from "@lucide/svelte";
    
    let containerEl;
    let { children } = $props();
    let showButton = $state(false);
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
