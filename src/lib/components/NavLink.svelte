<script>
    import { page } from '$app/stores';
    const { url, name } = $props();
    let isActive = $derived($page.url.pathname.startsWith(`/${url}`));
  </script>
  

<a href="/{url}" class="hover:underline {isActive ? 'text-slate-900' : 'text-slate-500'}">{name}</a>