<script lang="ts">
  import * as Card from "$lib/components/ui/card/index.js";
  import ArrowLeft from "@lucide/svelte/icons/arrow-left";
  import type { MovieAnalytics } from "src/types/types";
  import { Button } from "$lib/components/ui/button/index.js";
  import { API_URL, POSTER_PREFIX } from "../const/const";
  import { Skeleton } from "$lib/components/ui/skeleton/index.js";
  import { currency_formatter } from "./reuse";
  import { onDestroy, onMount } from "svelte";
  import { route, navigate } from "../router";

  let movie = $state<MovieAnalytics>();
  let backdrop_dom_node: HTMLDivElement | null = null;
  let loading = $state<boolean>(false);

  function back_to_search_page() {
    navigate("/analytics", { state: 'navigateFromResult', viewTransition: true });
  }

  onMount(async () => {
    loading = true;
    const res = await fetch(`${API_URL}/analytics/${route.params.movie_id}`)
    movie = await res.json();
    let sum = 0;
    for (const [shap_key, shap_value] of Object.entries(movie?.shap_values!)) {
      if ("A" <= shap_key && shap_key <= "S") {
        sum += shap_value;
        delete movie?.shap_values[shap_key];
      }
    }
    movie.shap_values['genres'] = sum;
    loading = false;
    const main = document.body.querySelector('div#app main');
    backdrop_dom_node = document.createElement('div');
    backdrop_dom_node.style = `position: absolute; width: 100%; height: 300px; z-index: -1`;
    const imgElem: HTMLImageElement = document.createElement('img');
    imgElem.src = `${POSTER_PREFIX}${movie?.backdrop_path}`;
    imgElem.style = `height: 100%; width: 100%; object-fit: cover; opacity: 0; transition: opacity .75s cubic-bezier(.165,.84,.44,1)`;
    if (imgElem.complete) {
      imgElem.style.opacity = "0.2";
    } else {
      imgElem.addEventListener('load', () => {
        imgElem.style.opacity = "0.2";
      });
    }
    backdrop_dom_node.insertAdjacentElement('afterbegin', imgElem);
    main?.insertAdjacentElement('afterbegin', backdrop_dom_node);
  })

  onDestroy(() => {
    backdrop_dom_node?.remove();
  })

  const extract_release_year = (date: string) => {
    if (!date) return '';
    return date.split("-")[0];
  }

  const reformat_date = (date: string | null) => {
    if (!date) return '';
    const [y, m, d] = date.split("-");
    return `${m}/${d}/${y}`;
  }

  const reformat_time = (time: number | null) => {
    if (!time) return '';
    const h = Math.floor(time / 60);
    const m = time % 60;
    let str = '';
    if (h > 0) str += `${h}h `;
    if (m > 0) str += `${m}m`;
    return str;
  }

  const original_language_map: Record<number, string> = {
    1: "en",
    0: "",
    4: "hi",
    3: "fr",
    6: "ru",
    2: "es",
    5: "ja"
  }

  const get_original_language = (id: number) => {
    if (!id) return "";
    return original_language_map[id] ?? "";
  }

  const genres_map: Record<string, string> = {
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
    'S': 'Western'
  }

  const get_genres = (genres: string) => {
    if (!genres) return "";
    return eval(genres).map(g => genres_map[g]).join(", ");
  }

  const label_map: Record<string, string> = {
    "vote_average": "Vote Average",
    "vote_count": "Vote Count",
    "runtime": "Runtime",
    "budget": "Budget",
    "original_language": "Original Language",
    "popularity": "Popularity",
    "number_of_production_companies": "Number of Production Companies",
    "number_of_production_countries": "Number of Production Countries",
    "number_of_spoken_languages": "Number of Spoken Languages",
    "release_month": "Release Month",
    "genres": "Genres"
  }

  const transform_label = (raw_label: string) => {
    if (!raw_label) return "";
    return label_map[raw_label] ?? "";
  }

</script>

<div class="flex flex-col max-w-7xl mx-auto pt-10 px-6">
  <div class="flex justify-between mb-3">
    <Button variant="ghost" onclick={back_to_search_page} class="text-white">
      <ArrowLeft/>
      Back to Search page
    </Button>
  </div>

  <h1 class="text-white text-center text-3xl font-bold pb-2 mb-3">Prediction Analysis</h1>

  <div class="flex mb-6 gap-3 bg-blue-gray border border-blue-gray-2 p-6 rounded-xl">
      <div class="h-60 w-40">
        <img src={POSTER_PREFIX + movie?.poster_path} class="object-contain" id="poster" alt="movie poster">
      </div>
      {#if !loading}
        <div class="flex-7 text-white flex flex-col gap-3">
            <h1 class="text-2xl font-bold" id="title">{movie?.original_title} <span class="text-gray-2">({extract_release_year(movie?.release_date as string)})</span></h1>
            <div class="flex text-sm">
              <span>{reformat_date(movie?.release_date as string)} ({get_original_language(movie?.original_language).toUpperCase()})</span>
              <span class="pl-6 relative before:content-['•'] before:absolute before:left-2">{get_genres(movie?.genres)}</span>
              <span class="pl-6 relative before:content-['•'] before:absolute before:left-2">{reformat_time(movie?.runtime as number)}</span>
            </div>
            <h3 class="text-xl font-bold">Overview</h3>
            <p>{movie?.overview}</p>
        </div>
      {:else}
        <div class="flex-7 text-white flex flex-col gap-3">
            <Skeleton class="h-8 bg-gray-2 w-80 opacity-20"></Skeleton>
            <Skeleton class="h-6 bg-gray-2 w-100 opacity-20"></Skeleton>
            <Skeleton class="h-8 bg-gray-2 w-40 opacity-20"></Skeleton>
            <Skeleton class="h-25 bg-gray-2 w-200 opacity-20"></Skeleton>
        </div>
      {/if}
  </div>

  <div class="flex flex-col md:flex-row justify-between gap-4 mb-12">
    <Card.Root class="flex-1 bg-blue-gray gap-4 border-blue-gray-2 min-w-0">
      <Card.Header>
        <Card.Title class="text-white">Actual Box Office Revenue</Card.Title>
      </Card.Header>
      <Card.Content>
        {#if !loading}
          <p class="text-white text-4xl font-extrabold">{currency_formatter.format(movie?.revenue as number)}</p>
        {:else}
          <Skeleton class="h-10 bg-gray-2 w-60 opacity-20"></Skeleton>
        {/if}
      </Card.Content>
      <Card.Footer>
        <p class="text-gray-2 text-sm">Actual revenue at the time of the release</p>
      </Card.Footer>
    </Card.Root>  

    <Card.Root class="flex-1 bg-dark-blue-2 border border-light-blue gap-4 min-w-0">
      <Card.Header>
        <Card.Title class="text-white">Predicted Box Office Revenue</Card.Title>
      </Card.Header>
      <Card.Content>
        {#if !loading}
          <p class="text-white text-4xl font-extrabold">{currency_formatter.format(movie?.predicted_revenue as number)}</p>
        {:else}
          <Skeleton class="h-10 bg-gray-2 w-60 opacity-20"></Skeleton>
        {/if}
      </Card.Content>
      <Card.Footer>
        <p class="text-gray-2 text-sm">Final calculated prediction</p>
      </Card.Footer>
    </Card.Root>  
  </div>
  
  <div>
    <h1 class="text-white text-xl font-bold mb-5">Key Prediction Factors</h1>
  
    <table class="text-white w-full">
      <thead class="text-left">
        <tr class="border border-blue-gray-2 bg-dark-gray-2">
          <th class="px-4 py-3 w-1/2">Feature</th>
          <th class="px-4 py-3">Impact on Revenue</th>
        </tr>
      </thead>
      <tbody>
        {#each Object.entries(movie?.shap_values || []) as [shap_label, shap_value]}
          <tr class="border border-blue-gray-2 bg-dark-gray-3 font-light">
            <td class="px-4 py-7">{transform_label(shap_label)}</td>
            <td class="px-4 py-7">
              <div class="{shap_value > 0 ? "text-light-green bg-dark-green" : "text-light-red bg-dark-red"}  rounded-3xl w-fit px-5 py-3 font-bold">
                {#if shap_value > 0}
                  <span class="mr-2">&#8593</span> {currency_formatter.format(shap_value)}
                {:else}
                  <span class="mr-2">&#8595;</span> {currency_formatter.format(shap_value)}
                {/if}
              </div>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>

<style>
  #poster {
    view-transition-name: poster;
  }
  #title {
    view-transition-name: title;
  }
</style>

