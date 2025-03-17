"use client";
import axios from "axios";
import config from "@/utilities/config";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";
import Loading from "@/app/_components/loading";

interface RecordProps {
  records: Array<{
    id: number;
    title: string;
    description: string;
    upload_date: string;
    vectorized: boolean;
    embedding_model: string;
  }>;
  embeddingModel: string;
  get_records: () => Promise<void>;
  setRecords: React.Dispatch<React.SetStateAction<any>>;
}

export default function record({
  records,
  get_records,
  setRecords,
  embeddingModel,
}: RecordProps) {
  const [showRevectorizeBtn, setShowRevectorizeBtn] = useState(true);
  const [vectorizing, setVectorizing] = useState(
    records.map((e) => ({ id: e.id, is_vectorizing: false }))
  );

  const delete_records = async (record_id: number) => {
    try {
      const res = await axios.get(
        `${config.api_url}/delete_record/${record_id}`
      );

      if (res.data["message"]) {
        alert(res.data["message"]);
        await get_records();
      }
    } catch (err) {
      console.log(err);
    }
  };

  const edit_record = (
    record_id: number,
    title: string,
    description: string
  ) => {
    window.localStorage.setItem("record_id", record_id.toString());
    window.localStorage.setItem("title", title);
    console.log(description);
    window.localStorage.setItem("description", description);

    redirect("/edit_record");
  };

  useEffect(() => {
    let found_record_which_needs_revectorization = false;

    for (let i = 0; i < records.length; i++) {
      const element = records[i];
      if (element.embedding_model != embeddingModel) {
        found_record_which_needs_revectorization = true;
        break;
      }
    }

    setShowRevectorizeBtn(found_record_which_needs_revectorization);
  }, []);

  const revectorize_all_records = async () => {
    records.forEach(async (record) => {
      if (record.embedding_model != embeddingModel) {
        await vectorize_record(record.id);
      }
    });

    setShowRevectorizeBtn(false);
  };

  const vectorize_record = async (record_id: number) => {
    setVectorizing((prevVectorizing) =>
      prevVectorizing.map((item) =>
        item.id === record_id ? { ...item, is_vectorizing: true } : item
      )
    );

    try {
      const res = await axios.get(
        `${config.api_url}/add_record_into_vector_db/${record_id}`
      );

      console.log(res);

      if (res.status == 201) {
        const updatedRecord: {
          id: number;
          title: string;
          description: string;
          upload_date: string;
          vectorized: boolean;
        }[] = [];

        records.forEach((element) => {
          if (element.id == record_id) {
            element.vectorized = true;
            element.embedding_model = embeddingModel;
          }

          updatedRecord.push(element);
        });

        setRecords(updatedRecord);

        alert(res.data["message"]);
      } else {
        console.log(res.data);
        alert("Error on vectorizing text");
      }
    } catch (err) {
      console.log(err);
      alert("Error on vectorizing text");
    } finally {
      setVectorizing((prevVectorizing) =>
        prevVectorizing.map((item) =>
          item.id === record_id ? { ...item, is_vectorizing: false } : item
        )
      );
    }
  };

  const print_records = () => {
    return records.map((e, index) => (
      <div className="card pt-4 rounded-lg shadow" key={e.id}>
        <h2
          className="text-xl font-bold mb-4 card-title line-clamp-1"
          style={{ width: "85%", marginLeft: "auto", marginRight: "auto" }}
        >
          {e.title}
        </h2>
        <div className="gap-1 px-4 sm:px-1 card-btns">
          <button
            className="flex justify-center px-1 items-center"
            onClick={() => edit_record(e.id, e.title, e.description)}
          >
            <span className="mr-2">
              <i className="fa fa-edit" />
            </span>
            <span>Edit</span>
          </button>
          <span>|</span>
          <button
            style={{ color: "red" }}
            className="flex justify-center px-1 items-center"
            onClick={() => delete_records(e.id)}
          >
            <span className="mr-2">
              <i className="fa fa-trash" />
            </span>
            <span>Delete</span>
          </button>
        </div>
        <div className="mt-4 p-2 px-5 card-text">
          <p className="my-4 text-left record-description">
            {e.description.replace(/\n/g, " ")}
          </p>
          <p className="mb-4 text-gray-300 text-sm text-left mt-3">
            Upload Date: {e.upload_date.split(" ")[0]}
          </p>
          <p className="mb-4 text-gray-300 text-sm text-left mt-3">
            Vectorized using :{" "}
            {e.embedding_model ? e.embedding_model : "No Model"}
          </p>
          <div
            className="grid justify-center"
            style={{
              gridTemplateColumns: "auto 10px",
              alignItems: "center",
              alignContent: "center",
            }}
          >
            {e.vectorized && e.embedding_model == embeddingModel ? (
              <p className="text-gray-500">Vectorized</p>
            ) : vectorizing[index].is_vectorizing ? (
              <Loading message={"Vectorizing Text"} textSizeClass={"text-lg"} />
            ) : e.embedding_model == undefined ? (
              <div className="relative group">
                <button
                  onClick={() => vectorize_record(e.id)}
                  className="bg-green-500 px-4 py-1 rounded hover:bg-green-600"
                >
                  Vectorize text
                </button>
                <div className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 hidden group-hover:block w-max px-3 py-1 text-sm text-white bg-gray-800 rounded-lg shadow-lg">
                  Vectorize the text for
                  <br /> using this record in AI response.
                  <div className="absolute left-1/2 -translate-x-1/2 top-full w-2 h-2 rotate-45 bg-gray-800"></div>
                </div>
              </div>
            ) : (
              <div className="relative group">
                <button
                  onClick={() => vectorize_record(e.id)}
                  className="bg-green-500 px-4 py-1 rounded hover:bg-green-600"
                >
                  Revectorize text
                </button>
                <div className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 hidden group-hover:block w-max px-3 py-1 text-sm text-white bg-gray-800 rounded-lg shadow-lg">
                  revectorize the text, because
                  <br /> embedding_model is changed.
                  <div className="absolute left-1/2 -translate-x-1/2 top-full w-2 h-2 rotate-45 bg-gray-800"></div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    ));
  };

  return (
    <>
      {showRevectorizeBtn && (
        <button
          className="bg-blue-500 text-white py-2 rounded my-2"
          style={{ width: "180px" }}
          onClick={revectorize_all_records}
        >
          Revectorize all
        </button>
      )}
      <div className="pt-5 px-2 mx-2 records-container grid grid-cols-1 md:grid-cols-1 lg:grid-cols-2 xl:grid-cols-2 2xl:grid-cols-3 gap-4 records_list_container">
        {records.length > 0 ? (
          print_records()
        ) : (
          <h1 className="absolute top-1/3 w-full left-0 text-center text-4xl">
            There are no records!!!
          </h1>
        )}
      </div>
    </>
  );
}
