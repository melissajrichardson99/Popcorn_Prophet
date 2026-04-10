<script lang="ts">
  import * as Tooltip from "$lib/components/ui/tooltip/index.js";
  import CircleQuestionMark from "@lucide/svelte/icons/circle-question-mark";
  import Dropdown from "$lib/components/ui/dropdown/Dropdown.svelte";
  import Input from "$lib/components/ui/input/input.svelte";
  import MaskedInput from "$lib/components/ui/masked-input/MaskedInput.svelte";
  import MultiDropdown from "$lib/components/ui/multi-dropdown/MultiDropdown.svelte";
  import TrendingUpNow from "@lucide/svelte/icons/trending-up-down";
  import TriangleAlert from "@lucide/svelte/icons/triangle-alert";
  import { Button } from "$lib/components/ui/button/index.js";
  import { form } from "./states.svelte";
  import { navigate } from "../router";
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
  let genres: string[] = $state([]);
  let original_language: string = $state("");

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

  let this_form: HTMLFormElement | null = null;

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

  async function predict(e: SubmitEvent) {
    e.preventDefault();

    is_release_month_dirty = true;
    is_original_language_dirty = true;
    vote_average_dirty = true;
    is_number_of_spoken_languages_dirty = true;
    is_runtime_dirty = true;
    is_popularity_dirty = true;
    is_number_of_production_countries_dirty = true;
    is_vote_count_dirty = true;
    is_number_of_production_companies_dirty = true;
    is_genres_dirty = true;
    is_budget_dirty = true;

    await tick();

    if (check_for_errors()) {
      const first_form_field_with_error = this_form!.querySelector(`[aria-invalid="true"]`) as HTMLElement;
      first_form_field_with_error.focus()
      return;
    }

    form.vote_count = vote_count; 
    form.vote_average = vote_average; 
    form.budget = budget; 
    form.number_of_production_countries = number_of_production_countries;
    form.number_of_production_companies = number_of_production_companies; 
    form.number_of_spoken_languages = number_of_spoken_languages; 
    form.popularity = popularity; 
    form.runtime = runtime; 
    form.release_month = release_month; 
    form.original_language = original_language;
    form.genres = genres;

    navigate('/prediction/result', { viewTransition: true });
  }

  onMount(() => {
    if (Object.values(form).length > 0) {
      vote_count = form.vote_count; 
      vote_average = form.vote_average;
      budget = form.budget; 
      number_of_production_countries = form.number_of_production_countries;
      number_of_production_companies = form.number_of_production_companies; 
      number_of_spoken_languages = form.number_of_spoken_languages; 
      popularity = form.popularity; 
      runtime = form.runtime; 
      release_month = form.release_month; 
      original_language = form.original_language;
      genres = form.genres;
    }
  });
</script>

<div class="max-w-5xl mx-auto py-10 flex flex-col px-6" id="prediction-wrapper">
  <h1 class="text-white text-4xl font-bold pb-3 text-center">Predict Your Movie's Box Office Revenue</h1>
  <p class="text-gray-2 pb-7 text-center">Enter movie details to predict its success</p>

  <form class="flex flex-col bg-dark-blue-3 border border-blue-gray-2 rounded-xl px-8 py-5 gap-8" bind:this={this_form}>
    <div class="flex gap-8 md:gap-4 flex-col md:flex-row"> 
      <div class="flex-1 flex flex-col gap-2 relative">
        <div class="flex gap-1">
          <label class="text-white">Budget</label> 
          <Tooltip.Root>
            <Tooltip.Trigger>
              <CircleQuestionMark color="white"></CircleQuestionMark>
            </Tooltip.Trigger>
            <Tooltip.Content>
              TMDB budget represents the production cost of a movie, reported in US dollars. It has a minimum of 0, no fixed maximum.
            </Tooltip.Content>
          </Tooltip.Root>
        </div>
        <MaskedInput bind:value={budget} bind:errs={budget_errs} bind:is_dirty={is_budget_dirty} required={true}/>
        {#if is_budget_dirty}
          {#each Object.values(budget_errs) as errMsg}
            <div class="flex items-center gap-1 absolute top-[110%]">
              <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
              <span class="text-red-500 text-sm">{errMsg}</span> 
            </div>
          {/each}
        {/if}
      </div>

      <div class="flex-1 flex flex-col gap-2 relative">
        <div class="flex gap-1">
          <label class="text-white">Vote Average</label>
          <Tooltip.Root>
            <Tooltip.Trigger>
              <CircleQuestionMark color="white"></CircleQuestionMark>
            </Tooltip.Trigger>
            <Tooltip.Content>
              TMDB vote average is the mean user rating for a movie based on submitted votes.
              <br/>
              It is bounded between 0 and 10, typically shown to one decimal place.
            </Tooltip.Content>
          </Tooltip.Root>
        </div>

        <Input min=0 max=10 type="number" bind:value={vote_average} bind:is_dirty={vote_average_dirty} bind:errs={vote_average_errs} required={true}/>
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

    <div class="flex gap-8 md:gap-4 flex-col md:flex-row"> 
      <div class="flex-1 flex flex-col gap-2 relative min-w-0">
        <div class="flex gap-1">
          <label class="text-white">Genres</label> 
          <Tooltip.Root>
            <Tooltip.Trigger>
              <CircleQuestionMark color="white"></CircleQuestionMark>
            </Tooltip.Trigger>
            <Tooltip.Content>
              TMDB genres describe the thematic categories a movie belongs to, such as Action or Drama. They are categorical and multi-valued.
            </Tooltip.Content>
          </Tooltip.Root>
        </div>

        <MultiDropdown options={genre_options} bind:errs={genres_errs} bind:is_dirty={is_genres_dirty} bind:value={genres} required={true}/>
        {#if is_genres_dirty}
          {#each Object.values(genres_errs) as errMsg}
            <div class="flex items-center gap-1 absolute top-[110%]">
              <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
              <span class="text-red-500 text-sm">{errMsg}</span> 
            </div>
          {/each}
        {/if}
      </div>

       <div class="flex-1 flex flex-col gap-2 relative">
        <div class="flex gap-1">
          <label class="text-white">Original Language</label>
          <Tooltip.Root>
            <Tooltip.Trigger>
              <CircleQuestionMark color="white"></CircleQuestionMark>
            </Tooltip.Trigger>
            <Tooltip.Content>
              The primary language in which a movie was originally produced
            </Tooltip.Content>
          </Tooltip.Root>
        </div>

        <Dropdown bind:value={original_language} bind:errs={original_language_errs} bind:is_dirty={is_original_language_dirty} options={original_language_options} required={true}/>
        {#if is_original_language_dirty}
          {#each Object.values(original_language_errs) as errMsg}
            <div class="flex items-center gap-1 absolute top-[110%]">
              <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
              <span class="text-red-500 text-sm">{errMsg}</span> 
            </div>
          {/each}
        {/if}
      </div>
    </div>

    <div class="flex gap-8 md:gap-4 flex-col md:flex-row"> 
     <div class="flex-1 flex flex-col gap-2 relative">
        <div class="flex gap-1">
          <label class="text-white">Release Month</label> 
          <Tooltip.Root>
            <Tooltip.Trigger>
              <CircleQuestionMark color="white"></CircleQuestionMark>
            </Tooltip.Trigger>
            <Tooltip.Content>
              TMDB release date is the calendar date when a movie was first released to the public.
            </Tooltip.Content>
          </Tooltip.Root>
        </div>

        <Dropdown bind:value={release_month} bind:errs={release_month_errs} bind:is_dirty={is_release_month_dirty} options={month_options} required={true}/>
        {#if is_release_month_dirty}
          {#each Object.values(release_month_errs) as errMsg}
            <div class="flex items-center gap-1 absolute top-[110%]">
              <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
              <span class="text-red-500 text-sm">{errMsg}</span> 
            </div>
          {/each}
        {/if}
      </div>

      <div class="flex-1 flex flex-col gap-2 relative">
        <div class="flex gap-1">
          <label class="text-white">Number of Languages</label> 
          <Tooltip.Root>
            <Tooltip.Trigger>
              <CircleQuestionMark color="white"></CircleQuestionMark>
            </Tooltip.Trigger>
            <Tooltip.Content>
              Total number of languages spoken in the movie
            </Tooltip.Content>
          </Tooltip.Root>
        </div>

        <Input bind:value={number_of_spoken_languages} bind:is_dirty={is_number_of_spoken_languages_dirty} bind:errs={number_of_language_errs} required={true} type="number"/>
        {#if is_number_of_spoken_languages_dirty}
          {#each Object.values(number_of_language_errs) as errMsg}
            <div class="flex items-center gap-1 absolute top-[110%]">
              <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
              <span class="text-red-500 text-sm">{errMsg}</span> 
            </div>
          {/each}
        {/if}
      </div>
    </div>

    <div class="flex gap-8 md:gap-4 flex-col md:flex-row"> 
      <div class="flex-1 flex flex-col gap-2 relative">
        <div class="flex gap-1">
          <label class="text-white">Runtime</label> 
          <Tooltip.Root>
            <Tooltip.Trigger>
              <CircleQuestionMark color="white"></CircleQuestionMark>
            </Tooltip.Trigger>
            <Tooltip.Content>
              TMDB runtime is the total duration of a movie or episode measured in minutes.
            </Tooltip.Content>
          </Tooltip.Root>
        </div>
        <Input type="number" required={true} suffix="mins" bind:is_dirty={is_runtime_dirty} bind:value={runtime} bind:errs={runtime_errs}/>
        {#if is_runtime_dirty}
          {#each Object.values(runtime_errs) as errMsg}
            <div class="flex items-center gap-1 absolute top-[110%]">
              <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
              <span class="text-red-500 text-sm">{errMsg}</span> 
            </div>
          {/each}
        {/if}
      </div>

      <div class="flex-1 flex flex-col gap-2 relative">
        <div class="flex gap-1">
          <label class="text-white">Number of Production Companies</label> 
          <Tooltip.Root>
            <Tooltip.Trigger>
              <CircleQuestionMark color="white"></CircleQuestionMark>
            </Tooltip.Trigger>
            <Tooltip.Content>
              Total number of production companies that fund and oversee the creation of films
            </Tooltip.Content>
          </Tooltip.Root>
        </div>

        <Input bind:value={number_of_production_companies} bind:is_dirty={is_number_of_production_companies_dirty} bind:errs={number_of_production_companies_errs} required={true} type="number"/>
        {#if is_number_of_production_companies_dirty}
          {#each Object.values(number_of_production_companies_errs) as errMsg}
            <div class="flex items-center gap-1 absolute top-[110%]">
              <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
              <span class="text-red-500 text-sm">{errMsg}</span> 
            </div>
          {/each}
        {/if}
      </div>
    </div>
    
    <div class="flex gap-8 md:gap-4 flex-col md:flex-row"> 
      <div class="flex-1 flex flex-col gap-2 relative">
        <div class="flex gap-1">
          <label class="text-white">Popularity</label> 
          <Tooltip.Root>
            <Tooltip.Trigger>
              <CircleQuestionMark color="white"></CircleQuestionMark>
            </Tooltip.Trigger>
            <Tooltip.Content>
              TMDB’s popularity score is a relative metric based on recent user activity
              <br/>
              such as page views, searches, and interactions rather than a direct measure of quality or ratings. 
              <br/>
              It updates frequently and is mainly useful for comparing how much attention movies or shows are getting right now on TMDB.
            </Tooltip.Content>
          </Tooltip.Root>
        </div>
        <Input bind:value={popularity} bind:errs={popularity_errs} bind:is_dirty={is_popularity_dirty} required={true} type="number"/>
        {#if is_popularity_dirty}
          {#each Object.values(popularity_errs) as errMsg}
            <div class="flex items-center gap-1 absolute top-[110%]">
              <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
              <span class="text-red-500 text-sm">{errMsg}</span> 
            </div>
          {/each}
        {/if}
      </div>

      <div class="flex-1 flex flex-col gap-2 relative">
        <div class="flex gap-1">
          <label class="text-white">Number of Production Countries</label> 
          <Tooltip.Root>
            <Tooltip.Trigger>
              <CircleQuestionMark color="white"></CircleQuestionMark>
            </Tooltip.Trigger>
            <Tooltip.Content>
              Production countries represent where a film's production companies are based, not necessarily filming locations
            </Tooltip.Content>
          </Tooltip.Root>
        </div>

        <Input bind:value={number_of_production_countries} bind:is_dirty={is_number_of_production_countries_dirty} bind:errs={number_of_production_countries_errs} required={true} type="number"/>
        {#if is_number_of_production_countries_dirty}
          {#each Object.values(number_of_production_countries_errs) as errMsg}
            <div class="flex items-center gap-1 absolute top-[110%]">
              <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
              <span class="text-red-500 text-sm">{errMsg}</span> 
            </div>
          {/each}
        {/if}
      </div>
    </div>

    <div class="flex gap-8 md:gap-4 flex-col md:flex-row"> 
      <div class="flex-1 flex flex-col gap-2 relative">
        <div class="flex gap-1">
          <label class="text-white">Vote Count</label> 
          <Tooltip.Root>
            <Tooltip.Trigger>
              <CircleQuestionMark color="white"></CircleQuestionMark>
            </Tooltip.Trigger>
            <Tooltip.Content>
              TMDB vote count is the total number of user ratings a movie has received on the platform.
              <br/>
              It has a minimum of 0 and no maximum, since it only increases as more users submit ratings.
            </Tooltip.Content>
          </Tooltip.Root>
        </div>

        <Input bind:value={vote_count} bind:errs={vote_count_errs} bind:is_dirty={is_vote_count_dirty} required={true} type="number"/>
        {#if is_vote_count_dirty}
          {#each Object.values(vote_count_errs) as errMsg}
            <div class="flex items-center gap-1 absolute top-[110%]">
              <TriangleAlert class="text-red-500" size="18"></TriangleAlert>
              <span class="text-red-500 text-sm">{errMsg}</span> 
            </div>
          {/each}
        {/if}
      </div>
      <div class="hidden md:flex flex-1 flex-col gap-2"></div>
    </div>

    <Button variant="blue" onclick={predict} class="w-fit self-center" type="submit">
      <TrendingUpNow/>
      Predict Now
    </Button>
  </form>
</div>

<style>
  @keyframes slide-out-to-left {
    from {
      right: 0%;
      opacity: 1;
    }
    to {
      right: 100%;
      opacity: 0;
    }
  }
  @keyframes slide-out-to-right {
    from {
      left: 0%;
      opacity: 1;
    }
    to {
      left: 100%;
      opacity: 0;
    }
  }
  #prediction-wrapper {
    view-transition-name: prediction-wrapper;
  }
  ::view-transition-group(prediction-wrapper) {
    animation-duration: 300ms;
  }
  ::view-transition-old(prediction-wrapper) {
    animation-name: slide-out-to-left;
  }
  ::view-transition-old(prediction-wrapper-back) {
    animation-name: slide-out-to-right;
  }
</style>
