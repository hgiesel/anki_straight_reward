import { writable } from "svelte/store";
import Rewards from "./Rewards.svelte";

$deckOptions.then((deckOptions) => {
  const data = writable({
    straightLength: 1,
    baseEase: 0.05,
    stepEase: 0.05,
    startEase: 1.3,
    stopEase: 2.5,
    enableNotification: true,
  });

  deckOptions.options.append({ component: Rewards, props: { data } }, -4)
})
