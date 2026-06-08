
export default function GitHubButton() {

  return (
    <div className="flex items-center gap-3">
      <a
        href="https://github.com/myokaiser/IA02/tree/web-demo"
        className={`
          px-4 py-2 rounded-md font-mono text-sm
          bg-zinc-700 text-white
        `}
      >
        {"Github"}
      </a>
    </div>
  );
}