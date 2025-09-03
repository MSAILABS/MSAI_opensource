"use client";

import { useState, useRef, useEffect, Fragment } from "react";
import { FaFolder } from "react-icons/fa";
import { GoSidebarCollapse } from "react-icons/go";
import { MdViewSidebar } from "react-icons/md";
import { IoOptionsOutline } from "react-icons/io5";
import axios from "axios";
import config from "@/utilities/config";
import { Field, Label, Switch } from "@headlessui/react";
import Records from "../records/records";
import Sidebar from "./sidebar";

let sendActive = true;
const chatbox = () => {
  const [enable, setEnable] = useState(false);
  const [selectedGroup, setSelectedGroup] = useState<null | object>(null);
  const [showRecords, setShowRecords] = useState(false);
  const [showLeftSidebar, setShowLeftSidebar] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  const inputMessage = useRef<HTMLTextAreaElement>(null);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<any>([
    // { type: "user", message: "hello" },
    // { type: "bot", message: "hello" },
  ]);
  const lastItemRef = useRef<HTMLDivElement | null>(null);
  const [showThoughts, setShowThoughts] = useState(false);
  const [thoughts, setThoughts] = useState<any>([
    // "!Hello!",
    // "!Processing you query!",
  ]);
  const [useRecords, setUseRecords] = useState(true);

  const [numberOfChunks, setNumberOfChunks] = useState(2);

  let chatkey = 0;

  const sendMessage = async () => {
    if (
      inputMessage.current?.value.replaceAll(" ", "") == "" ||
      sendActive == false ||
      enable == false
    )
      return;

    if (numberOfChunks < 1 && useRecords == true) {
      alert(
        "number of chunks should be greater then 0, and if you do not want to use records switch off use records at the top of page"
      );
      return;
    }

    if (numberOfChunks > 10) {
      alert("number of chunks should be between 1 to 10");
      return;
    }

    console.log(inputMessage.current?.value);

    const userMessage = {
      message: inputMessage.current?.value,
      type: "user",
      records_info: [],
    };
    setMessages((prevMessages: any) => [...prevMessages, userMessage]);

    try {
      setLoading(true);
      if (showSettings == true) setShowSettings(false);

      sendActive = false;
      setShowThoughts(true);

      const context =
        messages.legnth > 5
          ? messages.filter((e: any) => e["type"] != "error").slice(-5)
          : messages.filter((e: any) => e["type"] != "error");

      const selectedGroup = JSON.parse(
        localStorage.getItem("selectedGroup") ?? ""
      );

      if (!selectedGroup || selectedGroup == null || selectedGroup == "null") {
        alert("Group is not seleted, please first select a group");
        return;
      }

      const response = await axios.post(`${config.api_url}/chat`, {
        query: inputMessage.current?.value,
        context: context,
        use_records: useRecords,
        number_of_chunks: numberOfChunks,
        cluster_name: selectedGroup["name"],
      });

      console.log(response);

      let temp_records_info = [];

      for (let i = 0; i < response.data.records_ids.length; i++) {
        temp_records_info.push({
          id: response.data.records_ids[i],
          title: response.data.records_titles[i],
        });
      }

      console.log(temp_records_info);
      const botMessage = {
        message: response.data.message,
        type: "bot",
        records_info: temp_records_info,
      };
      setMessages((prevMessages: any) => [...prevMessages, botMessage]);
    } catch (err) {
      console.log(err);
      const errMessage = {
        message: "Error occured, can not process the query.",
        type: "error",
        records_info: [],
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

  useEffect(() => {
    setMessages([]);
  }, [selectedGroup]);

  useEffect(() => {
    if (lastItemRef.current) {
      lastItemRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]); // Runs whenever 'items' changes

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
    <>
      {enable && (
        <button
          className="links_div_btn chatbot_record_btn"
          onClick={() => setShowRecords(!showRecords)}
        >
          <FaFolder /> <span>Records</span>
        </button>
      )}
      <Field className="flex justify-end fixed p-1 record-toggle">
        <Label className="mr-2">Use Records</Label>
        <Switch
          checked={useRecords}
          onChange={setUseRecords}
          className="group inline-flex h-6 w-11 items-center rounded-full bg-gray-200 transition data-[checked]:bg-blue-600"
        >
          <span className="size-4 translate-x-1 rounded-full bg-white transition group-data-[checked]:translate-x-6" />
        </Switch>
      </Field>
      <div className="chatArea">
        <div className="chat-bubble-container" id="chat-bubble-container">
          {messages.length > 0 ? (
            <>
              {messages.map((e: any, index: number) => (
                <div
                  ref={index === messages.length - 1 ? lastItemRef : null}
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

                  {e["records_info"] && e["records_info"].length > 0 && (
                    <>
                      <hr style={{ margin: "20px 0px" }} />
                      <p style={{ marginBottom: "10px" }}>
                        Records used for AI response
                      </p>
                      {e["records_info"].map((e: any, index: number) => (
                        <p style={{ margin: "5px 0px" }} key={index}>
                          Id: {e["id"]}, Title: {e["title"]}
                        </p>
                      ))}
                    </>
                  )}
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
            <div className="text-center grid gap-y-12 justify-center items-center pb-12 min-h-[60vh] chatbot_intro">
              <div>
                <h1 className="typed-out text-2xl text-white p-1">
                  Welcome to MSAI LABS RAG + AI_Agents powered Chatbot.
                </h1>
              </div>
              <div className="grid grid-cols-1 gap-2 md:grid-cols-1">
                <p className="col-span-1 bg-gray-100 p-4 md:p-5 text-gray-800 rounded-lg">
                  🤖 Use chatbot with records. <br />
                  It helps generating answer using your uploaded records
                  (slower)
                </p>
                <p className="col-span-1 bg-gray-100 p-4 md:p-5 text-gray-800 rounded-lg">
                  🚫 Use chatbot without records. <br />
                  It can be useful when asking general question (faster)
                </p>
                {!enable && (
                  <p className="col-span-1 bg-red-500 p-4 md:p-5 text-white rounded-lg">
                    Chat is disabled. <br />
                    To use chat add group by clicking button on left
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
        <div className="chatinput-container">
          {showThoughts && (
            <div
              className="thought-process w-full"
              id="thought-process-div"
              style={{
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
          )}
          {showSettings && (
            <div
              className="thought-process w-full border-t border-white bg-gray-700"
              id="thought-process-div"
              style={{
                overflowY: "auto",
              }}
            >
              <div className="grid grid-cols-2 place-items-center gap-4 p-3">
                <p>Number of chunks used for AI response</p>
                <input
                  style={{ width: "70px", height: "40px" }}
                  className="px-2 bg-gray-800 color-white border-2-white rounded-lg text-center"
                  type="number"
                  min={1}
                  max={10}
                  placeholder="Number of Chunks"
                  defaultValue={2}
                  disabled={!enable}
                  onChange={(e) => setNumberOfChunks(parseInt(e.target.value))}
                />
              </div>
            </div>
          )}
          <div className="inputArea w-full flex items-center">
            <button
              id="options-btn"
              className="chat-send-btn"
              onClick={() => setShowSettings(!showSettings)}
            >
              <IoOptionsOutline />
            </button>
            <textarea
              ref={inputMessage}
              id="inputBox"
              className="chat-text-area w-full ml-2"
              placeholder="Type a message"
              disabled={!enable}
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
      <div
        style={{ display: showRecords ? "block" : "none" }}
        className="overlay_for_records"
        onClick={() => setShowRecords(!showRecords)}
      ></div>
      <div
        style={{ transform: showRecords ? "scaleX(1)" : "scaleX(0)" }}
        className="records_sidebar"
      >
        <Records showUpBtn={false} showRecords={showRecords} />
      </div>
      <div
        className="overlay_for_records"
        style={{ display: showLeftSidebar ? "block" : "none" }}
        onClick={() => setShowLeftSidebar(!showLeftSidebar)}
      ></div>
      <div
        style={{ transform: showLeftSidebar ? "scaleX(1)" : "scaleX(0)" }}
        className="left_sidebar"
      >
        <Sidebar
          enableChat={enable}
          setEnableChat={setEnable}
          selectedGroup={selectedGroup}
          setSelectedGroup={setSelectedGroup}
        />
      </div>
      <div
        className="left_sidebar_icon"
        onClick={() => setShowLeftSidebar(!showLeftSidebar)}
      >
        <GoSidebarCollapse color="silver" size={"3em"} />
      </div>
    </>
  );
};

export default chatbox;
