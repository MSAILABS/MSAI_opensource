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
}

export default function records() {
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [records, setRecords] = useState<Record[]>([]);
  const [loading, setLoading] = useState(true);

  const get_records = async () => {
    try {
      setLoading(true);
      const res = await axios.get(`${config.api_url}/get_records`);

      if (res) {
        setRecords(res.data?.records);
      }
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    get_records();
  }, [showAddDialog]);

  return (
    <div className="text-center h-full records-area">
      <div className="record-add-btn" id="add-button">
        <a
          href="#add-button"
          className="bg-green-500 text-white p-2 rounded ml-4 fixed bottom-4 right-4 flex items-center justify-center"
        >
          <IoTriangle />
        </a>
        <Add_Record open={showAddDialog} setOpen={setShowAddDialog} />
      </div>
      {loading ? (
        <div className="mt-20">
          <Loading message={"Fetching Records..."} />
        </div>
      ) : (
        <div className="pt-5 px-2 mx-2 records-container grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-4 gap-4">
          {records.length > 0 ? (
            <List_Record records={records} get_records={get_records} />
          ) : (
            <h1 className="absolute top-1/3 w-full left-0 text-center text-4xl">
              There are no records!!!
            </h1>
          )}
        </div>
      )}
    </div>
  );
}
