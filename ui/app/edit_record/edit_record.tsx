"use client";

import config from "@/utilities/config";
import Loading from "@/app/_components/loading";
import Alert from "@/app/_components/alert";
import axios from "axios";
import { useEffect, useRef, useState } from "react";

function edit_record() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [recordId, setRecordId] = useState<number | null>(null);

  const [loading, setLoading] = useState(false);
  const [resType, setResType] = useState({
    res: false,
    error: false,
    message: "",
  });

  const titleInput = useRef<HTMLInputElement>(null);
  const descInput = useRef<HTMLTextAreaElement>(null);

  // Ensure localStorage is only accessed on the client side
  useEffect(() => {
    if (typeof window !== "undefined") {
      setTitle(window.localStorage.getItem("title") || "");
      setDescription(window.localStorage.getItem("description") || "");
      setRecordId(Number(window.localStorage.getItem("record_id")) || -1);
    }
  }, []);

  const saveChanges = async () => {
    if (
      (title == titleInput.current?.value &&
        description == descInput.current?.value) ||
      recordId == -1
    ) {
      return;
    }

    setLoading(true);

    try {
      const res = await axios.post(
        `${config.api_url}/edit_record/${recordId}`,
        {
          title: titleInput.current?.value,
          description: descInput.current?.value,
        }
      );

      if (res.status == 200) {
        resType.res = true;
        resType.message = res.data["message"];

        setResType(resType);
      }
    } catch (err: any) {
      console.log(err);

      resType.res = true;
      resType.error = true;
      resType.message = err.response.data["message"];

      setResType(resType);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="records-area p-6 mt-5 md:mt-10 rounded-lg shadow-md">
      <h1 className="text-3xl font-bold mb-6 text-center text-white">
        Edit Record
      </h1>
      <div className="mb-4">
        <label className="block text-sm font-medium text-white">Title</label>
        <input
          defaultValue={title}
          ref={titleInput}
          type="text"
          className="mt-1 block w-full px-4 py-2 bg-black border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          placeholder="Enter title"
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium text-white">
          Description
        </label>
        <textarea
          ref={descInput}
          defaultValue={description
            .split("===msai-labs page break===")
            .join("\n\n")}
          className="mt-1 block w-full px-4 py-2 bg-black border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          placeholder="Enter description"
          rows={10}
        />
      </div>
      <div className="text-center">
        {loading ? (
          <Loading />
        ) : (
          <button
            onClick={saveChanges}
            className="px-4 py-2 bg-gray-200 text-black rounded-md shadow-sm hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500"
          >
            Save Changes
          </button>
        )}
        {resType.res && (
          <Alert
            type={resType.error ? "danger" : "success"}
            message={resType.message}
          />
        )}
      </div>
    </div>
  );
}

export default edit_record;
