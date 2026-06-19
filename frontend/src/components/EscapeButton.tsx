"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function EscapeButton() {
  const router = useRouter();

  const goHome = () => {
    router.push("/");
  };

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        goHome();
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  });

  return (
    <button
    onClick={goHome}
    className="
        fixed bottom-4 left-4 z-50 flex items-center gap-2 text-zinc-400 hover:text-white transition-colors
    "
    >
      <span className="
          px-2 py-1 rounded border border-zinc-600 bg-zinc-900 font-mono text-sm
      ">
        Esc
      </span>

      <span className="text-sm">
        Return to menu
      </span>
    </button>
  );
}