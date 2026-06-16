"use client";

import { useEffect } from "react";

type Props = {
  move: () => Promise<void>;
  left: () => Promise<void>;
  right: () => Promise<void>;
  kill: () => Promise<void>;
};

export function useKeyboard({
  move,
  left,
  right,
  kill,
}: Props) {

  useEffect(() => {

    const handleKeyDown = async (
      e: KeyboardEvent
    ) => {

      console.log("key", e.key.toLowerCase())

      switch (e.key.toLowerCase()) {

        case " ":
          await move();
          break;

        case "arrowleft":
          await left();
          break;

        case "arrowright":
          await right();
          break;

        case "k":
          await kill();
          break;
      }
    };

    window.addEventListener(
      "keydown",
      handleKeyDown
    );

    return () =>
      window.removeEventListener(
        "keydown",
        handleKeyDown
      );

  }, [move, left, right, kill]);
}