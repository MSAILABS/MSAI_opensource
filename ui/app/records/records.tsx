"use client";

import axios from "axios";
import { useState, useEffect } from "react";
import { IoTriangle } from "react-icons/io5";
import Add_Record from "./_components/add_records";
import List_Record from "./_components/list_record";
import config from "@/utilities/config";
import Loading from "../_components/loading";

interface Record {
  id: number;
  title: string;
  description: string;
  upload_date: string;
  vectorized: boolean;
  embedding_model: string;
}

export default function records({ showUpBtn, showRecords }: any) {
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [records, setRecords] = useState<Record[]>([]);
  const [embeddingModel, setEmbeddingModel] = useState("");
  const [loading, setLoading] = useState(true);

  const get_records = async () => {
    try {
      setLoading(true);
      const res = await axios.get(`${config.api_url}/get_records`);

      if (res) {
        setRecords(res.data?.records);
        setEmbeddingModel(res.data?.embedding_model);
      }
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (showRecords) {
      get_records();
    }
  }, [showAddDialog, showRecords]);

  return (
    <div className="text-center h-full records-area">
      <div className="record-add-btn" id="add-button">
        <a
          style={{ display: showUpBtn ? "block" : "none" }}
          href="#add-button"
          className="bg-green-500 text-white p-6 rounded ml-4 fixed bottom-4 flex items-center justify-center"
        >
          <IoTriangle style={{ fontSize: "25px" }} />
        </a>
        <div className="button_div grid">
          <p className="font-bold mt-5">
            Active Vectorizing Model: {embeddingModel}
          </p>
          <Add_Record open={showAddDialog} setOpen={setShowAddDialog} />
        </div>
      </div>
      {loading ? (
        <div className="mt-20">
          <Loading message={"Fetching Records..."} />
        </div>
      ) : (
        <List_Record
          records={records}
          get_records={get_records}
          setRecords={setRecords}
          embeddingModel={embeddingModel}
        />
      )}
    </div>
  );
}
