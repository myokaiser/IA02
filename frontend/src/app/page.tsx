"use client";

import Grid from "@/src/components/Grid";
import Controls from "@/src/components/Controls";
import Reset from "@/src/components/Reset";
import { useGame } from "@/src/hooks/useGame";

import { useState } from "react";

export default function Page() {
  const { state, running, start, reset } = useGame();
  const isFinished = state && state.done && state.phase === 2;

  if (!state) {
    return (
      <div className="p-6 text-white">
        Loading initial state...
      </div>
    );
  }

  return (
    <div className="p-6 flex flex-col gap-4 bg-black min-h-screen text-white">
      {!isFinished ? 
      <Controls running={running} onStart={start} />
      :
      <Reset running={running} onStart={reset} />}

      {!running && (
        <div className="text-xs text-zinc-400">
          Preview mode (initial state)
        </div>
      )}
      <div className="flex items-center justify-center min-h-screen bg-black">
        <div className="scale-[2.5] origin-center">
          <Grid
            map={state.map}
            position={state.position}
            orientation={state.orientation}
          />
        </div>
      </div>
      {/* <div className="text-xs text-zinc-500">
        Iteration: {state.iteration}
      </div> */}

      {isFinished && (
        <div className="text-red-400 font-bold">
          Simulation finished
        </div>
      )}
    </div>
  );
}