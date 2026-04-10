<script lang="ts">
  import * as Card from "$lib/components/ui/card/index.js";
  import ArrowLeft from "@lucide/svelte/icons/arrow-left";
  import Play from "@lucide/svelte/icons/play";
  import { API_URL, POSTER_PREFIX, TMDB_MOVIE_PREFIX } from "../const/const";
  import { Button } from "$lib/components/ui/button/index.js";
  import { Skeleton } from "$lib/components/ui/skeleton/index.js";
  import { convert_form_to_body, type Movie, type Prediction } from "../types/types";
  import { currency_formatter } from "./reuse";
  import { form } from "./states.svelte";
  import { navigate } from "../router";
  import { onMount } from "svelte";
  import pepe_band from "../assets/pepe-band.gif";
  import pepe_dancing from "../assets/pepe-dancing.gif";
  import pepe_what from "../assets/pepe-what.gif";
  import pepe_cry from "../assets/pepe-cry.gif";

  let prediction = $state<Prediction>();
  let verdict = $state<string>('');
  let loading = $state(false);

  function backToInput() {
    const prediction_wrapper = document.querySelector("#prediction-wrapper") as HTMLDivElement;
    prediction_wrapper.style.viewTransitionName = "prediction-wrapper-back";
    navigate('/prediction', { viewTransition: true });
  }

  function runSimulation() {
    navigate('/prediction/result/simulation', { viewTransition: true, state: { predicted_revenue: prediction?.predicted_revenue } });
  }

  onMount(async () => {
    if (!Object.keys(form).length) {
      navigate('/prediction');
    }
    
    loading = true;
    
    const res = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(convert_form_to_body(form))
    });
    
    loading = false;
    
    prediction = await res.json();
    const predicted_revenue = prediction?.predicted_revenue ?? 0;
    
    const ratio = predicted_revenue / form.budget;
    if (ratio >= 3 || predicted_revenue >= 500_000_000) {
      verdict = 'Blockbuster';
    } else if (2.5 < ratio && ratio <= 3) {
      verdict = 'Moderate Hit';
    } else if (2 < ratio && ratio <= 2.5) {
      verdict = 'Break-even';
    } else {
      verdict = 'Flop';
    }
  })

  function row_click(movie: Movie) {
    window.open(`${TMDB_MOVIE_PREFIX}/${movie.id}`, '_blank')!.focus();
  }

  let div: HTMLElement;

  function mouse_enter(e: any, movie: Movie) {
    const {x, y} = e.target.getBoundingClientRect()

    const overlay = document.body.querySelector("#overlay")!;
    div = document.createElement("div");
    div.style.position = 'absolute';
    div.style.left = `${x}px`;
    const TOOLTIP_HEIGHT = 280;
    const ROW_HEIGHT = e.target.offsetHeight;
    const OFFSET = 20;
    if (y + TOOLTIP_HEIGHT + OFFSET < window.innerHeight) {
      div.style.top = `${y + ROW_HEIGHT + OFFSET}px`;
    } else {
      div.style.top = `${y - TOOLTIP_HEIGHT - OFFSET}px`;
    }
    div.style.width = `${e.target.offsetWidth}px`;

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

    div.insertAdjacentHTML('afterbegin', `
      <div style="display: flex; gap: 12px; background-color: #1E2C35; padding: 20px; box-shadow: 0px 0px 10px #b2b2b2; border-radius: 20px; opacity: 0.95">
        <div style="height: 240x; width: 160px">
          <img src="${POSTER_PREFIX + movie.poster_path}" class="object-contain" id="poster" alt="movie poster">
        </div>

        <div style="flex: 7; display: flex; flex-direction: column; gap: 12px; color: #fff">
            <h1 style="font-weight: 700; font-size: 1.5rem; line-height: calc(2 / 1.5)" id="title">${movie.original_title} <span class="text-gray-2">(${extract_release_year(movie.release_date)})</span></h1>
            <div style="display: flex; font-size: 0.875rem; line-height: calc(1.25 / 0.875)">
              <span>${reformat_date(movie.release_date)} (${get_original_language(movie.original_language)})</span>
              <span class="pl-6 relative before:content-['•'] before:absolute before:left-2">${get_genres(movie.genres)}</span>
              <span class="pl-6 relative before:content-['•'] before:absolute before:left-2">${reformat_time(movie?.runtime as number)}</span>
            </div>
            <h3 style="font-weight: 700; font-size: 1.25rem; line-height: calc(1.75 / 1.25)">Overview</h3>
            <p>${movie.overview}</p>
        </div>
      </div>
    `);

    overlay.insertAdjacentElement('afterbegin', div);
  }

  function mouse_leave() {
    div.remove();
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
  };

  const original_language_map: Record<number, string> = {
    0: "",
    1: "en",
    2: "es",
    3: "fr",
    4: "hi",
    5: "ja",
    6: "ru"
  }

  const get_original_language = (id: number) => {
    if (!id) return "";
    return original_language_map[id] ?? "";
  }

  const verdict_color_map: Record<string, string> = {
    "Blockbuster": "text-light-green",
    "Moderate Hit": "text-light-blue",
    "Break-even": "text-gray-2",
    "Flop": "text-light-red"
  }

  function getVerdictTextColor(verdict: string) {
    return verdict_color_map[verdict];
  }
</script>

<div class="flex flex-col max-w-7xl mx-auto py-10 px-6" id="prediction-wrapper">
  <div class="flex justify-between mb-3">
    <div>
      <h1 class="text-white text-3xl font-bold pb-2">Prediction Result</h1>
      <p class="text-gray-2 pb-7">Based on the data you provided, here's our prediction</p>
    </div>
  </div>

  <div class="flex justify-between gap-4 mb-12 flex-col md:flex-row">
    <Card.Root class="flex-1 bg-blue-gray gap-4 border-blue-gray-2 min-w-0">
      <Card.Header>
        <Card.Title class="text-white">Projected Revenue</Card.Title>
      </Card.Header>
      <Card.Content>
        {#if loading}
          <Skeleton class="h-10 w-2/3 bg-light-gray"/>
        {:else}
          <p class="text-4xl font-extrabold text-light-blue">{prediction?.predicted_revenue ? currency_formatter.format(prediction.predicted_revenue) : "-"}</p>
        {/if}
      </Card.Content>
    </Card.Root>  

    <Card.Root class="flex-1 bg-blue-gray gap-4 border-blue-gray-2 min-w-0">
      <Card.Header>
        <Card.Title class="text-white">Verdict</Card.Title>
      </Card.Header>
      <Card.Content>
        {#if loading}
          <Skeleton class="h-10 w-2/3 bg-light-gray"/>
        {:else}
          <div class="flex gap-3">
            <p class="text-4xl font-extrabold {getVerdictTextColor(verdict)}">{verdict}</p>
            {#if verdict === "Blockbuster" }
              <img src={pepe_band} class="h-[70px] mt-[-20px]"/>
            {:else if verdict === "Moderate Hit" }
              <img src={pepe_dancing} class="h-[70px] mt-[-20px]"/>
            {:else if verdict === "Break-even" }
              <img src={pepe_what} class="h-[50px] mt-[-10px]"/>
            {:else if verdict === "Flop" }
              <img src={pepe_cry} class="h-[50px] mt-[-10px]"/>
            {/if}
          </div>
        {/if}
      </Card.Content>
    </Card.Root>
  </div>
  
  <h1 class="text-white font-bold text-xl mb-5">How It Compares</h1>

  <div class="overflow-auto mb-10">
    <table class="text-white w-full">
      <thead class="text-left">
        <tr class="border border-blue-gray-2 bg-dark-gray-2">
          <th class="px-4 py-3">Movie Title</th>
          <th class="px-4 py-3">Genre</th>
          <th class="px-4 py-3 text-right">Actual Box Office</th>
          <th class="px-4 py-3 text-right">Vote Average</th>
          <th class="px-4 py-3 text-right">Number of Votes</th>
          <th class="px-4 py-3 text-right">Budget</th>
        </tr>
      </thead>
      <tbody>
        {#if loading}
          {#each { length: 5} }
            <tr class="border border-blue-gray-2 bg-dark-gray-3 font-light">
              <td class="px-4 py-5">
                <Skeleton class="h-10 w-2/3 bg-light-gray"/>
              </td>
              <td class="px-4 py-5">
                <Skeleton class="h-10 w-2/3 bg-light-gray"/>
              </td>
              <td class="px-4 py-5 text-right">
                <Skeleton class="h-10 w-2/3 bg-light-gray"/>
              </td>
              <td class="px-4 py-5 text-right">
                <Skeleton class="h-10 w-2/3 bg-light-gray"/>
              </td>
              <td class="px-4 py-5 text-right">
                <Skeleton class="h-10 w-2/3 bg-light-gray"/>
              </td>
              <td class="px-4 py-5 text-right">
                <Skeleton class="h-10 w-2/3 bg-light-gray"/>
              </td>
            </tr>
          {/each}
        {/if}
        {#each prediction?.similar_movies as movie}
          <tr class="border border-blue-gray-2 bg-dark-gray-3 hover:bg-dark-gray-2 hover:cursor-pointer font-light" onclick={row_click(movie)} onmouseenter={(e) => mouse_enter(e, movie)} onmouseleave={mouse_leave}>
            <td class="px-4 py-5">{movie.original_title}</td>
            <td class="px-4 py-5">{get_genres(movie.genres)}</td>
            <td class="px-4 py-5 text-right font-extrabold">{currency_formatter.format(movie.revenue)}</td>
            <td class="px-4 py-5 text-right">{movie.vote_average.toFixed(2)}</td>
            <td class="px-4 py-5 text-right">{movie.vote_count}</td>
            <td class="px-4 py-5 text-right">{currency_formatter.format(movie.budget)}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>

  <div class="self-center flex gap-3">
    <Button variant="gray" onclick={backToInput}>
      <ArrowLeft/>
      Back to Input
    </Button>
    <Button variant="blue" onclick={runSimulation}>
      <Play/>
      Run Simulation
    </Button>
  </div>
</div>

<style>
  #prediction-wrapper {
    view-transition-name: prediction-wrapper;
  }
</style>
