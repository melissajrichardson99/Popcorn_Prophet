<script lang="ts">
  import * as Card from "$lib/components/ui/card/index.js";
  import * as Select from "$lib/components/ui/select/index.js";
  import ChartJSTrendline from 'chartjs-plugin-trendline';
  import type { Bar, Exploration, Pie } from "../types/types";
  import { API_URL } from "../const/const";
  import { Chart } from "chart.js/auto";
  import { Skeleton } from "$lib/components/ui/skeleton/index.js";
  import { currency_formatter, number_formatter } from "./reuse";
  import { onMount, onDestroy } from "svelte";

  let showLineOfBestFit = $state(false);
  let loading = $state(false);

  //Parameters
  let parameter_selection = $state("budget");
  let parameter_options: Record<string, string> = {
    "budget": "Budget",
    "release_month": "Release Month",
    "runtime": "Runtime",
    "popularity": "Popularity",
    "vote_count": "Vote Count",
    "vote_average": "Vote Average",
    "number_of_spoken_languages": "Number of Languages",
    "number_of_production_countries": "Number of Production Countries",
    "number_of_production_companies": "Number of Production Companies"
  };

  let bar_selection = $state("original_language");
  let bar_options: Record<string, string> = {
    "original_language": "Language",
    "release_month": "Release Month",
    "number_of_spoken_languages": "Number of Languages",
    "number_of_production_countries": "Number of Production Countries",
    "number_of_production_companies": "Number of Production Companies"
  }

  // Genre
  let genres: string[] = $state([]);
  let genres_selection = $derived(genres.join(', '));
  let genre_options = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", 
                      "Family", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance", "Science Fiction",
                      "Thriller", "TV Movie", "War", "Western"];

  let chartElem: HTMLCanvasElement;
  let chartInstance: Chart;
  let pie_chart_instance: Chart;
  let bar_chart_instance: Chart;
  let exploration = $state<Exploration | null>(null);
  let pie = $state<Pie | null>(null);
  let bar = $state<Bar | null>(null);
  let x_param_value: string = "budget";

  let pie_elem: HTMLCanvasElement;
  let bar_elem: HTMLCanvasElement;

  const trendline = {
    colorMin: "red",
    lineStyle: "solid",
    width: 3,
    label: {
      display: false,
    }
  }

  const data = {
    datasets: [{
      label: 'Scatter Dataset',
      data: [],
      backgroundColor: '#0F93D4',
    }]
  };

  const commonConfig = {
    border: {
      color: "#FFFFFF"
    },
    ticks: {
      color: '#FFFFFF',
      callback: (value: number, _index: number, _ticks: any[]) => {
        if (x_param_value === 'budget') {
          return currency_formatter.format(value);
        } else {
          return value;
        }
      }
    }
  }

  const config = {
    type: 'scatter',
    data: data,
    options: {
      aimation: false,
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          callbacks: {
            label: function(context: any) {
              const xLabel = config.options.scales.x.title.text;
              const yLabel = config.options.scales.y.title.text;
              const xValue = context.parsed.x;
              const yValue = context.parsed.y;
              return `${xLabel}: ${currency_formatter.format(xValue)}, ${yLabel}: ${currency_formatter.format(yValue)}`;
            }
          }
        }
      },
      elements: {
        point: {
          radius: 5,
          hoverRadius: 8
        }
      },
      scales: {
        x: {
          type: 'linear',
          position: 'bottom',
          title: {
            text: 'Budget',
            color: '#FFFFFF',
            display: true
          },
          ...commonConfig
        },
        y: {
          title: {
            text: 'Revenue',
            color: '#FFFFFF',
            display: true
          },
          ...commonConfig
        }
      }
    }
  };

  const pie_config = {
    type: 'pie',
    data: {},
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: "#FFFFFF"
          }
        },
        title: {
          display: true,
        },
        tooltip: {
          callbacks: {
            label: function(context: any) {
              return `${context.formattedValue} %`;
            }
          }
        }
      }
    },
  };

  const bar_config = {
    type: 'bar',
    data: {},
    options: {
      scales: {
        x: {
          border: {
            color: '#FFFFFF'
          },
          ticks: {
            color: '#FFFFFF',
          },
          title: {
            text: "Language",
            color: '#FFFFFF',
            display: true
          }
        },
        y: {
          beginAtZero: true,
          title: {
            text: 'Average Revenue',
            color: '#FFFFFF',
            display: true
          },
          ...commonConfig
        }
      },
      plugins: {
        colors: {
          enabled: true
        },
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            label: function(context: any) {
              return `${currency_formatter.format(context.raw)}`;
            }
          }
        }
      },
    },
  };

  onMount(async () => {
    Chart.register(ChartJSTrendline);
    chartElem = document.getElementById("scatter-chart") as HTMLCanvasElement;
    if (chartElem) {
      chartInstance = new Chart(chartElem, config as any)
    }

    updateChart();

    pie_elem = document.getElementById("pie-chart") as HTMLCanvasElement;
    if (pie_elem) {
      pie_chart_instance = new Chart(pie_elem, pie_config as any)
    }

    pie = await fetchPie();
    const pie_data = {
      labels: $state.snapshot(pie.labels),
      datasets: [{label: 'Percentage', data: $state.snapshot(pie.data)}]
    };
    (pie_config as any).data = pie_data;
    pie_chart_instance.update();

    bar_elem = document.getElementById("bar-chart") as HTMLCanvasElement;
    if (bar_elem) {
      bar_chart_instance = new Chart(bar_elem, bar_config as any)
    }
    updateBarChart();
  })

  onDestroy(() => {
    chartElem?.remove();
  })

  async function updateBarChart() {
    bar = await fetchBar();
    const bar_data = {
      labels: $state.snapshot(bar.labels),
      datasets: [
        {
          data: $state.snapshot(bar.data),
          borderWidth: 1,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(255, 205, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(201, 203, 207, 0.2)'
          ],
          borderColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)',
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',
            'rgb(54, 162, 235)',
            'rgb(153, 102, 255)',
            'rgb(201, 203, 207)'
          ]
        }
      ]
    };
    (bar_config as any).data = bar_data;
    bar_chart_instance.update();
  }

  async function updateChart() {
    exploration = await fetchExploration();
    (config.data.datasets[0] as any).data = $state.snapshot(exploration?.plot_dataset);
    chartInstance.update();
  }

  async function onParameterChange(x_param: string) {
    x_param_value = x_param;
    config.options.scales.x.title.text = parameter_options[x_param];
    updateChart();
  }

  async function onBarSelectionChange(x_param: string) {
    bar_config.options.scales.x.title.text = bar_options[x_param];
    updateBarChart();
  }

  async function fetchExploration(): Promise<Exploration> {
    loading = true;
    const url = new URL(`${API_URL}/exploration`);
    const searchParams = url.searchParams;
    if (parameter_selection) {
      searchParams.set("x_param", parameter_selection);
    }
    if (genres_selection) {
      searchParams.set("genres", genres_selection);
    }
    const exploration_res = await fetch(url)
    loading = false;
    return await exploration_res.json();
  }

  async function fetchPie(): Promise<Pie> {
    loading = true;
    const url = new URL(`${API_URL}/exploration-pie`);
    const pie_res = await fetch(url)
    loading = false;
    return await pie_res.json();
  }

  async function fetchBar(): Promise<Bar> {
    loading = true;
    const url = new URL(`${API_URL}/exploration-bar`);
    const searchParams = url.searchParams;
    if (bar_selection) {
      searchParams.set("x_param", bar_selection);
    }
    const bar_res = await fetch(url)
    loading = false;
    return await bar_res.json();
  }

  function onCheckShowLineOfBestFit() {
    if (showLineOfBestFit) {
      (config.data.datasets[0] as any).trendlineLinear = trendline;
    } else {
      delete (config.data.datasets[0] as any).trendlineLinear;
    }
    chartInstance.update();
  }
</script>

<div class="flex flex-col max-w-7xl mx-auto pt-10 px-6 gap-5">
  <div>
    <h1 class="text-white text-3xl font-bold pb-2">Data Exploration</h1>
    <p class="text-gray-2">Explore the relationship between movie parameters and box office revenue</p>
  </div>

  <div class="bg-dark-blue-3 gap-10 border border-blue-gray-2 rounded-xl flex flex-col p-5">
    <div class="flex items-end gap-3">
      <div class="flex flex-col flex-1">
        <p class="text-white mb-2">
          Select Parameter
        </p>
        <Select.Root type="single" bind:value={parameter_selection} onValueChange={onParameterChange}>
            <Select.Trigger class="w-full">{parameter_options[parameter_selection]}</Select.Trigger>
            <Select.Content>
              {#each Object.entries(parameter_options) as [parameter_value, parameter_option]}
                <Select.Item value={parameter_value}>{parameter_option}</Select.Item>
              {/each}
            </Select.Content>
        </Select.Root>
      </div>
      <div class="flex flex-col flex-1 overflow-hidden">
        <p class="text-white mb-2">
          Filter by Genre
        </p>
        <Select.Root type="multiple" bind:value={genres} onValueChange={updateChart}>
            <Select.Trigger class="w-full">
              <div class="overflow-hidden text-ellipsis">{genres_selection ? genres_selection : "Select genres"}</div>
            </Select.Trigger>
            <Select.Content>
              {#each genre_options as genre_option}
                <Select.Item value={genre_option}>{genre_option}</Select.Item>
              {/each}
            </Select.Content>
          </Select.Root>
      </div>

      <div class="flex gap-2 mb-2 flex-1">
        <input type="checkbox" bind:checked={showLineOfBestFit} onchange={onCheckShowLineOfBestFit}/>
        <label class="text-white">Show Line of Best Fit</label>
      </div>
    </div>

    <p class="text-white text-2xl font-bold mb-5 text-center">Revenue vs Quantitative Features</p>

    <div class="min-h-100 w-full">
      <canvas id="scatter-chart"></canvas>
    </div>
  </div>

  <div class="flex justify-between gap-4 flex-col md:flex-row">
    <Card.Root class="flex-1 bg-dark-blue-3 gap-4 border-blue-gray-2">
      <Card.Header>
        <Card.Title class="text-light-gray">Movies</Card.Title>
      </Card.Header>
      <Card.Content> 
        {#if loading}
          <Skeleton class="h-10 w-2/3 bg-light-gray"/>
        {:else}
          <p class="text-4xl font-extrabold text-white">{exploration?.total_number_of_movies ? number_formatter.format(exploration?.total_number_of_movies) : "-"}</p>
        {/if}
      </Card.Content>
    </Card.Root>  

    <Card.Root class="flex-1 bg-dark-blue-3 gap-4 border-blue-gray-2">
      <Card.Header>
        <Card.Title class="text-light-gray">Average Revenue</Card.Title>
      </Card.Header>
      <Card.Content>
        {#if loading}
          <Skeleton class="h-10 w-2/3 bg-light-gray"/>
        {:else}
          <p class="text-white text-4xl font-extrabold">{exploration?.average_revenue ? currency_formatter.format(exploration?.average_revenue) : "-"}</p>
        {/if}
      </Card.Content>
    </Card.Root>  

    <Card.Root class="flex-1 bg-dark-blue-3 gap-4 border-blue-gray-2">
      <Card.Header>
        <Card.Title class="text-light-gray">Average Budget</Card.Title>
      </Card.Header>
      <Card.Content>
        {#if loading}
          <Skeleton class="h-10 w-2/3 bg-light-gray"/>
        {:else}
          <p class="text-white text-4xl font-extrabold">{exploration?.average_budget ? currency_formatter.format(exploration?.average_budget) : "-"}</p>
        {/if}
      </Card.Content>
    </Card.Root>

    <Card.Root class="flex-1 bg-dark-blue-3 gap-4 border-blue-gray-2">
      <Card.Header>
        <Card.Title class="text-light-gray">Highest Revenue</Card.Title>
      </Card.Header>
      <Card.Content>
        {#if loading}
          <Skeleton class="h-10 w-2/3 bg-light-gray"/>
        {:else}
          <p class="text-white text-4xl font-extrabold">{exploration?.highest_revenue ? currency_formatter.format(exploration?.highest_revenue) : "-"}</p>
        {/if}
      </Card.Content>
    </Card.Root>
  </div>

  <div class="bg-dark-blue-3 border border-blue-gray-2 rounded-xl flex flex-col p-9">
      <p class="text-white mb-2">
        Select Parameter
      </p>

      <Select.Root type="single" bind:value={bar_selection} onValueChange={onBarSelectionChange}>
          <Select.Trigger class="w-100 mb-5">{bar_options[bar_selection]}</Select.Trigger>
          <Select.Content>
            {#each Object.entries(bar_options) as [parameter_value, parameter_option]}
              <Select.Item value={parameter_value}>{parameter_option}</Select.Item>
            {/each}
          </Select.Content>
      </Select.Root>

      <p class="text-white text-2xl font-bold mb-5 text-center">Average Revenue vs Features</p>

      <canvas id="bar-chart"></canvas>
  </div>

  <div class="bg-dark-blue-3 border border-blue-gray-2 rounded-xl flex flex-col p-9 mb-5 items-center">
    <p class="text-white -mb-5 text-2xl font-bold">Language Distribution</p>
    <div class="h-100 w-100">
      <canvas id="pie-chart"></canvas>
    </div>
  </div>
</div>
