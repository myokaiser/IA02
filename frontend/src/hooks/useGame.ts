"use client";

import { useEffect, useState } from "react";
import { fetchState, stepGame, startGame, resetGame } from "@/src/lib/api";

export function useGame() {
    type Data = {
        map: Record<string, string>,
        position: string,
        orientation: string,
        done: boolean,
        phase: number
    }
  const [state, setState] = useState<Data | null>(null);
  const [running, setRunning] = useState(false);

  // 1. LOAD INITIAL STATE ONLY ONCE
  useEffect(() => {
    fetchState().then(setState);
  }, []);

  // 2. START SIMULATION
  const start = async () => {
    await startGame();
    setRunning(true);
  };

    const reset = async () => {
    setRunning(false);

    await resetGame();

    const newState = await fetchState();
    setState(newState);
    };

  // 3. LOOP ONLY WHEN RUNNING
  useEffect(() => {
    if (!running) return;

    const interval = setInterval(async () => {
      await stepGame();
      const newState = await fetchState();
      setState(newState);

      if (newState.done && newState.phase === 2) {
        setRunning(false);
      }
    }, 400);

    return () => clearInterval(interval);
  }, [running]);

  return { state, running, start, reset };
}