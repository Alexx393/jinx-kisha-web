"use client";

import { useState } from "react";
import KishaAvatar from "@/components/KishaAvatar";

export default function Home() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!message.trim()) return;

    try {
      setLoading(true);
      const res = await fetch("http://localhost:10000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: message }),
      });
      const data = await res.json();
      setResponse(data.reply || "No response.");
    } catch (err) {
      console.error(err);
      setResponse("Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const handleSpeak = async () => {
    if (!response) return;

    setIsSpeaking(true);
    try {
      await fetch("http://localhost:10000/talk", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: response }),
      });
    } catch (err) {
      console.error(err);
    } finally {
      setTimeout(() => setIsSpeaking(false), 4000);
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center gap-8 p-6 bg-gradient-to-br from-black via-slate-900 to-black text-white">
      <h1 className="text-6xl md:text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-pink-500 via-purple-500 to-indigo-500">
        🧠 KISHA
      </h1>

      <KishaAvatar isSpeaking={isSpeaking} />

      <textarea
        className="w-full max-w-2xl p-4 rounded-lg bg-white/90 text-black placeholder:text-black/60 focus:outline-none focus:ring-2 focus:ring-pink-500 transition"
        rows={4}
        placeholder="Ask Kisha anything..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />

      <div className="flex flex-wrap gap-4">
        <button
          onClick={handleAsk}
          disabled={loading}
          className="px-6 py-3 rounded-lg bg-pink-600 hover:bg-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          {loading ? "Thinking..." : "Ask"}
        </button>

        <button
          onClick={handleSpeak}
          disabled={!response}
          className="px-6 py-3 rounded-lg bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          Speak
        </button>
      </div>

      {response && (
        <div className="mt-6 w-full max-w-2xl p-4 bg-white/10 backdrop-blur-md rounded-lg border border-white/10">
          <p className="text-purple-300">{response}</p>
        </div>
      )}
    </main>
  );
}
