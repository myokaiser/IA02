"use client";

import { useEffect, useState, useCallback } from "react";
import {
  fetchState,
  startGame,
  stepGame,
  resetGame,
  sendAction,
} from "@/src/lib/api";
import type { GameState } from "@/src/types/game";

export function useGame() {
  const [state, setState] = useState<GameState | null>(null);
  const [running, setRunning] = useState(false);
  const [mode, setMode] = useState<"ai" | "manual">("ai");

  // LOAD INITIAL STATE ONLY ONCE
  useEffect(() => {
    fetchState(mode).then(setState);
  }, [mode]);
  // ==============================

  // START SIMULATION
  const start = async () => {
    await startGame();
    setRunning(true);
  };
  // ==============================

  // RESET SIMULATION
  const reset = useCallback(async (currentMode: string) => {
    setRunning(false);

    await resetGame();

    const newState = await fetchState(currentMode);
    setState(newState);
  }, []);
  // ==============================

  // HANDLE HUMAN MODE
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
  // ==============================

  // LOOP ONLY WHEN RUNNING
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
  // ==============================
}