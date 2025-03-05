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
    if (records.length > 0) {
      return records.map((e) => (
        <div className="card pt-4 rounded shadow" key={e["id"]}>
          <h2 className="text-xl font-bold mb-4 card-title line-clamp-1">
            {e["title"]}
          </h2>
          <div className="grid grid-cols-5 gap-1 px-4 card-btns">
            <button
              className="flex justify-center px-1 items-center"
              onClick={() =>
                edit_record(e.id, e.title, e.description.replace(/\n/g, " "))
              }
            >
              <span className="mr-2">
                <i className="fa fa-edit" />
              </span>
              <span>Edit</span>
            </button>
            |
            <button
              style={{ color: "#008cff" }}
              className="500 flex justify-center px-1 items-center"
            >
              <span className="mr-2">
                <i className="fa fa-comments" />
              </span>
              <span>Chat</span>
            </button>
            |
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
    } else {
      return (
        <h1 className="absolute top-1/3 w-full left-0 text-center text-4xl">
          There are no records!!!
        </h1>
      );
    }
  };

  return print_records();
}
