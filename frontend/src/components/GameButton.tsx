
import { useRouter } from "next/navigation";

export default function GameButton() {
  const router = useRouter();
  const handleSignup = () => {
    router.push("/game");
  };

  return (
    <div className="flex items-center gap-3">
      <button
        onClick={handleSignup}
        className="
          px-4 py-2 rounded-md font-mono text-sm cursor-pointer transition hover:bg-zinc-800 bg-zinc-700 text-white
        "
      >
        {"▶ Start"}
      </button>
    </div>
  );
}