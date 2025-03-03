import Link from 'next/link'

export default function page() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 pb-20 gap-4 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <h1 className="text-2xl sm:text-4xl font-bold">MSAI LABS AI AGENTS</h1>
      <Link className="mt-4 rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5" href="/chatbot">Go to Chatbot</Link>
    </div>
  );
}
