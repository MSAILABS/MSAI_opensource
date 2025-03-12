"use client";
import axios from "axios";
import config from "@/utilities/config";
import { redirect } from "next/navigation";

interface RecordProps {
  records: Array<{
    id: number;
    title: string;
    description: string;
    upload_date: string;
  }>;
  get_records: () => Promise<void>;
}

export default function record({ records, get_records }: RecordProps) {
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

  const print_records = () => {
    return records.map((e) => (
      <div className="card pt-4 rounded-lg shadow" key={e["id"]}>
        <h2
          className="text-xl font-bold mb-4 card-title line-clamp-1"
          style={{ width: "85%", marginLeft: "auto", marginRight: "auto" }}
        >
          {e["title"]}
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
            onClick={() => delete_records(e["id"])}
          >
            <span className="mr-2">
              <i className="fa fa-trash" />
            </span>
            <span>Delete</span>
          </button>
        </div>
        <div className="mt-4 p-2 px-5 card-text">
          <p className="my-4 text-left record-description">
            {e["description"].replace(/\n/g, " ")}
          </p>
          <p className="mb-4 text-gray-300 text-sm text-left mt-3">
            Upload Date: {e["upload_date"].split(" ")[0]}
          </p>
        </div>
      </div>
    ));
  };

  return print_records();
}
