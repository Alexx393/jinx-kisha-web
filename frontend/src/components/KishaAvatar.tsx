"use client";

import { motion, useAnimation } from "framer-motion";
import { useState, useEffect } from "react";

export default function KishaAvatar({ isSpeaking }: { isSpeaking: boolean }) {
  const [blinking, setBlinking] = useState(false);
  const eyeControls = useAnimation();

  // Blink every few seconds
  useEffect(() => {
    const blinkInterval = setInterval(() => {
      setBlinking(true);
      setTimeout(() => setBlinking(false), 200);
    }, 4000);
    return () => clearInterval(blinkInterval);
  }, []);

  // Subtle eye movement back and forth
  useEffect(() => {
    const loopEyes = async () => {
      while (true) {
        await eyeControls.start({ x: -2, y: -1, transition: { duration: 2 } });
        await eyeControls.start({ x: 2, y: 1, transition: { duration: 2 } });
      }
    };
    loopEyes();
  }, [eyeControls]);

  return (
    <motion.div
      className="w-52 h-52 md:w-64 md:h-64 rounded-full bg-gradient-to-br from-purple-600 via-pink-500 to-indigo-700 shadow-2xl relative overflow-hidden border-4 border-white flex items-center justify-center"
      animate={{ scale: isSpeaking ? 1.1 : 1 }}
      transition={{ type: "spring", stiffness: 200 }}
    >
      {/* Eyes */}
      <motion.div
        className="absolute w-6 h-6 bg-white rounded-full left-1/3 top-1/3"
        animate={eyeControls}
      >
        {blinking && (
          <div className="absolute w-full h-full bg-black rounded-full" />
        )}
      </motion.div>
      <motion.div
        className="absolute w-6 h-6 bg-white rounded-full right-1/3 top-1/3"
        animate={eyeControls}
      >
        {blinking && (
          <div className="absolute w-full h-full bg-black rounded-full" />
        )}
      </motion.div>

      {/* Mouth */}
      <motion.div
        className="absolute bottom-10 left-1/2 transform -translate-x-1/2 w-12 h-2 bg-black rounded-full origin-center"
        animate={{
          scaleY: isSpeaking ? 3 : 1,
          transition: { duration: 0.2 },
        }}
      />

      {/* Extra glow */}
      <motion.div
        className="absolute w-full h-full rounded-full bg-white/10 blur-2xl"
        animate={{ opacity: isSpeaking ? 1 : 0 }}
        transition={{ duration: 0.3 }}
      />
    </motion.div>
  );
}
