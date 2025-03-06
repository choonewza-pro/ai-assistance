/* eslint-disable @next/next/no-async-client-component */
"use client";
import React, { useState } from "react";
import {
  Bars3Icon,
  ChevronLeftIcon,
  ChevronRightIcon,
} from "@heroicons/react/24/solid";
import to from "await-to-js";
import axios from "axios";

const ChatLLM =  () => {
  // const [streaming,setStreaming] = useState(false);
  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState<string>("");
  const [showLeftColumn, setShowLeftColumn] = useState(true);
  const [showRightColumn, setShowRightColumn] = useState(true);

  const handleSend = async () => {
    if (input.trim()) {
      setMessages([...messages, input]);
      setInput("");

      const question = encodeURIComponent(input);
      const url = `https://eportfolio.ntplc.co.th/rag-pdf-prompt?question=${question}`;
      const [error,resPrompt] = await to(
        axios.get(url).then((res) => res.data)
      )
      if(error){
        console.log("error",error)
        return
      }
      
      console.log("XXX",resPrompt)
      // Here you would add the logic to send the message to Ollama LLM and get the response
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {showLeftColumn && (
        <div className="hidden sm:block w-1/4 bg-gray-200 p-4">
          <button
            className="mb-4 p-2 bg-blue-500 text-white rounded-lg"
            onClick={() => setShowLeftColumn(false)}
          >
            <ChevronLeftIcon className="w-6 h-6" />
          </button>
          <div>Left Column Content</div>
        </div>
      )}
      <div className="flex-grow flex flex-col">
        <div className="flex justify-between p-4 bg-gray-100 border-b border-gray-300">
          <div>
            {!showLeftColumn && (
              <button
                className="p-2 bg-blue-500 text-white rounded-lg"
                onClick={() => setShowLeftColumn(!showLeftColumn)}
              >
                <Bars3Icon className="w-6 h-6" />
              </button>
            )}
          </div>

          <div>
            <h1 className="text-xl font-bold text-blue-500">อยากอบรมหลักสูตรอะไรถามมาครับ</h1>
          </div>

          <div>
            {!showRightColumn && (
              <button
                className="p-2 bg-blue-500 text-white rounded-lg"
                onClick={() => setShowRightColumn(!showRightColumn)}
              >
                <Bars3Icon className="w-6 h-6" />
              </button>
            )}
          </div>
        </div>
        <div className="flex-grow p-4 overflow-y-auto">
          {messages.map((message, index) => (
            <div key={index} className="mb-4">
              <div className="bg-blue-500 text-white p-2 rounded-lg">
                {message}
              </div>
            </div>
          ))}
        </div>
        <div className="p-4 bg-white border-t border-gray-300">
          <div className="flex">
            <input
              type="text"
              className="flex-grow p-2 border border-gray-300 rounded-lg text-black"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
            />
            <button
              className="ml-2 p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-400 cursor-pointer"
              onClick={handleSend}
            >
              Send
            </button>
          </div>
        </div>
      </div>
      {showRightColumn && (
        <div className="hidden sm:block w-1/4 bg-gray-200 p-4">
          <div className="flex justify-end">
            <button
              className="mb-4 p-2 bg-blue-500 text-white rounded-lg"
              onClick={() => setShowRightColumn(false)}
            >
              <ChevronRightIcon className="w-6 h-6" />
            </button>
          </div>
          <div>Right Column Content</div>
        </div>
      )}
    </div>
  );
};

export default ChatLLM;
