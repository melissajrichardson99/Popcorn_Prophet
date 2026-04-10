import { createRouter } from 'sv-router';
import Analytics from "./pages/Analytics.svelte";
import AnalyticsResult from "./pages/AnalyticsResult.svelte";
import DataExploration from "./pages/DataExploration.svelte";
import Prediction from "./pages/Prediction.svelte";
import Introduction from "./pages/Introduction.svelte";
import PredictionResult from "./pages/PredictionResult.svelte";
import Simulation from "./pages/Simulation.svelte";

export const { p, navigate, isActive, route } = createRouter({
	"/analytics": Analytics,
	"/analytics/result/:movie_id": AnalyticsResult,
	"/data-exploration": DataExploration,
	"/prediction": Prediction,
	"/prediction/result": PredictionResult,
	"/prediction/result/simulation": Simulation,
	"/": Introduction
});
