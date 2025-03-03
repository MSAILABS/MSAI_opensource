"use client"

import { FaFolder, FaComments, FaBars } from 'react-icons/fa';
import { redirect } from 'next/navigation'

export default function links() {
    function showMenu() {
        const elements = document.querySelectorAll('.mobile-menu-item');
        elements.forEach(element => {
            element.classList.toggle('hidden');
        });
    }

    const Redirect = (link: string) => {
        redirect(link)
    }

    return (
        <div className="h-full pt-6 flex flex-col right-box-shadow col-span-1 md:col-span-2">
            <div className="flex flex-col items-center md:mb-0 border-b border-white relative">
                <h1 className="w-100 text-center text-2xl text-white p-2 font-bold">MSAI LABS</h1>
                <button 
                    className="text-lg font-semibold md:hidden text-white text-center hover:text-gray-800 hover:bg-white flex items-center justify-center absolute right-0 top-0 mt-2 mr-2"
                    onClick={showMenu}
                >
                    <FaBars />
                </button>
            </div>
            <div>
                <p 
                    className="text-lg md:p-1 text-white my-4 text-center md:mt-5 hover:text-gray-800 hover:bg-white flex items-center justify-center hidden md:flex mobile-menu-item"
                    onClick={() => Redirect("/records")}
                >
                    <FaFolder className="mr-2" />
                    Records
                </p>
                <p 
                    className="text-lg md:p-1 my-4 text-white text-center hover:text-gray-800 hover:bg-white flex items-center justify-center hidden md:flex mobile-menu-item"
                    onClick={() => Redirect("/chatbot")}
                >
                    <FaComments className="mr-2" />
                    Chatbot
                </p>
            </div>
        </div>
    )
}