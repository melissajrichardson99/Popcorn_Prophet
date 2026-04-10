<script lang="ts">
  import './router.ts';
  import * as Tooltip from "$lib/components/ui/tooltip/index.js";
  import ArrowUp from "@lucide/svelte/icons/arrow-up";
  import logo from './assets/logo.png'
  import { Button } from "$lib/components/ui/button/index.js";
  import { Router } from 'sv-router';
  import { analytics_state } from "./pages/states.svelte";
  import { isActiveLink } from 'sv-router';

  function go_to_top_of_page() {
    window.scrollTo({top: 0, behavior: "smooth"});
  }
</script>

<main>
    <header class="text-white flex justify-between items-center max-md:items-start max-md:gap-3 border-b border-dark-gray p-5 max-md:flex-col sticky bg-dark-blue top-0 z-[2]">
      <div class="flex items-center gap-3">
        <img src={logo} class="w-10 h-10">
        <a class="hover:text-light-gray active:text-light-blue font-bold text-xl" href="/" use:isActiveLink={{ className: 'text-light-blue' }}>Popcorn Prophet</a>
      </div>
      <ul class="flex gap-10 max-md:self-end">
        <li><a class="hover:text-light-gray active:text-light-blue" href="/data-exploration" use:isActiveLink={{ className: 'text-light-blue' }}>Data Exploration</a></li>
        <li><a class="hover:text-light-gray active:text-light-blue" href="/prediction" use:isActiveLink={{ className: 'text-light-blue', startsWith: true }}>Prediction</a></li>
        <li><a class="hover:text-light-gray active:text-light-blue" href="/analytics" use:isActiveLink={{ className: 'text-light-blue', startsWith: true }}>Analytics</a></li>
      </ul>
    </header>

    <Tooltip.Provider>
      <Router></Router>
    </Tooltip.Provider>

    <div id="overlay" class="fixed top-0 left-0 h-full w-full pointer-events-none">
      <Button 
        class="absolute rounded-4xl right-10 bottom-10 pointer-events-auto transition-opacity ease-in-out 
               {!analytics_state.show_back_to_top_button ? "opacity-0" : "opacity-100"}"
        size="icon" variant="outline" onclick={go_to_top_of_page} title="Back to top">
        <ArrowUp/>
      </Button>
    </div>
</main>

