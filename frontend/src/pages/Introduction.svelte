<script lang="ts">
    import { Button } from "$lib/components/ui/button/index.js";
    import { navigate } from "../router";

    function toData(){
        navigate('/data-exploration', { viewTransition: true })
    }
    function toPrediction(){
        navigate('/prediction', { viewTransition: true })
    }
    function toAnalytics(){
        navigate('/analytics', { viewTransition: true })
    }

</script>

<div class="h-screen">
    <div class="h-full w-full opacity-30 absolute -z-1 bg-cover bg-[url(/src/assets/theater3.jpg)]"></div>
    <div class="max-w-5xl mx-auto pt-25 flex flex-col px-6">
        <h1 class="text-white text-4xl font-bold pb-3 text-center">Welcome to Popcorn Prophet</h1>
        <p class="text-gray-2 pb-7 text-center mb-5">Predicting the Box Office Revenue of a Movie Using Predictive Analytics and Modelling.</p>
        
        <div class="flex justify-between gap-10 mb-5 flex-col md:flex-row">
            <div class="flex-1 bg-dark-blue-3 gap-4 border-blue-gray-2 min-w-0 rounded-2xl border flex flex-col">
                <p class="text-white font-bold text-2xl text-center mt-5">Data Exploration</p>
                <p class="text-gray-2 p-5">Explore the data used to train our machine learning model. Examine the distribution of every key feature, and calculate averages, number of movies, and maximum revenue filtered by genres of your choice</p>
                <div class="flex justify-center mt-auto mb-5">
                    <Button variant="blue" onclick={toData}>
                        Take me there
                    </Button>
                </div>
            </div>
            <div class="flex-1 bg-dark-blue-3 gap-4 border-blue-gray-2 min-w-0 rounded-2xl border flex flex-col">
                <p class="text-white font-bold text-2xl text-center mt-5">Prediction</p>
                <p class="text-gray-2 p-5">Enter values for key parameters that will be used to predict the box office revenue of a movie. View the results of the prediction, its accuracy, and how it compares to actual movies with similar features. Run a simulation to see how slightly different values for features affect the prediected revenue.</p>
                <div class="flex justify-center mt-auto mb-5">
                    <Button variant="blue" onclick={toPrediction}>
                        Take me there
                    </Button>
                </div>
            </div>
            <div class="flex-1 bg-dark-blue-3 gap-4 border-blue-gray-2 min-w-0 rounded-2xl border flex flex-col">
                <p class="text-white font-bold text-2xl text-center mt-5">Analytics</p>
                <p class="text-gray-2 p-5">Examine movies existing in our dataset and observe how our predicted revenue compares to the actual revenue of real movies. Analize how key features are contributing to the overall prediction of the box office revenue.</p>
                <div class="flex justify-center mt-auto mb-5">
                    <Button variant="blue" onclick={toAnalytics}>
                        Take me there
                    </Button>
                </div>
            </div>
        </div>
    </div>
</div>
