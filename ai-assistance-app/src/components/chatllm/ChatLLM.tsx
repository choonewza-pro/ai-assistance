"use client";
import axios from "axios";
import React from "react";

const ChatLLM = () => {
  const onClick = async () => {
    console.log("ChatLLM button clicked");
    // const [error, result] = await to(
    //   axios
    //     .get(
    //       "http://localhost/ask-typhoon-stream?prompt=แต่งเรียงความกระต่ายกับเต่าใหมหน่อย"
    //     )
    //     .then((res) => res.data)
    // );
    // if (error) {
    //   console.log("ChatLLM error", error);
    // }
    // if (result) {
    //   console.log("ChatLLM result", result);
    // }

    axios({
        method: 'get',
        url: 'http://localhost/ask-typhoon-stream',
        params: {
          prompt: 'แต่งเรียงความกระต่ายกับเต่าใหมหน่อย',
          model: '1b'
        },
        responseType: 'stream'
      })
        .then(response => {
          response.data.on('data', (chunk:unknown) => {
            console.log((chunk as Buffer).toString());
          });
      
          response.data.on('end', () => {
            console.log('Stream ended');
          });
        })
        .catch(error => {
          console.error(error);
        });
  };
  return (
    <div>
      ChatLLM
      <button
        type="button"
        onClick={onClick}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded block cursor-pointer"
      >
        Click me
      </button>
    </div>
  );
};

export default ChatLLM;
