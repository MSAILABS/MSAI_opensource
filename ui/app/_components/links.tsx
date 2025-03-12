"use client";

import { FaFolder, FaComments, FaBars } from "react-icons/fa";
import { redirect, usePathname } from "next/navigation";
import Image from "next/image";
import logo from "@/public/Artboard 1 (1).png";

export default function links() {
  const pathname = usePathname();
  const Redirect = (link: string) => {
    redirect(link);
  };

  return (
    <div className="links_div">
      <div className="links_logo" onClick={() => Redirect("/chatbot")}>
        <Image
          src={logo}
          alt="logo"
          style={{
            width: "60px",
            height: "60px",
            borderRadius: "30px",
          }}
        />
        <h1 className="text-2xl">MSAI LABS</h1>
      </div>
      {pathname.includes("/edit_record") && (
        <button className="links_div_btn" onClick={() => Redirect("/chatbot")}>
          <FaComments /> <span>Chatbot</span>
        </button>
      )}
    </div>
  );
}
