export default function chatbox() {
    return (
        <div className="col-span-9 md:col-span-8 chatArea">
            <div className="chat-bubble-container" id="chat-bubble-container">
                <div className="text-center grid gap-y-12 justify-center items-center pb-12 min-h-[60vh]">
                    <h1 className="text-2xl text-white p-1">Welcome to MSAI LABS RAG + AI_Agents powered Chatbot.</h1>
                    <div className="grid grid-cols-1 gap-2 md:grid-cols-2">
                        <p className="col-span-1 bg-gray-100 p-4 md:p-5 text-gray-800 rounded-lg">🤖 Use chatbot with whole records</p>
                        <p className="col-span-1 bg-gray-100 p-4 md:p-5 text-gray-800 rounded-lg">📁 Use chatbot with specific record</p>
                        <p className="col-span-1 bg-gray-100 p-4 md:p-5 text-gray-800 rounded-lg">🚫 Use chatbot without records</p>
                        <p className="col-span-1 bg-gray-100 p-4 md:p-5 text-gray-800 rounded-lg">📄 Use chatbot with your specific document</p>
                    </div>
                </div>
                {/* <p className="chat-bubble user-bubble">Hello</p>
                <p className="chat-bubble bot-bubble">Hello, how are you are you fine</p> */}
            </div>
            <div className="chatinput-container">
                <div className="thought-process w-full" id="thought-process-div" style={{display: "none", overflowY: 'auto'}}></div>
                <div className="inputArea w-full flex items-center">
                    <button className="chat-attach-btn chat-buttons-left"><i className="fas fa-paperclip"></i></button>
                    <textarea id="inputBox" className="chat-text-area w-full" placeholder="Type a message"></textarea>
                    <button id="sendButton" className="chat-send-btn chat-buttons-right"><i className="fas fa-paper-plane"></i></button>
                </div>
            </div>
        </div>
    )
}