"use client";

import { useEffect, useState } from "react";
import {
  fetchState,
  startGame,
  stepGame,
  resetGame,
  sendAction,
} from "@/src/lib/api";

export function useGame() {
    type Data = {
        map: Record<string, string>,
        nb_lignes: number,
        nb_colonnes: number,
        position: string,
        orientation: string,
        done: boolean,
        phase: number,
        action: string,
        known: string[]
    }
  const [state, setState] = useState<Data | null>(null);
  const [running, setRunning] = useState(false);
  const [mode, setMode] = useState<"ai" | "manual">("ai");

  // 1. LOAD INITIAL STATE ONLY ONCE
  useEffect(() => {
    fetchState(mode).then(setState);
  }, [mode]);

  // 2. START SIMULATION
  const start = async () => {
    await startGame();
    setRunning(true);
  };

  const reset = async () => {
    setRunning(false);

    await resetGame();

    const newState = await fetchState(mode);
    setState(newState);
  };

  const move = async () => {
    await sendAction("move");

    const state = await fetchState(mode);
    setState(state);
  };

  const turnLeft = async () => {
    await sendAction("left");

    const state = await fetchState(mode);
    setState(state);
  };

  const turnRight = async () => {
    await sendAction("right");

    const state = await fetchState(mode);
    setState(state);
  };

  const kill = async () => {
    await sendAction("kill");

    const state = await fetchState(mode);
    setState(state);
  };

  // 3. LOOP ONLY WHEN RUNNING
  useEffect(() => {
  if (!running) return;

  if (mode !== "ai") return;

  const interval = setInterval(async () => {
    stepGame()
    const newState = await fetchState(mode);
    setState(newState);

    if (newState.done && newState.phase === 2) {
      setRunning(false);
    }
    }, 400);

    return () => clearInterval(interval);
  }, [running, mode]);

  return {
    state,

    running,
    start,
    reset,

    mode,
    setMode,

    move,
    turnLeft,
    turnRight,
    kill,
  };
}