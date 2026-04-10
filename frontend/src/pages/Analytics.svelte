<script lang="ts">
  import type { Movie } from "src/types/types";
  import { API_URL, POSTER_PREFIX } from "../const/const";
  import { Card, CardContent, CardHeader, CardTitle } from "$lib/components/ui/card"
  import { Command, CommandInput } from "$lib/components/ui/command";
  import { Skeleton } from "$lib/components/ui/skeleton/index.js";
  import { navigate, route } from "../router";
  import { onDestroy } from "svelte";
  import { analytics_state } from "./states.svelte";

  let movies: Movie[] = $state([]);
  let search_string = $state("");
  let is_loading = $state(false);
  let last_movie_id_state: number | null = null;

  let timeout: number | null = null;
  const cooldown = 200;

  if (route.state === 'navigateFromResult' && localStorage.getItem("states")) {
    const states = JSON.parse(localStorage.getItem("states")!);
    search_string = states.search_string;
    movies = states.movies;
    last_movie_id_state = states.last_movie_id_state;
  }

  const beforeUnloadListener = () => {
    localStorage.removeItem("states");
  }
  window.addEventListener("beforeunload", beforeUnloadListener)

  function on_movie_selection(e: PointerEvent, movie: Movie) {
    let card = e.target as HTMLElement;
    while (card.getAttribute('data-slot') !== 'card') {
      card = card.parentElement as HTMLElement;
    }
    const poster = card.querySelector('img') as HTMLImageElement;
    poster.style.viewTransitionName = "poster";
    const title = card.querySelector("[data-slot='card-header']") as HTMLElement;
    title.style.viewTransitionName = "title";

    localStorage.setItem("states", JSON.stringify({ search_string, movies, last_movie_id_state }));
    navigate('/analytics/result/:movie_id', { 
      params: { movie_id: movie.id.toString()}, 
      state: $state.snapshot(movie),
      viewTransition: true, 
    });
  }

  async function on_input_change() {
    if (search_string.trim() === '') {
      is_loading = false;
      movies = [];
      last_movie_id_state = null;
      return;
    }

    is_loading = true;
    if (timeout) clearTimeout(timeout);
      
    timeout = setTimeout(async () => {
      await get_movies(search_string);
      is_loading = false;
    }, cooldown);
  }

  async function get_movies(title: string, last_movie_id?: number) {
    let url = `${API_URL}/movies?title=${title.trim()}`;
    if (last_movie_id) {
      url = url + `&last_id=${last_movie_id}`
    }
    const res = await fetch(url);
    const movies_json = await res.json();
    movies = last_movie_id ? [...movies, ...movies_json] : movies_json;
    last_movie_id_state = movies.length ? movies[movies.length - 1].id : null;
  }

  const scrollListener = () => {
    const innerHeight = window.innerHeight;
    
    if (innerHeight + window.scrollY >= document.documentElement.scrollHeight) {
      get_movies(search_string.trim(), last_movie_id_state!);
    }

    analytics_state.show_back_to_top_button = document.documentElement.scrollTop > innerHeight / 2;
  }
  window.addEventListener("scroll", scrollListener);

  onDestroy(() => {
    window.removeEventListener("scroll", scrollListener);
    window.removeEventListener("beforeunload", beforeUnloadListener);
    analytics_state.show_back_to_top_button = false;
  })
</script>

<div class="max-w-4xl mx-auto pt-10 flex flex-col px-6 relative">
  <h1 class="text-white text-4xl font-bold pb-3 text-center">Find an Existing Movie</h1>
  <p class="text-gray-2 pb-7 text-center">Search our database to view the prediction explainability dashboard for any movie</p>

  <Command class="mb-7">
    <CommandInput placeholder="Search for a movie title" oninput={on_input_change} bind:value={search_string}/>
  </Command>

  {#if is_loading}
    <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
      {#each { length: 4 }}
        <Card class="gap-3 opacity-50">
          <CardHeader>
            <CardTitle>
              <Skeleton class="h-10 w-full bg-black"/>
            </CardTitle>
          </CardHeader>
          <CardContent>
           <Skeleton class="h-60 md:h-50 w-full bg-black"/>
          </CardContent>
        </Card>
      {/each}
    </div>
  {:else}
    {#if movies.length === 0 && search_string.trim().length !== 0}
      <p class="text-white text-3xl">No movies found (&gt;_&lt;)</p>
    {:else}
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
        {#each movies as movie}
          <Card class="bg-dark-gray-2 hover:bg-blue-gray-2 border-blue-gray-2 hover:border-blue-gray gap-3 text-white hover:cursor-pointer perspective-[1px] translate-z-0 hover:scale-[1.1] duration-0.3 transform transition-transform hover:shadow-lg hover:shadow-cyan-500/50 font-normal hover:font-bold" onclick={(e) => on_movie_selection(e as any, movie)}>
            <CardHeader>
              <CardTitle class="overflow-hidden text-ellipsis whitespace-nowrap">{movie.original_title}</CardTitle>
            </CardHeader>
            <CardContent class="text-center">
              {#if movie.poster_path}
                <img src={POSTER_PREFIX + movie.poster_path} alt="">
              {:else}
                <p>No poster available</p>
                <p>(⋟﹏⋞)</p>
              {/if}
            </CardContent>
          </Card>
        {/each}
      </div>
    {/if}
  {/if}

</div>

