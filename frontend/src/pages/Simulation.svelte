<script lang="ts">
  import ArrowDown from "@lucide/svelte/icons/arrow-down";
  import ArrowUp from "@lucide/svelte/icons/arrow-up";
  import Button from "$lib/components/ui/button/button.svelte";
  import CircleQuestionMark from "@lucide/svelte/icons/circle-question-mark";
  import Dropdown from "$lib/components/ui/dropdown/Dropdown.svelte";
  import Input from "$lib/components/ui/input/input.svelte";
  import MaskedInput from "$lib/components/ui/masked-input/MaskedInput.svelte";
  import MultiDropdown from "$lib/components/ui/multi-dropdown/MultiDropdown.svelte";
  import RotateCCW from "@lucide/svelte/icons/rotate-ccw";
  import TriangleAlert from "@lucide/svelte/icons/triangle-alert";
  import { API_URL } from "../const/const";
  import { convert_form_to_body } from "../types/types";
  import { currency_formatter } from "./reuse";
  import { fade, fly } from 'svelte/transition';
  import { form } from "./states.svelte";
  import { navigate, route } from "../router";
  import { onMount, tick } from "svelte";

  let genre_options: Record<string, string> = {
    'A': 'Action',
    'B': 'Adventure',
    'C': 'Animation',
    'D': 'Comedy',
    'E': 'Crime',
    'F': 'Documentary',
    'G': 'Drama',
    'H': 'Family',
    'I': 'Fantasy',
    'J': 'History',
    'K': 'Horror',
    'L': 'Music',
    'M': 'Mystery',
    'N': 'Romance',
    'O': 'Science Fiction',
    'P': 'TV Movie',
    'Q': 'Thriller',
    'R': 'War',
    'S': 'Western',
  }

  let month_options: Record<string, string> = { 
    "1": "January", 
    "2": "February", 
    "3": "March", 
    "4": "April", 
    "5": "May", 
    "6": "June", 
    "7": "July",
    "8": "August", 
    "9": "September", 
    "10": "October", 
    "11": "November", 
    "12": "December" 
  };

  let original_language_options: Record<string, string> = { 
    "en": "English",
    "fr": "French",
    "ru": "Russian",
    "es": "Spanish", 
    "ja": "Japanese", 
    "hi": "Hindi",
    "others": "Others" 
  };

  let vote_count = $state();
  let vote_average = $state();
  let budget = $state();
  let number_of_production_countries = $state();
  let popularity = $state();
  let number_of_production_companies = $state();
  let runtime = $state();
  let number_of_spoken_languages = $state();
  let release_month: string = $state("");
  let original_language: string = $state("");
  let genres: string[] = $state([]);
  let predicted_revenue: number = $state()!;
  let initial_predicted_value: number | undefined = $state();
  let updated_predicted_revenue: number | undefined = $state();
  let revenue_diff: number | null = $state(null);

  let vote_average_errs = $state<Record<string, string>>({});
  let number_of_language_errs = $state<Record<string, string>>({});
  let number_of_production_companies_errs = $state<Record<string, string>>({});
  let number_of_production_countries_errs = $state<Record<string, string>>({});
  let popularity_errs = $state<Record<string, string>>({});
  let vote_count_errs = $state<Record<string, string>>({});
  let runtime_errs = $state<Record<string, string>>({});
  let release_month_errs = $state<Record<string, string>>({});
  let original_language_errs = $state<Record<string, string>>({});
  let genres_errs = $state<Record<string, string>>({});
  let budget_errs = $state<Record<string, string>>({});

  let is_release_month_dirty = $state<boolean>(false);
  let is_original_language_dirty = $state<boolean>(false);
  let vote_average_dirty = $state<boolean>(false);
  let is_number_of_spoken_languages_dirty = $state<boolean>(false);
  let is_runtime_dirty = $state<boolean>(false);
  let is_popularity_dirty = $state<boolean>(false);
  let is_number_of_production_countries_dirty = $state<boolean>(false);
  let is_vote_count_dirty = $state<boolean>(false);
  let is_number_of_production_companies_dirty = $state<boolean>(false);
  let is_genres_dirty = $state<boolean>(false);
  let is_budget_dirty = $state<boolean>(false);

  function check_for_errors() {
    return (
      Object.values(vote_average_errs).length > 0 ||
      Object.values(number_of_language_errs).length > 0 ||
      Object.values(number_of_production_companies_errs).length > 0 ||
      Object.values(number_of_production_countries_errs).length > 0 ||
      Object.values(popularity_errs).length > 0 ||
      Object.values(vote_count_errs).length > 0 ||
      Object.values(runtime_errs).length > 0 ||
      Object.values(release_month_errs).length > 0 ||
      Object.values(original_language_errs).length > 0 ||
      Object.values(genres_errs).length > 0 ||
      Object.values(budget_errs).length > 0
    );
  }

  let original_bar!: HTMLElement;
  let simulated_bar!: HTMLElement;

  function update_bar_height() {
    console.log(revenue_diff, updated_predicted_revenue);
    if (revenue_diff == null && revenue_diff == undefined && updated_predicted_revenue == null && updated_predicted_revenue == undefined) {
      return;
    }
    console.log('run');
    let original_ratio;
    let simulated_ratio;

    if (revenue_diff < 0) {
      original_ratio = 1; 
      simulated_ratio = updated_predicted_revenue / initial_predicted_value;
    } else if (revenue_diff > 0) {
      simulated_ratio = 1;
      original_ratio = initial_predicted_value / updated_predicted_revenue;
    } else {
      simulated_ratio = 1;
      original_ratio = 1;
    }
    original_bar.style.height = `${Math.round(original_ratio * 100)}%`;
    simulated_bar.style.height = `${Math.round(simulated_ratio * 100)}%`;
  }

  onMount(async () => {
    if (!Object.keys(form).length) {
      navigate('/prediction');
      return;
    }

    set_form_from_memory();
  });

  function set_form_from_memory() {
    vote_count = form.vote_count;
    vote_average = form.vote_average;
    budget = form.budget;
    popularity = form.popularity;
    runtime = form.runtime;
    release_month = form.release_month.toString();
    original_language = form.original_language;
    genres = form.genres;
    number_of_production_countries = form.number_of_production_countries;
    number_of_production_companies = form.number_of_production_companies;
    number_of_spoken_languages = form.number_of_spoken_languages;
    predicted_revenue = (route.state as any).predicted_revenue as number;
    initial_predicted_value = predicted_revenue;
    updated_predicted_revenue = undefined;
  }

  function reset_all() {
    set_form_from_memory();
    simulated_bar.style.height = "0%";
    original_bar.style.height = "100%";
    revenue_diff = 0;
    updated_predicted_revenue = 0;
    update_bar_height();
  }

  async function update_prediction() {
    await tick();

    if (check_for_errors()) {
      return;
    }

    const form = {
      vote_count,
      vote_average,
      budget: Number(budget),
      popularity,
      runtime,
      release_month,
      original_language,
      genres: genres.join(""),
      number_of_production_countries,
      number_of_production_companies,
      number_of_spoken_languages,
      predicted_revenue,
    }

    const body = convert_form_to_body(form);

    const res = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    const new_prediction = await res.json();
    updated_predicted_revenue = new_prediction.predicted_revenue;
    predicted_revenue = updated_predicted_revenue!;
    revenue_diff = updated_predicted_revenue! - initial_predicted_value;
    update_bar_height();
  }
</script>

<div class="flex flex-col mx-auto pt-10 px-6 max-w-7xl" id="prediction-wrapper">
  <div class="flex justify-between mb-7">
	  <div>
		  <h1 class="text-white text-3xl font-bold pb-2">Box Office Scenario Simulator</h1>
		  <p class="text-gray-2">Adjust a variable on the left to see its impact on the prediction</p>
	  </div>
  </div>

  <div class="flex flex-col md:flex-row justify-between gap-8 mb-5">
    <div class="bg-dark-blue-3 border border-blue-gray-2 rounded-xl flex flex-col flex-7/20 p-5 pb-6 min-w-0">
      <div class="flex justify-between items-center mb-5">
        <h1 class="text-2xl text-white font-bold">Adjust Variables</h1>
        <Button class="text-gray-2" variant="ghost" onclick={reset_all}>
          <RotateCCW/>
          Reset All
        </Button>
      </div>

      <div class="flex flex-col gap-2 mb-8 relative">
        <label class="text-white">Budget ($)</label>
        <MaskedInput bind:value={budget} bind:errs={budget_errs} bind:is_dirty={is_budget_dirty} required={true} onblur={update_prediction}/>
        {#if is_budget_dirty}
          {#each Object.values(budget_errs) as errMsg}
            <div class="flex items-center gap-1 absolute top-[110%]">
              <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
              <span class="text-red-500 text-sm">{errMsg}</span> 
            </div>
          {/each}
        {/if}
      </div>

      <div class="flex flex-col gap-2 mb-8 relative">
        <label class="text-white">Genres</label>
        <MultiDropdown options={genre_options} bind:errs={genres_errs} bind:is_dirty={is_genres_dirty} bind:value={genres} required={true} on_value_change={update_prediction}/>
        {#if is_genres_dirty}
          {#each Object.values(genres_errs) as errMsg}
            <div class="flex items-center gap-1 absolute top-[110%]">
              <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
              <span class="text-red-500 text-sm">{errMsg}</span> 
            </div>
          {/each}
        {/if}
      </div>

      <div class="flex flex-col gap-2 mb-8 relative">
        <label class="text-white">Release Month</label>
        <Dropdown bind:value={release_month} bind:errs={release_month_errs} bind:is_dirty={is_release_month_dirty} options={month_options} required={true} on_value_change={update_prediction}/>
        {#if is_release_month_dirty}
          {#each Object.values(release_month_errs) as errMsg}
            <div class="flex items-center gap-1 absolute top-[110%]">
              <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
              <span class="text-red-500 text-sm">{errMsg}</span> 
            </div>
          {/each}
        {/if}
      </div>

      <div class="flex flex-col gap-2 mb-8 relative">
        <label class="text-white">Runtime</label>
        <Input type="number" required={true} suffix="mins" bind:is_dirty={is_runtime_dirty} bind:value={runtime} bind:errs={runtime_errs} onblur={update_prediction}/>
        {#if is_runtime_dirty}
          {#each Object.values(runtime_errs) as errMsg}
            <div class="flex items-center gap-1 absolute top-[110%]">
              <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
              <span class="text-red-500 text-sm">{errMsg}</span> 
            </div>
          {/each}
        {/if}
      </div>

      <div class="flex flex-col gap-2 mb-8 relative">
        <label class="text-white">Popularity</label>
        <Input bind:value={popularity} bind:errs={popularity_errs} bind:is_dirty={is_popularity_dirty} required={true} type="number" onblur={update_prediction}/>
        {#if is_popularity_dirty}
          {#each Object.values(popularity_errs) as errMsg}
            <div class="flex items-center gap-1 absolute top-[110%]">
              <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
              <span class="text-red-500 text-sm">{errMsg}</span> 
            </div>
          {/each}
        {/if}
      </div>

      <div class="flex gap-4 mb-8">
        <div class="flex-1 relative flex flex-col gap-2">
          <label class="text-white">Vote Count</label>
          <Input bind:value={vote_count} bind:errs={vote_count_errs} bind:is_dirty={is_vote_count_dirty} required={true} type="number" onblur={update_prediction}/>
          {#if is_vote_count_dirty}
            {#each Object.values(vote_count_errs) as errMsg}
              <div class="flex items-center gap-1 absolute top-[110%]">
                <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
                <span class="text-red-500 text-sm">{errMsg}</span> 
              </div>
            {/each}
          {/if}
        </div>

        <div class="flex-1 relative flex flex-col gap-2">
          <label class="text-white">Vote Average</label>

          <Input min=0 max=10 type="number" bind:value={vote_average} bind:is_dirty={vote_average_dirty} bind:errs={vote_average_errs} required={true} onblur={update_prediction}/>
          {#if vote_average_dirty}
            {#each Object.values(vote_average_errs) as errMsg}
              <div class="flex items-center gap-1 absolute top-[110%]">
                <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
                <span class="text-red-500 text-sm">{errMsg}</span> 
              </div>
            {/each}
          {/if}
        </div>
      </div>

      <div class="flex flex-col gap-2 mb-8 relative">
        <label class="text-white">Original Language</label>

        <Dropdown bind:value={original_language} bind:errs={original_language_errs} bind:is_dirty={is_original_language_dirty} options={original_language_options} required={true} on_value_change={update_prediction}/>
        {#if is_original_language_dirty}
          {#each Object.values(original_language_errs) as errMsg}
            <div class="flex items-center gap-1 absolute top-[110%]">
              <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
              <span class="text-red-500 text-sm">{errMsg}</span> 
            </div>
          {/each}
        {/if}
      </div>

      <div class="flex gap-4">
        <div class="flex-1 flex flex-col gap-2 relative">
          <label class="text-white"># Languages</label>

          <Input bind:value={number_of_spoken_languages} bind:is_dirty={is_number_of_spoken_languages_dirty} bind:errs={number_of_language_errs} required={true} type="number" onblur={update_prediction}/>
          {#if is_number_of_spoken_languages_dirty}
            {#each Object.values(number_of_language_errs) as errMsg}
              <div class="flex items-center gap-1 absolute top-[110%]">
                <span class="text-red-500 text-xs">{errMsg}</span> 
              </div>
            {/each}
          {/if}
        </div>
        <div class="flex-1 flex flex-col gap-2 relative">
          <label class="text-white"># Prod. Comp.</label>

          <Input bind:value={number_of_production_companies} bind:is_dirty={is_number_of_production_companies_dirty} bind:errs={number_of_production_companies_errs} required={true} type="number" onblur={update_prediction}/>
          {#if is_number_of_production_companies_dirty}
            {#each Object.values(number_of_production_companies_errs) as errMsg}
              <div class="flex items-center gap-1 absolute top-[110%]">
                <span class="text-red-500 text-xs">{errMsg}</span> 
              </div>
            {/each}
          {/if}
        </div>

        <div class="flex-1 flex flex-col gap-2 relative">
          <label class="text-white"># Prod. Count.</label>

          <Input bind:value={number_of_production_countries} bind:is_dirty={is_number_of_production_countries_dirty} bind:errs={number_of_production_countries_errs} required={true} type="number" onblur={update_prediction}/>
          {#if is_number_of_production_countries_dirty}
            {#each Object.values(number_of_production_countries_errs) as errMsg}
              <div class="flex items-center gap-1 absolute top-[110%]">
                <span class="text-red-500 text-xs">{errMsg}</span> 
              </div>
            {/each}
          {/if}
        </div>
      </div>
    </div>

    <div class="flex-13/20 flex flex-col">
      <div class="bg-dark-blue-3 border border-blue-gray-2 rounded-xl p-7 mb-7">
        <p class="text-gray-2 mb-3">Predicted Worldwide Box Office</p>
        <div class="flex gap-2">
          <p class="text-white font-extrabold text-4xl">{currency_formatter.format(predicted_revenue)}</p>
          {#if revenue_diff}
            <div class="flex gap-1 {revenue_diff > 0 ? "text-light-green" : "text-light-red"} font-extrabold self-end pb-1" in:fly={{ y: 200, duration: 2000 }} out:fade>
                {#if revenue_diff > 0}
                  <ArrowUp/>
                {:else}
                  <ArrowDown/>
                {/if}
                <span>{currency_formatter.format(revenue_diff)}</span>
            </div>
          {/if}
        </div>
      </div>
      <div class="bg-dark-blue-3 border border-blue-gray-2 rounded-xl flex flex-col flex-1 p-7">
        <p class="text-white font-bold mb-3">Original vs. Simulated Revenue</p>
        <div class="flex text-white h-full">
          <div class="flex flex-col flex-1 bg-blue items-center h-full">
            <div class="flex-1 flex flex-col">
              <div class="w-20 bg-blue-gray-2 mt-auto rounded-t-lg transition-all ease-in-out h-full" bind:this={original_bar}>
              </div>
            </div>
            <span class="text-light-gray mb-2">Original</span>
            <span>{currency_formatter.format(initial_predicted_value)}</span>
          </div>
          <div class="flex flex-col flex-1 items-center h-full ">
            <div class="flex-1 flex flex-col">
              <div class="w-20 bg-light-blue mt-auto rounded-t-lg transition-all ease-in-out" bind:this={simulated_bar}>
              </div>
            </div>
            <span class="mb-2">Simulated</span>
            <span>{updated_predicted_revenue ? currency_formatter.format(updated_predicted_revenue) : "-"}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
