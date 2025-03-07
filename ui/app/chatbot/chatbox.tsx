"use client";

import { useState, useRef, useEffect, Fragment } from "react";
import axios from "axios";
import config from "@/utilities/config";

let sendActive = true;
const chatbox = () => {
  const inputMessage = useRef<HTMLTextAreaElement>(null);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<any>([]);
  const [showThoughts, setShowThoughts] = useState(false);
  const [thoughts, setThoughts] = useState<any>([]);
  let chatkey = 0;

  const sendMessage = async () => {
    if (
      inputMessage.current?.value.replaceAll(" ", "") == "" ||
      sendActive == false
    )
      return;

    console.log(inputMessage.current?.value);

    const userMessage = { message: inputMessage.current?.value, type: "user" };
    setMessages((prevMessages: any) => [...prevMessages, userMessage]);

    try {
      setLoading(true);

      sendActive = false;
      setShowThoughts(true);
      const response = await axios.post(`${config.api_url}/chat`, {
        query: inputMessage.current?.value,
      });

      const botMessage = { message: response.data.message, type: "bot" };
      setMessages((prevMessages: any) => [...prevMessages, botMessage]);
    } catch (err) {
      console.log(err);
      const errMessage = {
        message: "Error occured, can not process the query.",
        type: "error",
      };
      setMessages((prevMessages: any) => [...prevMessages, errMessage]);
    } finally {
      if (inputMessage.current) inputMessage.current.value = "";
      sendActive = true;
      setLoading(false);

      setTimeout(() => {
        setShowThoughts(false);
        setThoughts([]);
      }, 2000);
    }
  };

  function startEventSource() {
    // Create a new EventSource object, pointing to the server URL that sends events.
    const eventSource = new EventSource(`${config.api_url}/sse`);

    // Event listener for 'open' event, which indicates that the connection has been established.
    eventSource.onopen = function (event) {
      console.log("Connection opened:", event);
    };

    // Event listener for 'message' event, which receives data sent by the server.
    eventSource.onmessage = function (event) {
      console.log("New message:", event.data);

      if (event.data.includes("tools") == false) {
        setThoughts((prevThoughts: any) => [...prevThoughts, event.data]);
      }
    };

    // Event listener for 'error' event, which occurs when there is an error with the connection.
    eventSource.onerror = function (event) {
      console.error("Error occurred:", event);

      // Optionally, close the connection if an error occurs.
      if (event.eventPhase === EventSource.CLOSED) {
        eventSource.close();
        console.log("Connection closed due to error.");
      }
    };

    // Optional: Custom event listener for specific events sent by the server.
    eventSource.addEventListener("customEvent", function (event) {
      console.log("Custom event received:", event.data);
      // Process the custom event data here.
    });
  }

  useEffect(() => {
    // Call the function to start listening to the EventSource.
    startEventSource();
  }, []);

  const processMessage = (messages: any) => {
    let key = 9999;
    const filteredMessages = messages.filter((e: any) => e.length > 0);
    return filteredMessages.map((e: any, index: number) => (
      <Fragment key={key++}>
        <p>{e}</p>
        {index < filteredMessages.length - 1 && <br />}
      </Fragment>
    ));
  };

  return (
    <div className="chatArea">
      <div className="chat-bubble-container" id="chat-bubble-container">
        {messages.length > 0 ? (
          <>
            {messages.map((e: any) => (
              <div
                key={chatkey++}
                className={`chat-bubble ${
                  e["type"] == "user"
                    ? "user-bubble"
                    : e["type"] == "error"
                    ? "bot-bubble bg-red-500"
                    : "bot-bubble"
                }`}
              >
                {processMessage(e["message"].split("\n"))}
              </div>
            ))}
            {loading && (
              <div className="chat-bubble bot-bubble" id="process_query_text">
                <p>
                  <span className="loading-icon">⏳</span> Processing Query
                </p>
              </div>
            )}
          </>
        ) : (
          <div className="text-center grid gap-y-12 justify-center items-center pb-12 min-h-[60vh]">
            <h1 className="text-2xl text-white p-1">
              Welcome to MSAI LABS RAG + AI_Agents powered Chatbot.
            </h1>
            <div className="grid grid-cols-1 gap-2 md:grid-cols-2">
              <p className="col-span-1 bg-gray-100 p-4 md:p-5 text-gray-800 rounded-lg">
                🤖 Use chatbot with whole records
              </p>
              <p className="col-span-1 bg-gray-100 p-4 md:p-5 text-gray-800 rounded-lg">
                📁 Use chatbot with specific record
              </p>
              <p className="col-span-1 bg-gray-100 p-4 md:p-5 text-gray-800 rounded-lg">
                🚫 Use chatbot without records
              </p>
              <p className="col-span-1 bg-gray-100 p-4 md:p-5 text-gray-800 rounded-lg">
                📄 Use chatbot with your specific document
              </p>
            </div>
          </div>
        )}
      </div>
      <div className="chatinput-container">
        <div
          className="thought-process w-full"
          id="thought-process-div"
          style={{
            display: showThoughts ? "block" : "none",
            overflowY: "auto",
          }}
        >
          {thoughts.map((e: any, index: number) => (
            <p key={index}>
              {index === thoughts.length - 1 && (
                <span className="loading-icon">⏳</span>
              )}
              {e.slice(1, -1)}
            </p>
          ))}
        </div>
        <div className="inputArea w-full flex items-center">
          <button className="chat-attach-btn chat-buttons-left">
            <i className="fas fa-paperclip"></i>
          </button>
          <textarea
            ref={inputMessage}
            id="inputBox"
            className="chat-text-area w-full"
            placeholder="Type a message"
          ></textarea>
          <button
            onClick={sendMessage}
            id="sendButton"
            className="chat-send-btn chat-buttons-right"
          >
            <i className="fas fa-paper-plane"></i>
          </button>
        </div>
      </div>
    </div>
  );
};

export default chatbox;
