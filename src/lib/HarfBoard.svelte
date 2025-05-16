<script>
    import { onMount, onDestroy } from "svelte";
    import { createEventDispatcher } from "svelte";
    
    const { open = false } = $props();
    const dispatch = createEventDispatcher();

    function handleKey(event) {
        if (event.key === "Escape") {
            dispatch("close");
        }
    }

    function handleClickOutside(event) {
        const target = event.target;
        if (target?.closest("#hf-container")) return;
        dispatch("close");
    }

    function isValidString(str) {
        return typeof str?.trim === 'function' && str.trim() !== '';
    }

    onMount(() => {
        const textbox = document.getElementById('hf-textbox');
        const arabKeys = {
            "a": "ا",
            "b": "ب",
            "p": "پ",
            "t": "ت",
            "c": "ث",
            "j": "ج",
            "H": "ح",
            "R": "خ",
            "d": "د",
            "C": "ذ",
            "r": "ر",
            "z": "ز",
            "s": "س",
            "x": "ش",
            "S": "ص",
            "D": "ض",
            "T": "ط",
            "Z": "ظ",
            "g": "ع",
            "G": "غ",
            "f": "ف",
            "q": "ق",
            "k": "ك",
            "K": "گ",
            "l": "ل",
            "m": "م",
            "n": "ن",
            "h": "ه",
            "w": "و",
            "i": "ي",
            "e": "ة",
            "y": "ي",
            "Y": "ى",
            "A": "أ",
            "o": "و",
            "O": "ؤ",
            "E": "إ",
            "I": "ئ",
            "u": "ء",
            ",": "،",
            "?": "؟",
        };
        let changes = [];
        let lastChange = 0;
        const TYPING_THRESHOLD = 1000;

        textbox.addEventListener('beforeinput', function (event) {
            const letter = event.data;

            if (letter && arabKeys[letter]) {
                event.preventDefault();

                const start = textbox.selectionStart;
                const end = textbox.selectionEnd;
                const arabLetter = arabKeys[letter];
                const newValue = textbox.value.slice(0, start) + arabLetter + textbox.value.slice(end);

                textbox.value = newValue;
                textbox.setSelectionRange(start + arabLetter.length, start + arabLetter.length);
            }
        });

        textbox.addEventListener('input', function (event) {
            textbox.style.height = "auto";
            textbox.style.height = textbox.scrollHeight + "px";

            const currentValue = event.target.value;
            const currentTime = Date.now();
            if (isValidString(currentValue)) {
                changes[changes.length - (currentTime - lastChange <= TYPING_THRESHOLD)] = currentValue;
                lastChange = currentTime;
            }
        });

        textbox.addEventListener('keydown', function (event) {
            if (event.ctrlKey && event.key === 'z') {
                event.preventDefault();
                changes.pop();
                textbox.value = changes.at(-1) || '';
            }
        });
        window.addEventListener("keydown", handleKey);
        return () => window.removeEventListener("keydown", handleKey);
    });
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="fixed {open ? '' : 'hidden'} inset-0 z-50 flex items-center justify-center backdrop-blur-sm" onclick={handleClickOutside}>
    <div
        id="hf-container"
        class="lg:w-3/4 2xl:w-1/2 mx-auto mt-8 px-4 flex flex-col items-center"
        style="font-family: 'Geist';"
    >
        <div
            class="w-full mb-4 border border-slate-300 rounded-lg bg-gray-50 shadow-lg shadow-slate-200"
        >
            <div class="py-2 bg-white rounded-t-lg">
                <textarea
                    id="hf-textbox"
                    rows="1"
                    style="font-family: 'Scheherazade New';"
                    class="resize-none w-full text-2xl px-4 py-2 text-slate-900 caret-slate-400 bg-white border-0 focus:ring-0 focus:outline-none"
                    dir="rtl"
                    autocomplete="off"
                    autocorrect="off"
                    autocapitalize="off"
                    spellcheck="false"
                ></textarea>
                <div
                    id="hf-transliterate-content"
                    class="hidden w-full text-2xl px-4 py-2 text-slate-500 caret-slate-400 bg-white border-t border-slate-300"
                >
                    <i
                        id="hf-transliterate-spinner"
                        class="fa fa-spinner fa-spin mx-auto"
                        aria-hidden="true"
                    ></i>
                    <span id="hf-textbox-transliterate"></span>
                </div>
            </div>
            <div
                class="flex flex-col justify-center items-center gap-2 border-t border-slate-200"
            >
                <div
                    class="border-b border-gray-200 w-full px-2 py-6 flex flex-col items-center"
                >
                    <div
                        class="flex flex-wrap flex-row-reverse w-4/5 justify-center gap-2"
                        id="hf-keyboard"
                    >
                        {#each Object.entries(arabKeys) as [key, value]}
                            <div class="flex flex-col items-center gap-1">
                                <span class="text-xs font-semibold text-slate-500">{key}</span>
                                <button class="py-2 w-16 font-semibold text-slate-800 bg-white border border-slate-300 rounded-md shadow-xs" style="font-family: Scheherazade New;">{value}</button>
                            </div>
                        {/each}
                    </div>
                </div>
                <!-- <div
                    class="flex justify-center items-center gap-2 px-2 py-6 w-4/5"
                >
                    <button
                        id="hf-transliterate-button"
                        class="px-4 py-2 rounded-md gap-1 cursor-pointer bg-white border border-slate-300 text-slate-500 hover:text-slate-700 hover:border-slate-700 disabled:opacity-25 disabled:cursor-not-allowed"
                        type="button"
                        disabled={textbox.length === 0}
                    >
                        Transliterate
                    </button>
                </div> -->
            </div>
        </div>
    </div>
</div>