import { IoTriangle } from "react-icons/io5";
import Add_Record from "./_components/add_records";

export default function records() {
    return (
        <div className="col-span-9 md:col-span-8 text-center h-full records-area">
            <div className="record-add-btn" id="add-button">
                
                <a href="#add-button" className="bg-green-500 text-white p-2 rounded ml-4 fixed bottom-4 right-4 flex items-center justify-center">
                    <IoTriangle />
                </a>
                <Add_Record />
            </div>
            <div className="pt-5 px-2 mx-2 records-container grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 gap-4">
                <div className="card pt-4 rounded shadow">
                    <h2 className="text-xl font-bold mb-4 card-title">Medical History</h2>
                    <div className="grid grid-cols-5 gap-1 px-4 card-btns">
                        <button className="flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-edit" /></span>
                            <span>Edit</span>
                        </button>
                        |
                        <button style={{color: '#008cff'}} className="500 flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-comments" /></span>
                            <span>Chat</span>
                        </button>
                        |
                        <button style={{color: 'red'}} className="flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-trash" /></span>
                            <span>Delete</span>
                        </button>
                    </div>
                    <div className="mt-4 p-2 px-5 card-text">
                        <p className="my-4 text-left record-description">
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt, iusto assumenda, dolores aut similique magnam sint vel adipisci nostrum minima modi. Molestiae aliquam dolore eum, minima nulla repellat amet obcaecati. Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt, iusto assumenda, dolores aut similique magnam sint vel adipisci nostrum minima modi. Molestiae aliquam dolore eum, minima nulla repellat amet obcaecati.
                        </p>
                        <p className="mb-4 text-gray-300 text-sm text-left mt-3">Upload Date: 2023-10-01</p>
                    </div>
                </div>
                <div className="card pt-4 rounded shadow">
                    <h2 className="text-xl font-bold mb-4 card-title">Medical History</h2>
                    <div className="grid grid-cols-5 gap-1 px-4 card-btns">
                        <button className="flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-edit" /></span>
                            <span>Edit</span>
                        </button>
                        |
                        <button style={{color: '#008cff'}} className="500 flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-comments" /></span>
                            <span>Chat</span>
                        </button>
                        |
                        <button style={{color: 'red'}} className="flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-trash" /></span>
                            <span>Delete</span>
                        </button>
                    </div>
                    <div className="mt-4 p-2 px-5 card-text">
                        <p className="my-4 text-left record-description">
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt, iusto assumenda, dolores aut similique magnam sint vel adipisci nostrum minima modi. Molestiae aliquam dolore eum, minima nulla repellat amet obcaecati. Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt, iusto assumenda, dolores aut similique magnam sint vel adipisci nostrum minima modi. Molestiae aliquam dolore eum, minima nulla repellat amet obcaecati.
                        </p>
                        <p className="mb-4 text-gray-300 text-sm text-left mt-3">Upload Date: 2023-10-01</p>
                    </div>
                </div>
                <div className="card pt-4 rounded shadow">
                    <h2 className="text-xl font-bold mb-4 card-title">Medical History</h2>
                    <div className="grid grid-cols-5 gap-1 px-4 card-btns">
                        <button className="flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-edit" /></span>
                            <span>Edit</span>
                        </button>
                        |
                        <button style={{color: '#008cff'}} className="500 flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-comments" /></span>
                            <span>Chat</span>
                        </button>
                        |
                        <button style={{color: 'red'}} className="flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-trash" /></span>
                            <span>Delete</span>
                        </button>
                    </div>
                    <div className="mt-4 p-2 px-5 card-text">
                        <p className="my-4 text-left record-description">
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt, iusto assumenda, dolores aut similique magnam sint vel adipisci nostrum minima modi. Molestiae aliquam dolore eum, minima nulla repellat amet obcaecati. Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt, iusto assumenda, dolores aut similique magnam sint vel adipisci nostrum minima modi. Molestiae aliquam dolore eum, minima nulla repellat amet obcaecati.
                        </p>
                        <p className="mb-4 text-gray-300 text-sm text-left mt-3">Upload Date: 2023-10-01</p>
                    </div>
                </div>
                <div className="card pt-4 rounded shadow">
                    <h2 className="text-xl font-bold mb-4 card-title">Medical History</h2>
                    <div className="grid grid-cols-5 gap-1 px-4 card-btns">
                        <button className="flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-edit" /></span>
                            <span>Edit</span>
                        </button>
                        |
                        <button style={{color: '#008cff'}} className="500 flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-comments" /></span>
                            <span>Chat</span>
                        </button>
                        |
                        <button style={{color: 'red'}} className="flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-trash" /></span>
                            <span>Delete</span>
                        </button>
                    </div>
                    <div className="mt-4 p-2 px-5 card-text">
                        <p className="my-4 text-left record-description">
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt, iusto assumenda, dolores aut similique magnam sint vel adipisci nostrum minima modi. Molestiae aliquam dolore eum, minima nulla repellat amet obcaecati. Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt, iusto assumenda, dolores aut similique magnam sint vel adipisci nostrum minima modi. Molestiae aliquam dolore eum, minima nulla repellat amet obcaecati.
                        </p>
                        <p className="mb-4 text-gray-300 text-sm text-left mt-3">Upload Date: 2023-10-01</p>
                    </div>
                </div>
                <div className="card pt-4 rounded shadow">
                    <h2 className="text-xl font-bold mb-4 card-title">Medical History</h2>
                    <div className="grid grid-cols-5 gap-1 px-4 card-btns">
                        <button className="flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-edit" /></span>
                            <span>Edit</span>
                        </button>
                        |
                        <button style={{color: '#008cff'}} className="500 flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-comments" /></span>
                            <span>Chat</span>
                        </button>
                        |
                        <button style={{color: 'red'}} className="flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-trash" /></span>
                            <span>Delete</span>
                        </button>
                    </div>
                    <div className="mt-4 p-2 px-5 card-text">
                        <p className="my-4 text-left record-description">
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt, iusto assumenda, dolores aut similique magnam sint vel adipisci nostrum minima modi. Molestiae aliquam dolore eum, minima nulla repellat amet obcaecati. Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt, iusto assumenda, dolores aut similique magnam sint vel adipisci nostrum minima modi. Molestiae aliquam dolore eum, minima nulla repellat amet obcaecati.
                        </p>
                        <p className="mb-4 text-gray-300 text-sm text-left mt-3">Upload Date: 2023-10-01</p>
                    </div>
                </div>
                <div className="card pt-4 rounded shadow">
                    <h2 className="text-xl font-bold mb-4 card-title">Medical History</h2>
                    <div className="grid grid-cols-5 gap-1 px-4 card-btns">
                        <button className="flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-edit" /></span>
                            <span>Edit</span>
                        </button>
                        |
                        <button style={{color: '#008cff'}} className="500 flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-comments" /></span>
                            <span>Chat</span>
                        </button>
                        |
                        <button style={{color: 'red'}} className="flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-trash" /></span>
                            <span>Delete</span>
                        </button>
                    </div>
                    <div className="mt-4 p-2 px-5 card-text">
                        <p className="my-4 text-left record-description">
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt, iusto assumenda, dolores aut similique magnam sint vel adipisci nostrum minima modi. Molestiae aliquam dolore eum, minima nulla repellat amet obcaecati. Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt, iusto assumenda, dolores aut similique magnam sint vel adipisci nostrum minima modi. Molestiae aliquam dolore eum, minima nulla repellat amet obcaecati.
                        </p>
                        <p className="mb-4 text-gray-300 text-sm text-left mt-3">Upload Date: 2023-10-01</p>
                    </div>
                </div>
                <div className="card pt-4 rounded shadow">
                    <h2 className="text-xl font-bold mb-4 card-title">Medical History</h2>
                    <div className="grid grid-cols-5 gap-1 px-4 card-btns">
                        <button className="flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-edit" /></span>
                            <span>Edit</span>
                        </button>
                        |
                        <button style={{color: '#008cff'}} className="500 flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-comments" /></span>
                            <span>Chat</span>
                        </button>
                        |
                        <button style={{color: 'red'}} className="flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-trash" /></span>
                            <span>Delete</span>
                        </button>
                    </div>
                    <div className="mt-4 p-2 px-5 card-text">
                        <p className="my-4 text-left record-description">
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt, iusto assumenda, dolores aut similique magnam sint vel adipisci nostrum minima modi. Molestiae aliquam dolore eum, minima nulla repellat amet obcaecati. Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt, iusto assumenda, dolores aut similique magnam sint vel adipisci nostrum minima modi. Molestiae aliquam dolore eum, minima nulla repellat amet obcaecati.
                        </p>
                        <p className="mb-4 text-gray-300 text-sm text-left mt-3">Upload Date: 2023-10-01</p>
                    </div>
                </div>
                <div className="card pt-4 rounded shadow">
                    <h2 className="text-xl font-bold mb-4 card-title">Medical History</h2>
                    <div className="grid grid-cols-5 gap-1 px-4 card-btns">
                        <button className="flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-edit" /></span>
                            <span>Edit</span>
                        </button>
                        |
                        <button style={{color: '#008cff'}} className="500 flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-comments" /></span>
                            <span>Chat</span>
                        </button>
                        |
                        <button style={{color: 'red'}} className="flex justify-center px-1 items-center">
                            <span className="mr-2"><i className="fa fa-trash" /></span>
                            <span>Delete</span>
                        </button>
                    </div>
                    <div className="mt-4 p-2 px-5 card-text">
                        <p className="my-4 text-left record-description">
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt, iusto assumenda, dolores aut similique magnam sint vel adipisci nostrum minima modi. Molestiae aliquam dolore eum, minima nulla repellat amet obcaecati. Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt, iusto assumenda, dolores aut similique magnam sint vel adipisci nostrum minima modi. Molestiae aliquam dolore eum, minima nulla repellat amet obcaecati.
                        </p>
                        <p className="mb-4 text-gray-300 text-sm text-left mt-3">Upload Date: 2023-10-01</p>
                    </div>
                </div>
            </div>
        </div>
    )
}