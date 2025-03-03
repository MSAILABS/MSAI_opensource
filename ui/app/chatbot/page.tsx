import Chatbox from "./chatbox";
import Links from "../_components/links";

export default function page() {
    return (
        <div className="grid grid-cols-1 md:grid-cols-10 h-screen">
            <Links />
            <Chatbox />
        </div>
    );
}